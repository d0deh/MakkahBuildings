"use client";

import { useState, useRef } from "react";
import { Button } from "@/components/ui/button";
import { Send } from "lucide-react";

interface ChatInputProps {
  onSend: (message: string) => void;
  disabled?: boolean;
}

export function ChatInput({ onSend, disabled }: ChatInputProps) {
  const [value, setValue] = useState("");
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const handleSend = () => {
    const trimmed = value.trim();
    if (!trimmed || disabled) return;
    onSend(trimmed);
    setValue("");
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="border-t border-[hsl(var(--border))] p-3 flex gap-2 items-end">
      <textarea
        ref={textareaRef}
        value={value}
        onChange={(e) => {
          setValue(e.target.value);
          e.target.style.height = "auto";
          e.target.style.height = Math.min(e.target.scrollHeight, 120) + "px";
        }}
        onKeyDown={handleKeyDown}
        placeholder="اسأل عن البيانات..."
        disabled={disabled}
        rows={1}
        className="flex-1 bg-[hsl(var(--muted))] border border-[hsl(var(--border))] rounded-lg px-3 py-2 text-sm text-foreground placeholder:text-muted-foreground resize-none focus:outline-none focus:ring-1 focus:ring-gold/50"
        dir="rtl"
      />
      <Button
        size="icon"
        onClick={handleSend}
        disabled={disabled || !value.trim()}
        className="bg-gold hover:bg-gold-dark text-background h-9 w-9 shrink-0"
      >
        <Send className="h-4 w-4" />
      </Button>
    </div>
  );
}
