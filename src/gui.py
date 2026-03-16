"""Web GUI for Urban Survey Report Generator.

Navy+Gold themed Arabic interface served on localhost via Flask.
Uses SSE for real-time progress and native file dialogs for browsing.
"""
from __future__ import annotations

import json
import os
import queue
import subprocess
import threading
import webbrowser
from datetime import datetime
from pathlib import Path

from flask import Flask, Response, jsonify, render_template_string, request

from .config import OUTPUT_DIR
from .pipeline import generate_report

app = Flask(__name__)

# Single-user state
_queue: queue.Queue = queue.Queue()
_state = {"running": False, "result": None}


# ------------------------------------------------------------------ HTML
HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>مولد التقارير العمرانية</title>
<style>
:root {
  --navy: #1B2A4A;
  --gold: #C9A84C;
  --dark-gold: #A68A3E;
  --light-navy: #2D4A7A;
  --bg-light: #F0F0F0;
  --white: #FFFFFF;
  --text-dark: #1A1A1A;
}
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
  font-family: "Segoe UI", Tahoma, sans-serif;
  background: var(--bg-light);
  height: 100vh;
  overflow: hidden;
}
.container {
  display: grid;
  grid-template-columns: 340px 1fr;
  height: 100vh;
  direction: rtl;
}
/* --- Right panel (controls, appears right in RTL) --- */
.panel-controls {
  background: var(--navy);
  padding: 28px 22px;
  display: flex;
  flex-direction: column;
  color: white;
  overflow-y: auto;
}
h1 {
  color: var(--gold);
  font-size: 21px;
  text-align: center;
  margin-bottom: 28px;
}
.section-title {
  color: #8899AA;
  font-size: 13px;
  margin: 14px 0 6px;
}
.input-group {
  display: flex;
  gap: 8px;
  margin-bottom: 14px;
}
.input-group input {
  flex: 1;
  padding: 9px 12px;
  border: 1px solid #3a5070;
  border-radius: 6px;
  background: rgba(255,255,255,0.08);
  color: white;
  font-family: inherit;
  font-size: 13px;
  direction: ltr;
  text-align: right;
  outline: none;
  transition: border-color 0.2s;
}
.input-group input:focus { border-color: var(--gold); }
.input-group input::placeholder { color: #6680A0; }
.btn-browse {
  padding: 9px 14px;
  background: var(--gold);
  color: var(--navy);
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: bold;
  font-family: inherit;
  font-size: 13px;
  white-space: nowrap;
  transition: background 0.2s;
}
.btn-browse:hover { background: var(--dark-gold); }
.checkbox-group {
  display: flex;
  align-items: center;
  gap: 10px;
  margin: 6px 0 18px;
}
.checkbox-group input[type="checkbox"] {
  accent-color: var(--gold);
  width: 18px;
  height: 18px;
  cursor: pointer;
}
.checkbox-group label { font-size: 14px; cursor: pointer; }
.progress-container { margin: 8px 0; }
.progress-bar {
  width: 100%;
  height: 14px;
  background: var(--light-navy);
  border-radius: 7px;
  overflow: hidden;
}
.progress-fill {
  height: 100%;
  background: var(--gold);
  width: 0%;
  transition: width 0.4s ease;
  border-radius: 7px;
}
.progress-text {
  font-size: 12px;
  color: #99AABB;
  margin-top: 5px;
  min-height: 1.2em;
}
.btn-generate {
  margin-top: auto;
  padding: 14px;
  background: var(--gold);
  color: var(--navy);
  border: none;
  border-radius: 8px;
  font-size: 18px;
  font-weight: bold;
  font-family: inherit;
  cursor: pointer;
  transition: background 0.2s, opacity 0.2s;
}
.btn-generate:hover { background: var(--dark-gold); }
.btn-generate:disabled { opacity: 0.45; cursor: not-allowed; }

/* --- Left panel (log, appears left in RTL) --- */
.panel-log {
  padding: 22px 24px;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}
.log-title {
  font-size: 16px;
  font-weight: bold;
  margin-bottom: 10px;
  color: var(--text-dark);
}
.log-box {
  flex: 1;
  background: white;
  border-radius: 8px;
  padding: 14px;
  overflow-y: auto;
  font-size: 13px;
  line-height: 2;
  border: 1px solid #DDD;
  direction: rtl;
}
.log-entry { color: var(--text-dark); }
.log-entry .ts { color: #999; font-size: 11px; margin-left: 8px; }
.log-entry.error { color: #C62828; font-weight: bold; }
.log-entry.success { color: #2E7D32; font-weight: bold; }
.log-placeholder {
  color: #AAA;
  text-align: center;
  margin-top: 40px;
  font-size: 14px;
}

/* --- Result --- */
.result-section {
  margin-top: 14px;
  padding: 16px;
  background: white;
  border-radius: 8px;
  border: 1px solid #DDD;
  display: none;
}
.result-section.visible { display: block; }
.result-title { font-size: 14px; font-weight: bold; margin-bottom: 6px; }
.result-path {
  font-size: 12px;
  color: #666;
  margin-bottom: 12px;
  direction: ltr;
  text-align: right;
  word-break: break-all;
}
.result-buttons { display: flex; gap: 8px; }
.btn-result {
  padding: 9px 22px;
  border: none;
  border-radius: 6px;
  font-size: 13px;
  font-weight: bold;
  font-family: inherit;
  cursor: pointer;
  transition: background 0.2s;
}
.btn-open-file { background: var(--gold); color: var(--navy); }
.btn-open-folder { background: var(--light-navy); color: white; }
.btn-open-file:hover { background: var(--dark-gold); }
.btn-open-folder:hover { background: var(--navy); }

/* --- Error toast --- */
.toast {
  position: fixed;
  top: 20px;
  left: 50%;
  transform: translateX(-50%);
  background: #C62828;
  color: white;
  padding: 14px 28px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: bold;
  box-shadow: 0 4px 20px rgba(0,0,0,0.3);
  z-index: 1000;
  display: none;
  direction: rtl;
}
.toast.visible { display: block; animation: fadeIn 0.3s ease; }
@keyframes fadeIn { from { opacity: 0; transform: translateX(-50%) translateY(-10px); } to { opacity: 1; transform: translateX(-50%) translateY(0); } }
</style>
</head>
<body>
<div class="toast" id="toast"></div>
<div class="container">
  <!-- Controls panel -->
  <div class="panel-controls">
    <h1>مولد التقارير العمرانية</h1>

    <div class="section-title">── ملف البيانات ──</div>
    <div class="input-group">
      <input type="text" id="filePath" placeholder="اختر ملف Excel...">
      <button class="btn-browse" onclick="browseFile()">تصفح</button>
    </div>

    <div class="section-title">── مجلد المخرجات ──</div>
    <div class="input-group">
      <input type="text" id="outputDir" value="{{ output_dir }}">
      <button class="btn-browse" onclick="browseFolder()">تصفح</button>
    </div>

    <div class="checkbox-group">
      <input type="checkbox" id="useAi" checked>
      <label for="useAi">تفعيل التحليل الذكي</label>
    </div>

    <div class="progress-container">
      <div class="progress-bar"><div class="progress-fill" id="progressFill"></div></div>
      <div class="progress-text" id="progressText"></div>
    </div>

    <button class="btn-generate" id="btnGenerate" onclick="startGeneration()">
      إنشاء التقرير
    </button>
  </div>

  <!-- Log panel -->
  <div class="panel-log">
    <div class="log-title">سجل العمليات</div>
    <div class="log-box" id="logBox">
      <div class="log-placeholder" id="logPlaceholder">سيتم عرض تقدم العمليات هنا...</div>
    </div>
    <div class="result-section" id="resultSection">
      <div class="result-title">── النتيجة ──</div>
      <div class="result-path" id="resultPath"></div>
      <div class="result-buttons">
        <button class="btn-result btn-open-file" onclick="openFile()">فتح الملف</button>
        <button class="btn-result btn-open-folder" onclick="openFolder()">فتح المجلد</button>
      </div>
    </div>
  </div>
</div>

<script>
const $ = id => document.getElementById(id);

function timestamp() {
  const d = new Date();
  return d.toLocaleTimeString("en-GB", {hour:"2-digit", minute:"2-digit", second:"2-digit"});
}

function addLog(text, cls) {
  $("logPlaceholder").style.display = "none";
  const el = document.createElement("div");
  el.className = "log-entry" + (cls ? " " + cls : "");
  el.innerHTML = '<span class="ts">[' + timestamp() + ']</span> ' + text;
  $("logBox").appendChild(el);
  $("logBox").scrollTop = $("logBox").scrollHeight;
}

function showToast(msg) {
  const t = $("toast");
  t.textContent = msg;
  t.classList.add("visible");
  setTimeout(() => t.classList.remove("visible"), 4000);
}

function setEnabled(enabled) {
  $("btnGenerate").disabled = !enabled;
}

// --- File browsing (uses native dialogs via server) ---
async function browseFile() {
  try {
    const res = await fetch("/browse-file", {method: "POST"});
    const data = await res.json();
    if (data.path) $("filePath").value = data.path;
  } catch(e) { console.error(e); }
}

async function browseFolder() {
  try {
    const res = await fetch("/browse-folder", {method: "POST"});
    const data = await res.json();
    if (data.path) $("outputDir").value = data.path;
  } catch(e) { console.error(e); }
}

// --- Generation ---
async function startGeneration() {
  const filePath = $("filePath").value.trim();
  if (!filePath) { showToast("يرجى اختيار ملف البيانات أولاً"); return; }

  // Reset UI
  $("logBox").innerHTML = '<div class="log-placeholder" id="logPlaceholder" style="display:none"></div>';
  $("resultSection").classList.remove("visible");
  $("progressFill").style.width = "0%";
  $("progressText").textContent = "";
  setEnabled(false);
  addLog("بدء إنشاء التقرير...");

  try {
    const res = await fetch("/generate", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({
        excel_path: filePath,
        output_dir: $("outputDir").value.trim(),
        use_ai: $("useAi").checked,
      }),
    });
    if (!res.ok) {
      const err = await res.json();
      showToast(err.error || "خطأ غير متوقع");
      setEnabled(true);
      return;
    }
  } catch(e) {
    showToast("فشل الاتصال بالخادم");
    setEnabled(true);
    return;
  }

  // Listen for SSE progress events
  const evtSource = new EventSource("/events");

  evtSource.addEventListener("progress", e => {
    const d = JSON.parse(e.data);
    $("progressFill").style.width = d.pct + "%";
    $("progressText").textContent = "%" + d.pct + " - " + d.step;
    addLog(d.step);
  });

  evtSource.addEventListener("done", e => {
    const d = JSON.parse(e.data);
    addLog("تم بنجاح!", "success");
    $("resultPath").textContent = d.path;
    $("resultSection").classList.add("visible");
    $("progressFill").style.width = "100%";
    $("progressText").textContent = "%100 - اكتمل";
    setEnabled(true);
    evtSource.close();
  });

  evtSource.addEventListener("error_msg", e => {
    const d = JSON.parse(e.data);
    addLog("خطأ: " + d.message, "error");
    showToast(d.message);
    setEnabled(true);
    evtSource.close();
  });

  evtSource.onerror = () => {
    evtSource.close();
    setEnabled(true);
  };
}

// --- Result buttons ---
async function openFile() {
  await fetch("/open-file", {method: "POST"});
}
async function openFolder() {
  await fetch("/open-folder", {method: "POST"});
}
</script>
</body>
</html>"""


# ------------------------------------------------------------------ Routes
@app.route("/")
def index():
    return render_template_string(
        HTML_TEMPLATE,
        output_dir=str(OUTPUT_DIR).replace("\\", "/"),
    )


@app.route("/browse-file", methods=["POST"])
def browse_file():
    """Open native file dialog (works because this is localhost)."""
    import tkinter as tk
    from tkinter import filedialog

    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    path = filedialog.askopenfilename(
        title="اختر ملف البيانات",
        filetypes=[("Excel files", "*.xlsx *.xls"), ("All files", "*.*")],
    )
    root.destroy()
    return jsonify({"path": path})


@app.route("/browse-folder", methods=["POST"])
def browse_folder():
    """Open native folder dialog."""
    import tkinter as tk
    from tkinter import filedialog

    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    path = filedialog.askdirectory(title="اختر مجلد المخرجات")
    root.destroy()
    return jsonify({"path": path})


@app.route("/generate", methods=["POST"])
def start_generate():
    if _state["running"]:
        return jsonify({"error": "التقرير قيد الإنشاء حالياً"}), 409

    data = request.get_json()
    excel_path = data.get("excel_path", "").strip()
    output_dir = data.get("output_dir", "").strip()
    use_ai = data.get("use_ai", True)

    if not excel_path or not Path(excel_path).is_file():
        return jsonify({"error": "ملف البيانات غير موجود"}), 400

    # Clear any stale messages
    while not _queue.empty():
        try:
            _queue.get_nowait()
        except queue.Empty:
            break

    _state["running"] = True
    _state["result"] = None

    def worker():
        try:
            def on_progress(step: str, pct: int):
                _queue.put(("progress", {"step": step, "pct": pct}))

            result = generate_report(
                excel_path=excel_path,
                output_dir=output_dir or None,
                use_ai=use_ai,
                on_progress=on_progress,
            )
            _state["result"] = result
            _queue.put(("done", {"path": result}))
        except Exception as exc:
            import traceback
            tb = traceback.format_exc()
            _queue.put(("error_msg", {"message": f"{exc}\n\n{tb}"}))
        finally:
            _state["running"] = False

    threading.Thread(target=worker, daemon=True).start()
    return jsonify({"status": "started"})


@app.route("/events")
def events():
    """SSE endpoint — streams progress from worker thread to browser."""
    def stream():
        while True:
            try:
                msg = _queue.get(timeout=30)
                event_type, data = msg
                payload = json.dumps(data, ensure_ascii=False)
                yield f"event: {event_type}\ndata: {payload}\n\n"
                if event_type in ("done", "error_msg"):
                    break
            except queue.Empty:
                # Keep-alive ping
                yield "event: ping\ndata: {}\n\n"

    return Response(stream(), mimetype="text/event-stream",
                    headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})


@app.route("/open-file", methods=["POST"])
def open_file():
    if _state["result"] and Path(_state["result"]).exists():
        os.startfile(_state["result"])
    return jsonify({"ok": True})


@app.route("/open-folder", methods=["POST"])
def open_folder():
    if _state["result"]:
        folder = str(Path(_state["result"]).parent)
        subprocess.Popen(["explorer", folder])
    return jsonify({"ok": True})


# ------------------------------------------------------------------ Entry point
def main():
    port = 5000
    url = f"http://localhost:{port}"
    print(f"\n  Urban Survey Report Generator")
    print(f"  Running at: {url}\n")
    threading.Timer(1.5, lambda: webbrowser.open(url)).start()
    app.run(host="127.0.0.1", port=port, debug=False, threaded=True)


if __name__ == "__main__":
    main()
