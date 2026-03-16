"use client";

import { useState } from "react";
import { Eye, EyeOff } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import { EditableText } from "@/components/editable-text";
import { regenerateSection } from "@/lib/api";
import { useDashboardStore } from "@/lib/store";

interface AiNarrativeSectionProps {
  sessionId: string;
  title: string;
  content: string | null;
  section: string;
}

export function AiNarrativeSection({
  sessionId,
  title,
  content,
  section,
}: AiNarrativeSectionProps) {
  const [regeneratedText, setRegeneratedText] = useState<string | null>(null);
  const [isRegenerating, setIsRegenerating] = useState(false);
  const { hiddenSections, toggleSection } = useDashboardStore();

  const isHidden = hiddenSections.has(section);
  const text = regeneratedText ?? content;

  const handleRegenerate = async () => {
    setIsRegenerating(true);
    try {
      const result = await regenerateSection(sessionId, section);
      setRegeneratedText(result.text);
    } catch (err) {
      console.error("Regenerate failed:", err);
    } finally {
      setIsRegenerating(false);
    }
  };

  if (isHidden) {
    return (
      <div className="bg-[hsl(var(--surface))] border border-[hsl(var(--border))] rounded-lg overflow-hidden opacity-50">
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
            onClick={() => toggleSection(section)}
            className="h-7 w-7 text-muted-foreground hover:text-foreground"
          >
            <EyeOff className="h-3.5 w-3.5" />
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className="group bg-[hsl(var(--surface))] border border-[hsl(var(--border))] rounded-lg overflow-hidden">
      <div className="px-6 py-3 flex items-center justify-between border-b border-[hsl(var(--border))]">
        <h3 className="text-foreground font-bold text-sm">{title}</h3>
        <div className="flex items-center gap-1">
          <Button
            size="icon"
            variant="ghost"
            onClick={() => toggleSection(section)}
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
        {isRegenerating ? (
          <div className="space-y-3">
            <Skeleton className="h-4 w-full bg-[hsl(var(--surface-hover))]" />
            <Skeleton className="h-4 w-5/6 bg-[hsl(var(--surface-hover))]" />
            <Skeleton className="h-4 w-4/5 bg-[hsl(var(--surface-hover))]" />
            <Skeleton className="h-4 w-full bg-[hsl(var(--surface-hover))]" />
            <Skeleton className="h-4 w-3/4 bg-[hsl(var(--surface-hover))]" />
          </div>
        ) : text ? (
          <EditableText sectionId={section} originalText={text} />
        ) : (
          <p className="text-[hsl(var(--text-muted))] italic text-sm">
            لم يتم تفعيل التحليل الذكي
          </p>
        )}
      </div>
    </div>
  );
}
