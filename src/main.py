"""CLI entry point for the Urban Survey Report Generator."""
from __future__ import annotations
import sys
import click
from dotenv import load_dotenv
from pathlib import Path

# Fix Windows console encoding for Arabic output
if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass
if sys.stderr and hasattr(sys.stderr, 'reconfigure'):
    try:
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

load_dotenv()


@click.command()
@click.argument("excel_file", type=click.Path(exists=True))
@click.option("--output", "-o", type=click.Path(), default=None,
              help="Output directory (default: output/)")
@click.option("--no-ai", is_flag=True, default=False,
              help="Generate report without AI analysis")
@click.option("--template", "-t", type=click.Path(exists=True), default=None,
              help="Base PowerPoint template")
def cli(excel_file: str, output: str | None, no_ai: bool, template: str | None):
    """Generate an urban survey PowerPoint report from Excel data.

    EXCEL_FILE: Path to the survey .xlsx file
    """
    from .pipeline import generate_report

    click.echo("\n" + "=" * 50)
    click.echo("  مولد التقارير العمرانية")
    click.echo("  Urban Survey Report Generator")
    click.echo("=" * 50 + "\n")

    click.echo(f"Input: {excel_file}")
    click.echo(f"AI:    {'Disabled' if no_ai else 'Enabled'}")
    click.echo("")

    try:
        result = generate_report(
            excel_path=excel_file,
            output_dir=output,
            use_ai=not no_ai,
            template_path=template,
        )
        click.echo(f"\nReport saved: {result}")
    except Exception as e:
        click.echo(f"\nError: {e}", err=True)
        raise click.Abort()


if __name__ == "__main__":
    cli()
