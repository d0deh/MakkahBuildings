"use client";

import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from "recharts";
import type { PieLabelRenderProps } from "recharts";
import type { ChartSpec } from "@/lib/types";

const COLORS = [
  "#3B82AA",
  "#C9A84C",
  "#4A90D9",
  "#E67E22",
  "#27AE60",
  "#8E44AD",
  "#C0392B",
  "#16A085",
];

interface PieChartComponentProps {
  spec: ChartSpec;
}

const renderCustomLabel = (props: PieLabelRenderProps) => {
  const cx = Number(props.cx ?? 0);
  const cy = Number(props.cy ?? 0);
  const midAngle = Number(props.midAngle ?? 0);
  const innerRadius = Number(props.innerRadius ?? 0);
  const outerRadius = Number(props.outerRadius ?? 0);
  const percent = Number(props.percent ?? 0);
  const name = String(props.name ?? "");

  const RADIAN = Math.PI / 180;
  const radius = innerRadius + (outerRadius - innerRadius) * 1.4;
  const x = cx + radius * Math.cos(-midAngle * RADIAN);
  const y = cy + radius * Math.sin(-midAngle * RADIAN);

  if (percent < 0.05) return null;

  return (
    <text
      x={x}
      y={y}
      fill="hsl(210 29% 90%)"
      textAnchor={x > cx ? "start" : "end"}
      dominantBaseline="central"
      fontSize={12}
    >
      {name} ({(percent * 100).toFixed(0)}%)
    </text>
  );
};

export function PieChartComponent({ spec }: PieChartComponentProps) {
  const { data } = spec;
  const filteredData = data.filter((d) => d.value > 0);

  return (
    <ResponsiveContainer width="100%" height={300}>
      <PieChart>
        <Pie
          data={filteredData}
          cx="50%"
          cy="50%"
          innerRadius={60}
          outerRadius={100}
          dataKey="value"
          label={renderCustomLabel}
          animationDuration={800}
        >
          {filteredData.map((_, index) => (
            <Cell key={index} fill={COLORS[index % COLORS.length]} />
          ))}
        </Pie>
        <Tooltip
          contentStyle={{
            backgroundColor: "hsl(215 25% 11%)",
            border: "1px solid hsl(215 14% 21%)",
            borderRadius: "8px",
            color: "hsl(210 29% 90%)",
            direction: "rtl",
          }}
          labelStyle={{ color: "#C9A84C", fontWeight: "bold" }}
        />
        <Legend
          wrapperStyle={{ color: "hsl(210 29% 90%)", fontSize: 12 }}
        />
      </PieChart>
    </ResponsiveContainer>
  );
}
