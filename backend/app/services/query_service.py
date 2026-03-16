"""Pandas query pipeline for precise data answers in chat."""
from __future__ import annotations

import re
import logging
import pandas as pd
from ..core.models import SurveyRecord
from ..ai.client import ask_claude
from ..ai.prompts import COLUMN_SCHEMA, SYSTEM_QUERY_GEN

logger = logging.getLogger(__name__)

# Whitelist of allowed pandas/python operations
ALLOWED_NAMES = {
    "len", "sum", "min", "max", "mean", "median", "count",
    "abs", "round", "int", "float", "str", "bool", "list", "dict",
    "True", "False", "None",
}

# Patterns that indicate unsafe code
UNSAFE_PATTERNS = [
    r'\bimport\b', r'\bexec\b', r'\beval\b', r'\b__\b',
    r'\bopen\b', r'\bos\b', r'\bsys\b', r'\bsubprocess\b',
    r'\bglobals\b', r'\blocals\b', r'\bgetattr\b', r'\bsetattr\b',
    r'\bdelattr\b', r'\bcompile\b', r'\bbreakpoint\b',
]


def _is_safe_expression(code: str) -> bool:
    """Check if the generated code is safe to execute."""
    for pattern in UNSAFE_PATTERNS:
        if re.search(pattern, code):
            return False
    return True


def records_to_dataframe(records: list[SurveyRecord]) -> pd.DataFrame:
    """Convert survey records to a pandas DataFrame."""
    data = [r.model_dump() for r in records]
    return pd.DataFrame(data)


def query_data(records: list[SurveyRecord], question: str) -> dict | None:
    """Two-step pipeline: generate query → execute → return result.

    Returns dict with query/result on success, None on failure.
    """
    # Step 1: Ask Claude to generate a pandas expression
    system = SYSTEM_QUERY_GEN.format(column_schema=COLUMN_SCHEMA)
    try:
        code = ask_claude(system, question, use_cache=False).strip()
    except Exception as e:
        logger.warning("Query generation failed: %s", e)
        return None

    # Clean up — remove markdown code fences if present
    code = re.sub(r'^```(?:python)?\s*', '', code)
    code = re.sub(r'\s*```$', '', code)
    code = code.strip()

    if not code:
        return None

    # Step 2: Validate and execute
    if not _is_safe_expression(code):
        logger.warning("Unsafe query rejected: %s", code)
        return None

    try:
        df = records_to_dataframe(records)
        # Execute in a restricted namespace
        namespace = {"df": df, "pd": pd, "len": len}
        result = eval(code, {"__builtins__": {}}, namespace)  # noqa: S307

        # Convert result to a serializable format
        if isinstance(result, pd.DataFrame):
            if len(result) > 20:
                result = result.head(20)
            result_str = result.to_string()
        elif isinstance(result, pd.Series):
            result_str = result.to_string()
        elif isinstance(result, dict):
            result_str = "\n".join(f"  {k}: {v}" for k, v in result.items())
        elif isinstance(result, (int, float)):
            result_str = str(round(result, 2) if isinstance(result, float) else result)
        else:
            result_str = str(result)

        return {
            "query": code,
            "result": result_str,
            "count": len(result) if hasattr(result, "__len__") and not isinstance(result, str) else None,
        }
    except Exception as e:
        logger.warning("Query execution failed: %s — code: %s", e, code)
        return None
