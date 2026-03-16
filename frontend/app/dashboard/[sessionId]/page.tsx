"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { MessageSquare, Download } from "lucide-react";
import { StatsCards } from "@/components/stats-cards";
import { ChartSection } from "@/components/chart-section";
import { AiNarrativeSection } from "@/components/ai-narrative-section";
import { DashboardSkeleton, ProgressBanner, ChartSkeleton } from "@/components/loading-state";
import { ChatPanel } from "@/components/chat/chat-panel";
import { ExportModal } from "@/components/export/export-modal";
import { MarkdownContent } from "@/components/markdown-content";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { getStats, getCharts, getAiSection, getValidation } from "@/lib/api";
import { useDashboardStore } from "@/lib/store";
import type { AreaStats, ChartData, AiContent } from "@/lib/types";

const CHART_AI_MAP: Record<string, string> = {
  presence: "desc_presence",
  building_type: "desc_building_type",
  building_condition: "desc_building_condition",
  construction: "desc_construction",
  finish: "desc_finish",
  floors: "desc_floors",
  building_usage: "desc_building_usage",
  occupancy: "desc_occupancy",
  road_type: "desc_road_type",
  road_width: "desc_road_width",
  lighting: "desc_lighting",
  parking: "desc_parking",
  compliance: "desc_compliance",
  map: "analysis",
};

const FULL_WIDTH_CHARTS = ["presence", "building_condition", "building_usage", "map"];

