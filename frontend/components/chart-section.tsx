"use client";

import { useState } from "react";
import { Eye, EyeOff } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import { EditableText } from "@/components/editable-text";
import { regenerateSection } from "@/lib/api";
import { useDashboardStore } from "@/lib/store";

interface ChartSectionProps {
  sessionId: string;
  chartId: string;
  title: string;
  image: string;
  aiDescription: string | null;
  aiSection: string;
  fullWidth?: boolean;
}

export function ChartSection({
  sessionId,
  chartId,
  title,
  image,
  aiDescription,
  aiSection,
  fullWidth,
}: ChartSectionProps) {
  const [regeneratedText, setRegeneratedText] = useState<string | null>(null);
  const [isRegenerating, setIsRegenerating] = useState(false);
  const { hiddenSections, toggleSection } = useDashboardStore();

  const isHidden = hiddenSections.has(chartId);
  const description = regeneratedText ?? aiDescription;

  const handleRegenerate = async () => {
    setIsRegenerating(true);
    try {
      const result = await regenerateSection(sessionId, aiSection);
      setRegeneratedText(result.text);
    } catch (err) {
      console.error("Regenerate failed:", err);
    } finally {
      setIsRegenerating(false);
    }
  };

  if (isHidden) {
    return (
      <div
        className={`bg-[hsl(var(--surface))] border border-[hsl(var(--border))] rounded-lg overflow-hidden opacity-50 ${
          fullWidth ? "col-span-full" : ""
        }`}
      >
        <div className="px-6 py-3 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <h3 className="text-muted-foreground font-bold text-sm">{title}</h3>
            <span className="text-[10px] bg-muted text-muted-foreground px-2 py-0.5 rounded">
              مخفي
            </span>
          </div>
          <Button
            size="icon"
            variant="ghost"
            onClick={() => toggleSection(chartId)}
            className="h-7 w-7 text-muted-foreground hover:text-foreground"
          >
            <EyeOff className="h-3.5 w-3.5" />
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div
      className={`group bg-[hsl(var(--surface))] border border-[hsl(var(--border))] rounded-lg overflow-hidden ${
        fullWidth ? "col-span-full" : ""
      }`}
    >
      <div className="px-6 py-3 flex items-center justify-between border-b border-[hsl(var(--border))]">
        <h3 className="text-foreground font-bold text-sm">{title}</h3>
        <div className="flex items-center gap-1">
          <Button
            size="icon"
            variant="ghost"
            onClick={() => toggleSection(chartId)}
            className="h-7 w-7 text-muted-foreground hover:text-foreground opacity-0 group-hover:opacity-100 transition-opacity"
          >
            <Eye className="h-3.5 w-3.5" />
          </Button>
          <Button
            size="sm"
            variant="ghost"
            className="text-gold hover:text-gold/80 hover:bg-[hsl(var(--surface-hover))] text-xs opacity-0 group-hover:opacity-100 transition-opacity"
            onClick={handleRegenerate}
            disabled={isRegenerating}
          >
            {isRegenerating ? "جاري التحليل..." : "إعادة التحليل ↻"}
          </Button>
        </div>
      </div>
      <div className="p-6">
        {/* eslint-disable-next-line @next/next/no-img-element */}
        <img src={image} alt={title} className="w-full rounded-lg" />
        <div className="mt-4 p-4 bg-[hsl(var(--muted))] rounded-lg">
          {isRegenerating ? (
            <div className="space-y-2">
              <Skeleton className="h-4 w-full bg-[hsl(var(--surface-hover))]" />
              <Skeleton className="h-4 w-3/4 bg-[hsl(var(--surface-hover))]" />
            </div>
          ) : description ? (
            <EditableText sectionId={aiSection} originalText={description} />
          ) : (
            <p className="text-sm text-[hsl(var(--text-muted))] italic">
              لم يتم تفعيل التحليل الذكي
            </p>
          )}
        </div>
      </div>
    </div>
  );
}
