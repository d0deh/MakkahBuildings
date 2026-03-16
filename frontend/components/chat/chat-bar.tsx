"use client";

import { useRef, useEffect } from "react";
import { ChevronDown } from "lucide-react";
import { Button } from "@/components/ui/button";
import { ChatInput } from "./chat-input";
import { ChatMessageComponent } from "./chat-message";
import { useDashboardStore } from "@/lib/store";
import { sendChatMessage, pinItem as pinItemApi } from "@/lib/api";
import type { ChatMessage } from "@/lib/types";

interface ChatBarProps {
  sessionId: string;
}

export function ChatBar({ sessionId }: ChatBarProps) {
  const {
    conversationOpen,
    setConversationOpen,
    chatMessages,
    addMessage,
    chatLoading,
    setChatLoading,
    pinItem,
  } = useDashboardStore();

  const messagesEndRef = useRef<HTMLDivElement>(null);
  const conversationRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    if (conversationOpen) {
      messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }
  }, [chatMessages, conversationOpen]);

  // Open conversation when messages exist
  useEffect(() => {
    if (chatMessages.length > 0 && !conversationOpen) {
      setConversationOpen(true);
    }
  }, [chatMessages.length, conversationOpen, setConversationOpen]);

  const handleSend = async (text: string) => {
    const userMsg: ChatMessage = {
      id: Date.now().toString(),
      role: "user",
      content: text,
    };
    addMessage(userMsg);
    setChatLoading(true);
    setConversationOpen(true);

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
    <div className="fixed bottom-0 left-0 right-0 z-50 flex flex-col items-center pointer-events-none">
      {/* Conversation area */}
      {conversationOpen && chatMessages.length > 0 && (
        <div
          ref={conversationRef}
          className="w-full max-w-[800px] pointer-events-auto"
        >
          <div className="bg-background/95 backdrop-blur-md border border-[hsl(var(--border))] border-b-0 rounded-t-xl shadow-2xl max-h-[60vh] flex flex-col">
            {/* Conversation header */}
            <div className="flex items-center justify-between px-4 py-2 border-b border-[hsl(var(--border))] shrink-0">
              <h3 className="text-xs font-bold text-muted-foreground">
                محادثة مع البيانات
              </h3>
              <div className="flex items-center gap-1">
                <Button
                  size="icon"
                  variant="ghost"
                  onClick={() => setConversationOpen(false)}
                  className="h-6 w-6 text-muted-foreground hover:text-foreground"
                >
                  <ChevronDown className="h-3.5 w-3.5" />
                </Button>
              </div>
            </div>

            {/* Messages */}
            <div className="flex-1 overflow-y-auto p-4 space-y-1" dir="rtl">
              {chatMessages.map((msg) => (
                <ChatMessageComponent
                  key={msg.id}
                  message={msg}
                  onPin={msg.role === "assistant" ? handlePin : undefined}
                />
              ))}
              {chatLoading && (
                <div className="flex gap-1.5 items-center px-2 py-3">
                  <span className="w-2 h-2 rounded-full bg-gold animate-bounce" />
                  <span className="w-2 h-2 rounded-full bg-gold animate-bounce [animation-delay:0.1s]" />
                  <span className="w-2 h-2 rounded-full bg-gold animate-bounce [animation-delay:0.2s]" />
                </div>
              )}
              <div ref={messagesEndRef} />
            </div>
          </div>
        </div>
      )}

      {/* Input bar — always visible */}
      <div className="w-full max-w-[800px] pointer-events-auto">
        <div className="bg-background/95 backdrop-blur-md border border-[hsl(var(--border))] rounded-t-xl shadow-2xl px-2 pb-2 pt-1">
          {/* Collapsed state — show message count if conversation is hidden */}
          {!conversationOpen && chatMessages.length > 0 && (
            <button
              onClick={() => setConversationOpen(true)}
              className="w-full text-center py-1 text-xs text-muted-foreground hover:text-gold transition-colors"
            >
              {chatMessages.length} رسالة — اضغط لعرض المحادثة
            </button>
          )}
          <ChatInput onSend={handleSend} disabled={chatLoading} />
        </div>
      </div>
    </div>
  );
}
