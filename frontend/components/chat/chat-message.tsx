"use client";

import { Pin } from "lucide-react";
import { Button } from "@/components/ui/button";
import { MarkdownContent } from "@/components/markdown-content";
import type { ChatMessage } from "@/lib/types";

interface ChatMessageComponentProps {
  message: ChatMessage;
  onPin?: (message: ChatMessage) => void;
}

export function ChatMessageComponent({
  message,
  onPin,
}: ChatMessageComponentProps) {
  const isUser = message.role === "user";

  return (
    <div
      className={`flex ${isUser ? "justify-start" : "justify-start"} mb-3 animate-in slide-in-from-bottom-2 duration-300`}
    >
      <div
        className={`max-w-[90%] rounded-lg px-4 py-3 text-sm ${
          isUser
            ? "bg-gold/10 border border-gold/20 text-foreground"
            : "bg-[hsl(var(--muted))] text-foreground/90"
        }`}
      >
        {isUser ? (
          <p className="leading-relaxed">{message.content}</p>
        ) : (
          <div className="relative group/msg">
            <MarkdownContent content={message.content} />
            {onPin && (
              <Button
                size="icon"
                variant="ghost"
                className="absolute top-0 left-0 h-6 w-6 opacity-0 group-hover/msg:opacity-100 transition-opacity text-gold hover:text-gold/80"
                onClick={() => onPin(message)}
                title="تثبيت في التقرير"
              >
                <Pin className="h-3 w-3" />
              </Button>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
