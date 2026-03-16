"use client";

import { useState } from "react";
import { Pencil, Check, X, RotateCcw } from "lucide-react";
import { Button } from "@/components/ui/button";
import { MarkdownContent } from "@/components/markdown-content";
import { useDashboardStore } from "@/lib/store";

interface EditableTextProps {
  sectionId: string;
  originalText: string;
}

export function EditableText({ sectionId, originalText }: EditableTextProps) {
  const { editedTexts, setEditedText, clearEditedText } = useDashboardStore();
  const [editing, setEditing] = useState(false);
  const [draft, setDraft] = useState("");

  const displayText = editedTexts[sectionId] ?? originalText;
  const isEdited = sectionId in editedTexts;

  const startEdit = () => {
    setDraft(displayText);
    setEditing(true);
  };

  const save = () => {
    setEditedText(sectionId, draft);
    setEditing(false);
  };

  const cancel = () => {
    setEditing(false);
  };

  const restore = () => {
    clearEditedText(sectionId);
    setEditing(false);
  };

  if (editing) {
    return (
      <div className="space-y-3">
        <textarea
          value={draft}
          onChange={(e) => setDraft(e.target.value)}
          rows={8}
          className="w-full bg-[hsl(var(--muted))] border border-gold/30 rounded-lg px-4 py-3 text-sm text-foreground resize-y focus:outline-none focus:ring-1 focus:ring-gold/50"
          dir="rtl"
        />
        <div className="flex gap-2">
          <Button
            size="sm"
            onClick={save}
            className="bg-gold hover:bg-gold-dark text-background text-xs"
          >
            <Check className="h-3 w-3 ml-1" />
            حفظ
          </Button>
          <Button
            size="sm"
            variant="ghost"
            onClick={cancel}
            className="text-muted-foreground text-xs"
          >
            <X className="h-3 w-3 ml-1" />
            إلغاء
          </Button>
          {isEdited && (
            <Button
              size="sm"
              variant="ghost"
              onClick={restore}
              className="text-gold text-xs mr-auto"
            >
              <RotateCcw className="h-3 w-3 ml-1" />
              استعادة الأصلي
            </Button>
          )}
        </div>
      </div>
    );
  }

  return (
    <div className="relative group/edit">
      <MarkdownContent content={displayText} />
      <Button
        size="icon"
        variant="ghost"
        onClick={startEdit}
        className="absolute top-0 left-0 h-7 w-7 opacity-0 group-hover/edit:opacity-100 transition-opacity text-gold hover:text-gold/80 hover:bg-[hsl(var(--surface-hover))]"
        title="تعديل النص"
      >
        <Pencil className="h-3.5 w-3.5" />
      </Button>
      {isEdited && (
        <span className="absolute top-0 left-8 text-[10px] text-gold/60">
          معدّل
        </span>
      )}
    </div>
  );
}
