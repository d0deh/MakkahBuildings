"use client";

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  Cell,
} from "recharts";
import type { ChartSpec } from "@/lib/types";

const DEFAULT_COLOR = "#3B82AA";

interface BarChartComponentProps {
  spec: ChartSpec;
}

export function BarChartComponent({ spec }: BarChartComponentProps) {
  const { data, colorMap } = spec;

  return (
    <ResponsiveContainer width="100%" height={300}>
      <BarChart
        data={data}
        layout="vertical"
        margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
      >
        <XAxis type="number" stroke="hsl(213 10% 47%)" fontSize={12} />
        <YAxis
          type="category"
          dataKey="name"
          stroke="hsl(213 10% 47%)"
          fontSize={12}
          width={120}
          tick={{ fill: "hsl(210 29% 90%)" }}
        />
        <Tooltip
          contentStyle={{
            backgroundColor: "hsl(215 25% 11%)",
            border: "1px solid hsl(215 14% 21%)",
            borderRadius: "8px",
            color: "hsl(210 29% 90%)",
            direction: "rtl",
          }}
          labelStyle={{ color: "#C9A84C", fontWeight: "bold" }}
          cursor={{ fill: "hsl(215 14% 14% / 0.5)" }}
        />
        <Bar dataKey="value" radius={[0, 4, 4, 0]} animationDuration={800}>
          {data.map((entry, index) => (
            <Cell
              key={index}
              fill={colorMap?.[entry.name] || DEFAULT_COLOR}
            />
          ))}
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  );
}
