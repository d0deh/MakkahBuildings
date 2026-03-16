import { create } from "zustand";
import type { ChatMessage, PinnedItem } from "./types";

interface DashboardStore {
  // Chat
  conversationOpen: boolean;
  setConversationOpen: (open: boolean) => void;
  chatMessages: ChatMessage[];
  addMessage: (msg: ChatMessage) => void;
  chatLoading: boolean;
  setChatLoading: (loading: boolean) => void;

  // Pinned items
  pinnedItems: PinnedItem[];
  setPinnedItems: (items: PinnedItem[]) => void;
  pinItem: (item: PinnedItem) => void;
  unpinItem: (messageId: string) => void;

  // Section visibility (M5)
  hiddenSections: Set<string>;
  toggleSection: (sectionId: string) => void;

  // Edited texts (M5)
  editedTexts: Record<string, string>;
  setEditedText: (sectionId: string, text: string) => void;
  clearEditedText: (sectionId: string) => void;
}

export const useDashboardStore = create<DashboardStore>((set) => ({
  // Chat
  conversationOpen: false,
  setConversationOpen: (open) => set({ conversationOpen: open }),
  chatMessages: [],
  addMessage: (msg) =>
    set((s) => ({ chatMessages: [...s.chatMessages, msg] })),
  chatLoading: false,
  setChatLoading: (loading) => set({ chatLoading: loading }),

  // Pinned items
  pinnedItems: [],
  setPinnedItems: (items) => set({ pinnedItems: items }),
  pinItem: (item) =>
    set((s) => ({ pinnedItems: [...s.pinnedItems, item] })),
  unpinItem: (messageId) =>
    set((s) => ({
      pinnedItems: s.pinnedItems.filter((p) => p.message_id !== messageId),
    })),

  // Section visibility
  hiddenSections: new Set<string>(),
  toggleSection: (sectionId) =>
    set((s) => {
      const next = new Set(s.hiddenSections);
      if (next.has(sectionId)) {
        next.delete(sectionId);
      } else {
        next.add(sectionId);
      }
      return { hiddenSections: next };
    }),

  // Edited texts
  editedTexts: {},
  setEditedText: (sectionId, text) =>
    set((s) => ({ editedTexts: { ...s.editedTexts, [sectionId]: text } })),
  clearEditedText: (sectionId) =>
    set((s) => {
      const next = { ...s.editedTexts };
      delete next[sectionId];
      return { editedTexts: next };
    }),
}));
