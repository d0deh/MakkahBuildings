"use client";

import { Pin } from "lucide-react";
import { Button } from "@/components/ui/button";
import { MarkdownContent } from "@/components/markdown-content";
import { BarChartComponent } from "@/components/charts/bar-chart";
import { PieChartComponent } from "@/components/charts/pie-chart";
import type { ChatMessage, ChartSpec } from "@/lib/types";

interface MessageSegment {
  type: "text" | "chart";
  content?: string;
  spec?: ChartSpec;
}

function isValidChartSpec(obj: unknown): obj is ChartSpec {
  if (!obj || typeof obj !== "object") return false;
  const o = obj as Record<string, unknown>;
  if (o.type !== "bar" && o.type !== "pie") return false;
  if (typeof o.title !== "string") return false;
  if (!Array.isArray(o.data)) return false;
  return o.data.every(
    (d: unknown) =>
      d &&
      typeof d === "object" &&
      typeof (d as Record<string, unknown>).name === "string" &&
      typeof (d as Record<string, unknown>).value === "number"
  );
}

function parseMessageContent(content: string): MessageSegment[] {
  const segments: MessageSegment[] = [];
  const regex = /<chart>([\s\S]*?)<\/chart>/g;
  let lastIndex = 0;
  let match: RegExpExecArray | null;

  while ((match = regex.exec(content)) !== null) {
    // Text before this chart block
    if (match.index > lastIndex) {
      const text = content.slice(lastIndex, match.index).trim();
      if (text) segments.push({ type: "text", content: text });
    }

    // Try to parse chart JSON
    try {
      const parsed = JSON.parse(match[1]);
      if (isValidChartSpec(parsed)) {
        segments.push({ type: "chart", spec: parsed });
      } else {
        // Invalid chart spec — render as text
        segments.push({ type: "text", content: match[0] });
      }
    } catch {
      // JSON parse failed — render as text
      segments.push({ type: "text", content: match[0] });
    }

    lastIndex = match.index + match[0].length;
  }

  // Remaining text after last chart
  if (lastIndex < content.length) {
    const text = content.slice(lastIndex).trim();
    if (text) segments.push({ type: "text", content: text });
  }

  // If no chart blocks found, return the whole thing as text
  if (segments.length === 0) {
    segments.push({ type: "text", content });
  }

  return segments;
}

interface ChatMessageComponentProps {
  message: ChatMessage;
  onPin?: (message: ChatMessage) => void;
}

export function ChatMessageComponent({
  message,
  onPin,
}: ChatMessageComponentProps) {
  const isUser = message.role === "user";

  if (isUser) {
    return (
      <div className="flex justify-end mb-3 animate-in slide-in-from-bottom-2 duration-300">
        <div className="max-w-[80%] rounded-2xl rounded-br-sm px-4 py-2.5 text-sm bg-gold/15 border border-gold/25 text-foreground">
          <p className="leading-relaxed">{message.content}</p>
        </div>
      </div>
    );
  }

  // Assistant message — parse for chart blocks
  const segments = parseMessageContent(message.content);

  return (
    <div className="mb-4 animate-in slide-in-from-bottom-2 duration-300">
      <div className="relative group/msg">
        {segments.map((segment, i) => {
          if (segment.type === "chart" && segment.spec) {
            return (
              <div
                key={i}
                className="my-3 bg-[hsl(var(--surface))] border border-[hsl(var(--border))] rounded-lg p-4"
              >
                <p className="text-sm font-bold text-gold mb-2">
                  {segment.spec.title}
                </p>
                {segment.spec.type === "pie" ? (
                  <PieChartComponent spec={segment.spec} />
                ) : (
                  <BarChartComponent spec={segment.spec} />
                )}
              </div>
            );
          }
          return (
            <div key={i} className="text-sm">
              <MarkdownContent content={segment.content || ""} />
            </div>
          );
        })}
        {onPin && (
          <Button
            size="icon"
            variant="ghost"
            className="absolute top-0 left-0 h-7 w-7 text-muted-foreground hover:text-gold transition-colors"
            onClick={() => onPin(message)}
            title="تثبيت في التقرير"
          >
            <Pin className="h-3.5 w-3.5" />
          </Button>
        )}
      </div>
    </div>
  );
}
