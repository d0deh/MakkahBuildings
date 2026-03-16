import type {
  UploadResponse,
  ChartsResponse,
  AiContent,
  AiSectionResponse,
  AreaStats,
  HealthResponse,
  ChartDataResponse,
  PinnedItem,
} from "./types";

const BASE = "/api";

async function request<T>(url: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE}${url}`, options);
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: "خطأ غير متوقع" }));
    throw new Error(err.detail || err.error || `HTTP ${res.status}`);
  }
  return res.json();
}

export async function checkHealth(): Promise<HealthResponse> {
  return request("/health");
}

export async function uploadExcel(file: File): Promise<UploadResponse> {
  const formData = new FormData();
  formData.append("file", file);
  return request("/upload", { method: "POST", body: formData });
}

export async function getStats(sessionId: string): Promise<AreaStats> {
  return request(`/sessions/${sessionId}/stats`);
}

export async function getCharts(sessionId: string): Promise<ChartsResponse> {
  return request(`/sessions/${sessionId}/charts`);
}

export async function getAiContent(sessionId: string): Promise<AiContent> {
  return request(`/sessions/${sessionId}/ai`);
}

export async function getAiSection(
  sessionId: string,
  section: string
): Promise<AiSectionResponse> {
  return request(`/sessions/${sessionId}/ai/${section}`);
}

export async function regenerateSection(
  sessionId: string,
  section: string
): Promise<AiSectionResponse> {
  return request(`/sessions/${sessionId}/ai/${section}/regenerate`, {
    method: "POST",
  });
}

export async function getChartData(
  sessionId: string
): Promise<ChartDataResponse> {
  return request(`/sessions/${sessionId}/chart-data`);
}

export async function sendChatMessage(
  sessionId: string,
  message: string,
  history: { role: string; content: string }[]
): Promise<{ reply: string; message_id: string }> {
  return request(`/sessions/${sessionId}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message, history }),
  });
}

export async function pinItem(
  sessionId: string,
  messageId: string,
  text: string,
  chartSpec?: Record<string, unknown> | null
): Promise<{ ok: boolean }> {
  return request(`/sessions/${sessionId}/pin`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      message_id: messageId,
      text,
      chart_spec: chartSpec || null,
    }),
  });
}

export async function unpinItem(
  sessionId: string,
  messageId: string
): Promise<{ ok: boolean }> {
  return request(`/sessions/${sessionId}/pin/${messageId}`, {
    method: "DELETE",
  });
}

export async function getPinnedItems(
  sessionId: string
): Promise<{ items: PinnedItem[] }> {
  return request(`/sessions/${sessionId}/pins`);
}

export async function exportPptx(
  sessionId: string,
  sections?: string[],
  editedTexts?: Record<string, string>,
  pinnedItems?: PinnedItem[]
): Promise<Blob> {
  const res = await fetch(`${BASE}/sessions/${sessionId}/export`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      sections: sections || null,
      edited_texts: editedTexts || null,
      pinned_items: pinnedItems || null,
    }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: "خطأ في التصدير" }));
    throw new Error(err.detail || `HTTP ${res.status}`);
  }
  return res.blob();
}
