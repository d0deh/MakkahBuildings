"use client";

import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import type { Components } from "react-markdown";

interface MarkdownContentProps {
  content: string;
}

function highlightNumbers(text: string) {
  const parts = text.split(/(\d+[\d,.%]*)/);
  return parts.map((part, i) =>
    /^\d+[\d,.%]*$/.test(part) ? (
      <span key={i} className="text-gold font-bold">
        {part}
      </span>
    ) : (
      <span key={i}>{part}</span>
    )
  );
}

const components: Components = {
  h2: ({ children }) => (
    <h2 className="text-lg font-bold text-foreground mb-3 mt-4 first:mt-0">
      {children}
    </h2>
  ),
  h3: ({ children }) => (
    <h3 className="text-base font-bold text-foreground mb-2 mt-3 first:mt-0">
      {children}
    </h3>
  ),
  p: ({ children }) => (
    <p className="text-sm text-foreground/80 leading-relaxed mb-3">
      {children}
    </p>
  ),
  strong: ({ children }) => (
    <span className="text-foreground font-bold">{children}</span>
  ),
  ul: ({ children }) => <ul className="space-y-2 mb-3">{children}</ul>,
  ol: ({ children }) => <ol className="space-y-2 mb-3">{children}</ol>,
  li: ({ children, ...props }) => {
    // Check if this is an ordered list item
    const isOrdered =
      (props as { node?: { parentNode?: { tagName?: string } } }).node
        ?.parentNode?.tagName === "ol";
    if (isOrdered) {
      const index = (props as { index?: number }).index ?? 0;
      return (
        <div className="flex items-start gap-3">
          <span className="w-6 h-6 rounded-full bg-gold/20 text-gold text-xs font-bold flex items-center justify-center shrink-0 mt-0.5">
            {index + 1}
          </span>
          <div className="text-sm text-foreground/80 leading-relaxed flex-1">
            {children}
          </div>
        </div>
      );
    }
    return (
      <div className="flex items-start gap-3">
        <span className="w-2 h-2 rounded-full bg-gold mt-2 shrink-0" />
        <div className="text-sm text-foreground/80 leading-relaxed flex-1">
          {children}
        </div>
      </div>
    );
  },
  // Custom text renderer to highlight numbers
  text: ({ children }) => {
    if (typeof children === "string") {
      return <>{highlightNumbers(children)}</>;
    }
    return <>{children}</>;
  },
};

export function MarkdownContent({ content }: MarkdownContentProps) {
  // Pre-process: convert bullet points (•) to markdown list items
  const processed = content
    .split("\n")
    .map((line) => {
      const trimmed = line.trim();
      if (trimmed.startsWith("•")) {
        return `- ${trimmed.slice(1).trim()}`;
      }
      return line;
    })
    .join("\n");

  return (
    <ReactMarkdown remarkPlugins={[remarkGfm]} components={components}>
      {processed}
    </ReactMarkdown>
  );
}
