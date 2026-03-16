"use client";

import { useState } from "react";
import { X, Download } from "lucide-react";
import { Button } from "@/components/ui/button";
import { exportPptx } from "@/lib/api";
import { useDashboardStore } from "@/lib/store";

interface ExportModalProps {
  sessionId: string;
  open: boolean;
  onClose: () => void;
}

const ALL_SECTIONS = [
  { id: "analysis", label: "الملخص التنفيذي" },
  { id: "presence", label: "وجود المباني" },
  { id: "building_type", label: "أنواع المباني" },
  { id: "building_condition", label: "حالة المباني" },
  { id: "construction", label: "أساليب الإنشاء" },
  { id: "finish", label: "التشطيب الخارجي" },
  { id: "floors", label: "توزيع الطوابق" },
  { id: "building_usage", label: "استخدامات المباني" },
  { id: "occupancy", label: "الإشغال" },
  { id: "road_type", label: "نوع الطريق" },
  { id: "road_width", label: "عرض الطريق" },
  { id: "lighting", label: "الإنارة" },
  { id: "parking", label: "المواقف" },
  { id: "map", label: "الخريطة" },
  { id: "insights", label: "الرؤى المتقاطعة" },
  { id: "recommendations", label: "التوصيات" },
];

export function ExportModal({ sessionId, open, onClose }: ExportModalProps) {
  const [selected, setSelected] = useState<Set<string>>(
    new Set(ALL_SECTIONS.map((s) => s.id))
  );
  const [exporting, setExporting] = useState(false);
  const { editedTexts, pinnedItems, hiddenSections } = useDashboardStore();

  if (!open) return null;

  const toggle = (id: string) => {
    const next = new Set(selected);
    if (next.has(id)) next.delete(id);
    else next.add(id);
    setSelected(next);
  };

  const handleExport = async () => {
    setExporting(true);
    try {
      // Exclude hidden sections
      const sections = [...selected].filter((s) => !hiddenSections.has(s));
      const blob = await exportPptx(
        sessionId,
        sections,
        editedTexts,
        pinnedItems
      );
      // Trigger download
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `report_${sessionId}.pptx`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
      onClose();
    } catch (err) {
      console.error("Export failed:", err);
    } finally {
      setExporting(false);
    }
  };

  return (
    <div className="fixed inset-0 z-[60] flex items-center justify-center bg-black/60">
      <div className="bg-[hsl(var(--surface))] border border-[hsl(var(--border))] rounded-xl w-full max-w-md mx-4 shadow-2xl">
        {/* Header */}
        <div className="px-6 py-4 border-b border-[hsl(var(--border))] flex items-center justify-between">
          <h3 className="text-foreground font-bold">تصدير التقرير</h3>
          <Button
            size="icon"
            variant="ghost"
            onClick={onClose}
            className="h-8 w-8"
          >
            <X className="h-4 w-4" />
          </Button>
        </div>

        {/* Section checklist */}
        <div className="p-6 max-h-[400px] overflow-y-auto space-y-2">
          {ALL_SECTIONS.map((section) => (
            <label
              key={section.id}
              className="flex items-center gap-3 p-2 rounded-lg hover:bg-[hsl(var(--surface-hover))] cursor-pointer transition-colors"
            >
              <input
                type="checkbox"
                checked={selected.has(section.id)}
                onChange={() => toggle(section.id)}
                className="w-4 h-4 accent-[#C9A84C] rounded"
              />
              <span
                className={`text-sm ${
                  hiddenSections.has(section.id)
                    ? "text-muted-foreground line-through"
                    : "text-foreground"
                }`}
              >
                {section.label}
                {hiddenSections.has(section.id) && (
                  <span className="text-xs text-muted-foreground mr-2">
                    (مخفي)
                  </span>
                )}
              </span>
            </label>
          ))}
        </div>

        {/* Footer */}
        <div className="px-6 py-4 border-t border-[hsl(var(--border))] flex gap-3">
          <Button
            onClick={handleExport}
            disabled={exporting || selected.size === 0}
            className="flex-1 bg-gold hover:bg-gold-dark text-background font-bold"
          >
            {exporting ? (
              "جاري التصدير..."
            ) : (
              <>
                <Download className="h-4 w-4 ml-2" />
                تصدير PPTX
              </>
            )}
          </Button>
          <Button variant="ghost" onClick={onClose} className="text-muted-foreground">
            إلغاء
          </Button>
        </div>
      </div>
    </div>
  );
}
