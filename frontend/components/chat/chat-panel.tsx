"use client";

import { useRef, useEffect } from "react";
import { X } from "lucide-react";
import { Button } from "@/components/ui/button";
import { ChatInput } from "./chat-input";
import { ChatMessageComponent } from "./chat-message";
import { useDashboardStore } from "@/lib/store";
import { sendChatMessage, pinItem as pinItemApi } from "@/lib/api";
import type { ChatMessage } from "@/lib/types";

interface ChatPanelProps {
  sessionId: string;
}

export function ChatPanel({ sessionId }: ChatPanelProps) {
  const {
    chatOpen,
    toggleChat,
    chatMessages,
    addMessage,
    chatLoading,
    setChatLoading,
    pinItem,
  } = useDashboardStore();

  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [chatMessages]);

  if (!chatOpen) return null;

  const handleSend = async (text: string) => {
    const userMsg: ChatMessage = {
      id: Date.now().toString(),
      role: "user",
      content: text,
    };
    addMessage(userMsg);
    setChatLoading(true);

    try {
      const history = chatMessages.map((m) => ({
        role: m.role,
        content: m.content,
      }));
      const { reply, message_id } = await sendChatMessage(
        sessionId,
        text,
        history
      );
      const assistantMsg: ChatMessage = {
        id: message_id,
        role: "assistant",
        content: reply,
      };
      addMessage(assistantMsg);
    } catch (err) {
      const errorMsg: ChatMessage = {
        id: Date.now().toString(),
        role: "assistant",
        content:
          err instanceof Error
            ? `خطأ: ${err.message}`
            : "حدث خطأ غير متوقع",
      };
      addMessage(errorMsg);
    } finally {
      setChatLoading(false);
    }
  };

  const handlePin = async (message: ChatMessage) => {
    try {
      await pinItemApi(sessionId, message.id, message.content);
      pinItem({
        message_id: message.id,
        text: message.content,
        chart_spec: message.chartSpec || null,
      });
    } catch (err) {
      console.error("Pin failed:", err);
    }
  };

  return (
    <div className="fixed top-0 left-0 h-full w-[400px] bg-background border-r border-[hsl(var(--border))] z-50 flex flex-col shadow-2xl animate-in slide-in-from-left duration-300 max-md:w-full">
      {/* Header */}
      <div className="px-4 py-3 border-b border-[hsl(var(--border))] flex items-center justify-between">
        <h3 className="text-foreground font-bold text-sm">
          محادثة مع البيانات
        </h3>
        <Button
          size="icon"
          variant="ghost"
          onClick={toggleChat}
          className="h-8 w-8 text-muted-foreground hover:text-foreground"
        >
          <X className="h-4 w-4" />
        </Button>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-1" dir="rtl">
        {chatMessages.length === 0 && (
          <div className="text-center text-muted-foreground text-sm mt-8">
            <p>اسأل أي سؤال حول بيانات المسح العمراني</p>
            <p className="mt-2 text-xs">
              مثال: ما نسبة المباني المهجورة؟
            </p>
          </div>
        )}
        {chatMessages.map((msg) => (
          <ChatMessageComponent
            key={msg.id}
            message={msg}
            onPin={msg.role === "assistant" ? handlePin : undefined}
          />
        ))}
        {chatLoading && (
          <div className="flex gap-1 items-center px-4 py-3">
            <span className="w-2 h-2 rounded-full bg-gold animate-bounce" />
            <span className="w-2 h-2 rounded-full bg-gold animate-bounce [animation-delay:0.1s]" />
            <span className="w-2 h-2 rounded-full bg-gold animate-bounce [animation-delay:0.2s]" />
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <ChatInput onSend={handleSend} disabled={chatLoading} />
    </div>
  );
}
