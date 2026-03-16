"use client";

import { useEffect, useRef, useState } from "react";
import { BarChartComponent } from "./bar-chart";
import { PieChartComponent } from "./pie-chart";
import type { ChartSpec } from "@/lib/types";

interface ChartWrapperProps {
  spec: ChartSpec;
}

export function ChartWrapper({ spec }: ChartWrapperProps) {
  const ref = useRef<HTMLDivElement>(null);
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    const el = ref.current;
    if (!el) return;

    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setVisible(true);
          observer.disconnect();
        }
      },
      { threshold: 0.1 }
    );

    observer.observe(el);
    return () => observer.disconnect();
  }, []);

  return (
    <div
      ref={ref}
      className={`transition-all duration-700 ${
        visible ? "opacity-100 translate-y-0" : "opacity-0 translate-y-4"
      }`}
    >
      {visible && (
        <>
          {spec.type === "bar" && <BarChartComponent spec={spec} />}
          {spec.type === "pie" && <PieChartComponent spec={spec} />}
        </>
      )}
    </div>
  );
}