export default function DashboardPage() {
  const params = useParams();
  const sessionId = params.sessionId as string;

  const [stats, setStats] = useState<AreaStats | null>(null);
  const [charts, setCharts] = useState<ChartData[]>([]);
  const [aiContent, setAiContent] = useState<AiContent>({});
  const [loading, setLoading] = useState(true);
  const [chartsLoading, setChartsLoading] = useState(true);
  const [aiLoading, setAiLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [exportOpen, setExportOpen] = useState(false);
  const [validationWarnings, setValidationWarnings] = useState<string[]>([]);
  const [allDone, setAllDone] = useState(false);

  const { chatOpen, toggleChat, pinnedItems } = useDashboardStore();

  useEffect(() => {
    // Load stats first (fast), then charts + AI in parallel
    async function loadCore() {
      try {
        const statsData = await getStats(sessionId);
        setStats(statsData);
        setLoading(false);

        // Fetch validation warnings
        getValidation(sessionId)
          .then((v) => setValidationWarnings(v.warnings || []))
          .catch(() => {});

        // Fire charts and AI loading in parallel
        getCharts(sessionId)
          .then((chartsData) => setCharts(chartsData.charts))
          .catch((err) => console.error("Charts load failed:", err))
          .finally(() => setChartsLoading(false));

        loadAiProgressively();
      } catch (err) {
        setError(err instanceof Error ? err.message : "خطأ في تحميل البيانات");
        setLoading(false);
      }
    }

    async function loadAiProgressively() {
      setAiLoading(true);
      try {
        // Stage 1: Executive summary first
        try {
          const result = await getAiSection(sessionId, "analysis");
          if (result.text) {
            setAiContent((prev) => ({ ...prev, analysis: result.text }));
          }
        } catch {
          // Skip failed section
        }

        // Stage 2: All chart descriptions in parallel
        const descSections = Object.values(CHART_AI_MAP).filter(
          (s) => s !== "analysis"
        );
        const uniqueDescs = [...new Set(descSections)];
        await Promise.all(
          uniqueDescs.map(async (section) => {
            try {
              const result = await getAiSection(sessionId, section);
              if (result.text) {
                setAiContent((prev) => ({ ...prev, [section]: result.text }));
              }
            } catch {
              // Skip failed section
            }
          })
        );

        // Stage 3: Insights + recommendations in parallel
        await Promise.all(
          ["insights", "recommendations"].map(async (section) => {
            try {
              const result = await getAiSection(sessionId, section);
              if (result.text) {
                setAiContent((prev) => ({ ...prev, [section]: result.text }));
              }
            } catch {
              // Skip failed section
            }
          })
        );
      } finally {
        setAiLoading(false);
      }
    }

    loadCore();
  }, [sessionId]);

  // Show "جاهز" banner briefly when loading completes
  useEffect(() => {
    const done = !chartsLoading && !aiLoading && stats !== null;
    if (done) {
      setAllDone(true);
      const timer = setTimeout(() => setAllDone(false), 2000);
      return () => clearTimeout(timer);
    }
  }, [chartsLoading, aiLoading, stats]);

  if (loading) return <DashboardSkeleton />;
  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center space-y-4">
          <p className="text-2xl text-status-danger font-bold">{error}</p>
          <a href="/" className="text-gold hover:underline">
            العودة للصفحة الرئيسية
          </a>
        </div>
      </div>
    );
  }

  if (!stats) return null;

  // Progress steps for the banner (5-step)
  const isLoading = chartsLoading || aiLoading;
  const progressSteps = [
    { id: "data", label: "قراءة البيانات", status: "done" as const },
    { id: "validation", label: "التحقق", status: "done" as const },
    {
      id: "charts",
      label: "الرسوم البيانية",
      status: chartsLoading ? ("active" as const) : ("done" as const),
    },
    {
      id: "ai",
      label: "التحليل الذكي",
      status: aiLoading
        ? ("active" as const)
        : chartsLoading
          ? ("pending" as const)
          : ("done" as const),
    },
    {
      id: "ready",
      label: "جاهز",
      status: isLoading ? ("pending" as const) : ("done" as const),
    },
  ];

  // Split charts into full-width and grid
  const fullWidthCharts = charts.filter((c) => FULL_WIDTH_CHARTS.includes(c.id));
  const gridCharts = charts.filter((c) => !FULL_WIDTH_CHARTS.includes(c.id));
  const mapChart = fullWidthCharts.find((c) => c.id === "map");
  const topFullWidth = fullWidthCharts.filter((c) => c.id !== "map");

  return (
    <div className="min-h-screen">
      {/* Header */}
      <header className="border-b border-[hsl(var(--border))] py-4 px-8 sticky top-0 z-40 bg-background/80 backdrop-blur-sm">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <div>
            <h1 className="text-lg font-bold text-foreground">
              مولد التقارير العمرانية
            </h1>
            <p className="text-muted-foreground text-sm">
              {stats.area_name} — {stats.total_records} سجل
            </p>
          </div>
          <div className="flex items-center gap-3">
            {isLoading && (
              <Badge
                variant="outline"
                className="text-gold border-gold/30 animate-pulse"
              >
                {chartsLoading ? "جاري تحميل الرسوم..." : "جاري التحليل الذكي..."}
              </Badge>
            )}
            <Button
              size="sm"
              variant="ghost"
              onClick={toggleChat}
              className={`text-muted-foreground hover:text-foreground ${chatOpen ? "text-gold" : ""}`}
              title="محادثة مع البيانات"
            >
              <MessageSquare className="h-4 w-4" />
            </Button>
            <Button
              size="sm"
              variant="ghost"
              onClick={() => setExportOpen(true)}
              className="text-muted-foreground hover:text-foreground"
              title="تصدير PPTX"
            >
              <Download className="h-4 w-4" />
            </Button>
            <a href="/">
              <Badge
                variant="outline"
                className="text-muted-foreground border-[hsl(var(--border))] hover:bg-[hsl(var(--surface-hover))] cursor-pointer"
              >
                تحليل جديد
              </Badge>
            </a>
          </div>
        </div>
      </header>

      {/* Chat Sidebar */}
      <ChatPanel sessionId={sessionId} />

      {/* Dashboard Content */}
      <main
        className={`max-w-7xl mx-auto p-6 space-y-10 transition-all duration-300 ${
          chatOpen ? "mr-[400px] max-md:mr-0" : ""
        }`}
      >
        {/* Section 1: Hero Stats */}
        <section>
          <StatsCards stats={stats} />
        </section>

        {/* Validation Warnings */}
        {validationWarnings.length > 0 && (
          <div className="bg-[hsl(var(--surface))] border border-status-warning/30 rounded-lg p-4">
            <p className="text-sm font-bold text-status-warning mb-2">تنبيهات التحقق</p>
            <ul className="space-y-1">
              {validationWarnings.map((w, i) => (
                <li key={i} className="text-xs text-muted-foreground flex items-center gap-2">
                  <span className="w-1.5 h-1.5 rounded-full bg-status-warning shrink-0" />
                  {w}
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Progress Banner */}
        {isLoading && <ProgressBanner steps={progressSteps} />}
        {allDone && !isLoading && (
          <div className="bg-[hsl(var(--surface))] border border-status-good/30 rounded-lg p-4 flex items-center gap-3">
            <div className="w-5 h-5 rounded-full bg-status-good flex items-center justify-center shrink-0">
              <svg className="w-3 h-3 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={3}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
              </svg>
            </div>
            <p className="text-sm font-bold text-status-good">جاهز</p>
          </div>
        )}

        {/* Section 2: Executive Summary (AI) */}
        <AiNarrativeSection
          sessionId={sessionId}
          title="الملخص التنفيذي"
          content={aiContent.analysis || null}
          section="analysis"
        />

        {/* Section 3: Full-width Charts */}
        <section className="space-y-6">
          {chartsLoading ? (
            <>
              <ChartSkeleton fullWidth />
              <ChartSkeleton fullWidth />
            </>
          ) : (
            topFullWidth.map((chart) => (
              <ChartSection
                key={chart.id}
                sessionId={sessionId}
                chartId={chart.id}
                title={chart.title}
                image={chart.image}
                aiDescription={aiContent[CHART_AI_MAP[chart.id]] || null}
                aiSection={CHART_AI_MAP[chart.id] || `desc_${chart.id}`}
                fullWidth
              />
            ))
          )}
        </section>

        {/* Section 4: Grid Charts */}
        <section>
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {chartsLoading ? (
              <>
                <ChartSkeleton />
                <ChartSkeleton />
                <ChartSkeleton />
                <ChartSkeleton />
              </>
            ) : (
              gridCharts.map((chart) => (
                <ChartSection
                  key={chart.id}
                  sessionId={sessionId}
                  chartId={chart.id}
                  title={chart.title}
                  image={chart.image}
                  aiDescription={aiContent[CHART_AI_MAP[chart.id]] || null}
                  aiSection={CHART_AI_MAP[chart.id] || `desc_${chart.id}`}
                />
              ))
            )}
          </div>
        </section>

        {/* Section 5: Map */}
        {chartsLoading ? (
          <ChartSkeleton fullWidth />
        ) : mapChart ? (
          <ChartSection
            sessionId={sessionId}
            chartId={mapChart.id}
            title={mapChart.title}
            image={mapChart.image}
            aiDescription={aiContent[CHART_AI_MAP[mapChart.id]] || null}
            aiSection={CHART_AI_MAP[mapChart.id] || "analysis"}
            fullWidth
          />
        ) : null}

        {/* Section 6: Cross-Data Insights */}
        <AiNarrativeSection
          sessionId={sessionId}
          title="رؤى متقاطعة من البيانات"
          content={aiContent.insights || null}
          section="insights"
        />

        {/* Section 7: Recommendations */}
        <AiNarrativeSection
          sessionId={sessionId}
          title="التوصيات"
          content={aiContent.recommendations || null}
          section="recommendations"
        />

        {/* Section 8: Pinned Items */}
        {pinnedItems.length > 0 && (
          <section className="space-y-4">
            <h2 className="text-foreground font-bold text-sm px-2">
              رؤى إضافية
            </h2>
            {pinnedItems.map((item) => (
              <div
                key={item.message_id}
                className="bg-[hsl(var(--surface))] border border-gold/20 rounded-lg p-6"
              >
                <MarkdownContent content={item.text} />
              </div>
            ))}
          </section>
        )}
      </main>

      {/* Export Modal */}
      <ExportModal
        sessionId={sessionId}
        open={exportOpen}
        onClose={() => setExportOpen(false)}
      />

      {/* Footer */}
      <footer className="border-t border-[hsl(var(--border))] text-muted-foreground text-center py-4 text-sm mt-12">
        مولد التقارير العمرانية v0.4
      </footer>
    </div>
  );
}
