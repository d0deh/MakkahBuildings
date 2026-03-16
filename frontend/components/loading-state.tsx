import { Skeleton } from "@/components/ui/skeleton";

interface LoadingStateProps {
  message: string;
  progress?: number;
}

export function LoadingState({ message, progress }: LoadingStateProps) {
  return (
    <div className="flex flex-col items-center justify-center py-20 gap-6">
      <div className="relative">
        <div className="w-20 h-20 rounded-full border-4 border-[hsl(var(--muted))] border-t-gold animate-spin" />
      </div>
      <p className="text-lg text-muted-foreground font-bold">{message}</p>
      {progress !== undefined && (
        <div className="w-64 h-2 bg-[hsl(var(--muted))] rounded-full overflow-hidden">
          <div
            className="h-full bg-gold rounded-full transition-all duration-500"
            style={{ width: `${progress}%` }}
          />
        </div>
      )}
    </div>
  );
}

/* ── Progress banner shown at top of dashboard while loading ── */

interface ProgressStep {
  id: string;
  label: string;
  status: "done" | "active" | "pending";
}

interface ProgressBannerProps {
  steps: ProgressStep[];
}

export function ProgressBanner({ steps }: ProgressBannerProps) {
  const active = steps.find((s) => s.status === "active");
  if (!active) return null;

  return (
    <div className="bg-[hsl(var(--surface))] border border-gold/20 rounded-lg p-4 flex items-center gap-4">
      <div className="w-5 h-5 rounded-full border-2 border-gold border-t-transparent animate-spin shrink-0" />
      <div className="flex-1 min-w-0">
        <p className="text-sm font-bold text-foreground">{active.label}</p>
        <div className="flex items-center gap-2 mt-2">
          {steps.map((step) => (
            <div key={step.id} className="flex items-center gap-1.5">
              <div
                className={`w-2 h-2 rounded-full shrink-0 ${
                  step.status === "done"
                    ? "bg-status-good"
                    : step.status === "active"
                    ? "bg-gold animate-pulse"
                    : "bg-[hsl(var(--muted))]"
                }`}
              />
              <span
                className={`text-xs ${
                  step.status === "done"
                    ? "text-status-good"
                    : step.status === "active"
                    ? "text-gold"
                    : "text-muted-foreground"
                }`}
              >
                {step.label}
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

/* ── Chart skeleton placeholder ── */

export function ChartSkeleton({ fullWidth }: { fullWidth?: boolean }) {
  return (
    <div
      className={`bg-[hsl(var(--surface))] border border-[hsl(var(--border))] rounded-lg overflow-hidden ${
        fullWidth ? "col-span-full" : ""
      }`}
    >
      <div className="px-6 py-3 border-b border-[hsl(var(--border))]">
        <Skeleton className="h-5 w-32 bg-[hsl(var(--muted))]" />
      </div>
      <div className="p-6 space-y-4">
        <Skeleton className="h-64 w-full rounded-lg bg-[hsl(var(--muted))]" />
        <Skeleton className="h-16 w-full rounded-lg bg-[hsl(var(--muted))]" />
      </div>
    </div>
  );
}

export function DashboardSkeleton() {
  return (
    <div className="space-y-6 p-6">
      {/* Stats skeleton */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
        {[...Array(4)].map((_, i) => (
          <div key={i} className="space-y-2">
            <Skeleton className="h-10 w-24 bg-[hsl(var(--muted))]" />
            <Skeleton className="h-4 w-32 bg-[hsl(var(--muted))]" />
          </div>
        ))}
      </div>
      {/* Chart skeletons */}
      {[...Array(3)].map((_, i) => (
        <div key={i} className="bg-[hsl(var(--surface))] border border-[hsl(var(--border))] rounded-lg overflow-hidden">
          <Skeleton className="h-10 w-full bg-[hsl(var(--muted))]" />
          <div className="p-6 space-y-4">
            <Skeleton className="h-64 w-full rounded-lg bg-[hsl(var(--muted))]" />
            <Skeleton className="h-16 w-full rounded-lg bg-[hsl(var(--muted))]" />
          </div>
        </div>
      ))}
    </div>
  );
}
