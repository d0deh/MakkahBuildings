"use client";

import { useState } from "react";
import { AlertTriangle, CheckCircle, X } from "lucide-react";
import { Button } from "@/components/ui/button";

interface ValidationBarProps {
  warnings: string[];
}

export function ValidationBar({ warnings }: ValidationBarProps) {
  const [dismissed, setDismissed] = useState(false);
  const [expanded, setExpanded] = useState(false);

  if (dismissed) return null;

  const hasWarnings = warnings.length > 0;

  return (
    <div
      className={`border rounded-lg px-4 py-2 flex items-start gap-3 text-sm ${
        hasWarnings
          ? "bg-status-warning/5 border-status-warning/20 text-status-warning"
          : "bg-status-good/5 border-status-good/20 text-status-good"
      }`}
    >
      {hasWarnings ? (
        <AlertTriangle className="h-4 w-4 mt-0.5 shrink-0" />
      ) : (
        <CheckCircle className="h-4 w-4 mt-0.5 shrink-0" />
      )}
      <div className="flex-1">
        {hasWarnings ? (
          <>
            <button
              onClick={() => setExpanded(!expanded)}
              className="font-bold hover:underline"
            >
              {warnings.length} تحذير في البيانات
            </button>
            {expanded && (
              <ul className="mt-2 space-y-1 text-xs">
                {warnings.map((w, i) => (
                  <li key={i}>{w}</li>
                ))}
              </ul>
            )}
          </>
        ) : (
          <span>البيانات سليمة — لا توجد تحذيرات</span>
        )}
      </div>
      <Button
        size="icon"
        variant="ghost"
        onClick={() => setDismissed(true)}
        className="h-6 w-6 shrink-0 text-inherit hover:text-inherit/80"
      >
        <X className="h-3 w-3" />
      </Button>
    </div>
  );
}
