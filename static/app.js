const I18N = {
  en: {
    tagline: "#Hello-This is your supportive-partner: I'm just a child - so teach me :3 ",
    navChat: "Chat",
    navKb: "Knowledge Base",
    chatTitle: "Chat",
    chatSub: "Ask anything about your uploaded documents",
    kbTitle: "Knowledge Base",
    kbSub: "Upload and manage your learning materials",
    chatEmptyTitle: "Hi! Ask me anything about your uploaded documents.",
    chatEmptySub: "No documents yet? Head to the Knowledge Base tab to upload one first.",
    send: "Send",
    kbUploadTitle: "Drag & drop a file here, or ",
    kbUploadLink: "browse",
    kbUploadSub: "Supports: PDF, DOCX, PPTX, XLSX, HTML, TXT, MD, images (JPG/PNG)",
    kbListHead: "Ingested documents",
    kbEmptyTitle: "No documents yet",
    themeLabel: "Theme",
    langLabel: "Language",
    assistant: "Assistant",
    thinking: "Thinking…",
    error: "Something went wrong, try again.",
    connError: "Couldn't reach the server. Check the backend.",
    uploading: (name) => `Processing "${name}"…`,
    uploaded: (source, n) => `Ingested "${source}" (${n} chunk${n === 1 ? "" : "s"}).`,
    uploadFailed: "Upload failed.",
    uploadConnError: "Couldn't reach the server.",
    loadDocsError: "Couldn't load the document list.",
    deleteConfirm: (source) => `Delete "${source}" from the knowledge base?`,
    deleteFailed: "Delete failed, try again.",
    chunkCount: (n) => `${n} chunk${n === 1 ? "" : "s"}`,
    noAnswer: "(no answer)",
    errorEyebrow: "Error",
  },
  vi: {
    tagline: "#Hello-This is your supportive-partner: I'm just a child - so teach me :3 ",
    navChat: "Trò chuyện",
    navKb: "Kho tài liệu",
    chatTitle: "Trò chuyện",
    chatSub: "Hỏi bất cứ điều gì về tài liệu đã upload",
    kbTitle: "Kho tài liệu",
    kbSub: "Upload và quản lý tài liệu học tập",
    chatEmptyTitle: "Chào bạn! Hỏi mình bất cứ điều gì về tài liệu đã upload nhé.",
    chatEmptySub: "Nếu chưa có tài liệu nào, qua tab \"Kho tài liệu\" để upload trước đã nha.",
    send: "Gửi",
    kbUploadTitle: "Kéo thả file vào đây, hoặc ",
    kbUploadLink: "chọn file",
    kbUploadSub: "Hỗ trợ: PDF, DOCX, PPTX, XLSX, HTML, TXT, MD, ảnh (JPG/PNG)",
    kbListHead: "Tài liệu đã nạp",
    kbEmptyTitle: "Chưa có tài liệu nào",
    themeLabel: "Giao diện",
    langLabel: "Ngôn ngữ",
    assistant: "Trợ lý",
    thinking: "Đang suy nghĩ…",
    error: "Có lỗi xảy ra, thử lại nhé.",
    connError: "Không kết nối được tới server. Kiểm tra lại backend nhé.",
    uploading: (name) => `Đang xử lý "${name}"…`,
    uploaded: (source, n) => `Đã nạp "${source}" (${n} đoạn).`,
    uploadFailed: "Upload thất bại.",
    uploadConnError: "Không kết nối được tới server.",
    loadDocsError: "Không tải được danh sách tài liệu.",
    deleteConfirm: (source) => `Xoá "${source}" khỏi kho tài liệu?`,
    deleteFailed: "Xoá thất bại, thử lại nhé.",
    chunkCount: (n) => `${n} đoạn`,
    noAnswer: "(không có câu trả lời)",
    errorEyebrow: "Lỗi",
  },
};

const VIEW_HEADERS = {
  chat: { titleKey: "chatTitle", subKey: "chatSub" },
  kb: { titleKey: "kbTitle", subKey: "kbSub" },
};

const state = {
  history: [], // [{role, content}]
  lang: localStorage.getItem("lang") || "en",
  theme: localStorage.getItem("theme") || (window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light"),
  activeTab: "chat",
};

function t(key) {
  return I18N[state.lang][key];
}

function applyLanguage() {
  document.documentElement.lang = state.lang;
  document.querySelectorAll("[data-i18n]").forEach((el) => {
    el.textContent = t(el.dataset.i18n);
  });
  document.getElementById("composerInput").placeholder = state.lang === "en"
    ? "Ask a question about your documents…"
    : "Đặt câu hỏi về tài liệu của bạn…";
  updateViewHeader();

  document.querySelectorAll(".lang-btn").forEach((btn) => {
    btn.classList.toggle("active", btn.dataset.lang === state.lang);
  });
}

function applyTheme() {
  document.documentElement.setAttribute("data-theme", state.theme);
  document.querySelectorAll(".swatch").forEach((btn) => {
    btn.classList.toggle("active", btn.dataset.theme === state.theme);
  });
}

function updateViewHeader() {
  const h = VIEW_HEADERS[state.activeTab];
  document.getElementById("viewTitle").textContent = t(h.titleKey);
  document.getElementById("viewSub").textContent = t(h.subKey);
}

document.querySelectorAll(".lang-btn").forEach((btn) => {
  btn.addEventListener("click", () => {
    state.lang = btn.dataset.lang;
    localStorage.setItem("lang", state.lang);
    applyLanguage();
  });
});

document.querySelectorAll(".swatch").forEach((btn) => {
  btn.addEventListener("click", () => {
    state.theme = btn.dataset.theme;
    localStorage.setItem("theme", state.theme);
    applyTheme();
  });
});

// ---------------- Nav ----------------
document.querySelectorAll(".nav-item").forEach((btn) => {
  btn.addEventListener("click", () => {
    document.querySelectorAll(".nav-item").forEach((b) => b.classList.remove("active"));
    document.querySelectorAll(".view").forEach((v) => v.classList.remove("active"));
    btn.classList.add("active");
    state.activeTab = btn.dataset.tab;
    document.getElementById(`view-${state.activeTab}`).classList.add("active");
    updateViewHeader();
    if (state.activeTab === "kb") loadDocuments();
  });
});

// ---------------- Chat ----------------
const thread = document.getElementById("thread");
const chatEmpty = document.getElementById("chatEmpty");
const composerForm = document.getElementById("composerForm");
const composerInput = document.getElementById("composerInput");
const sendBtn = document.getElementById("sendBtn");

const tplQuestion = document.getElementById("tpl-question");
const tplAnswer = document.getElementById("tpl-answer");
const tplPending = document.getElementById("tpl-pending");

composerInput.addEventListener("input", () => {
  composerInput.style.height = "auto";
  composerInput.style.height = Math.min(composerInput.scrollHeight, 120) + "px";
});

composerInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    composerForm.requestSubmit();
  }
});

composerForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const message = composerInput.value.trim();
  if (!message) return;

  chatEmpty.style.display = "none";
  addQuestion(message);
  composerInput.value = "";
  composerInput.style.height = "auto";
  sendBtn.disabled = true;

  const pendingNode = tplPending.content.cloneNode(true);
  pendingNode.querySelector(".a-eyebrow").textContent = t("thinking");
  const pendingCard = pendingNode.querySelector(".a-card");
  thread.appendChild(pendingNode);
  thread.scrollTop = thread.scrollHeight;

  try {
    const res = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message, history: state.history }),
    });
    const data = await res.json();
    pendingCard.remove();

    if (!res.ok) {
      addError(data.detail || t("error"));
      return;
    }

    addAnswer(data.answer, data.citations || [], data.model);
    state.history.push({ role: "user", content: message });
    state.history.push({ role: "assistant", content: data.answer });
    if (state.history.length > 12) state.history = state.history.slice(-12);

    document.getElementById("footerModel").textContent = data.model || "—";
  } catch (err) {
    pendingCard.remove();
    addError(t("connError"));
  } finally {
    sendBtn.disabled = false;
    composerInput.focus();
  }
});

function addQuestion(text) {
  const node = tplQuestion.content.cloneNode(true);
  node.querySelector(".q-bubble").textContent = text;
  thread.appendChild(node);
  thread.scrollTop = thread.scrollHeight;
}

function addAnswer(text, citations, model) {
  const node = tplAnswer.content.cloneNode(true);
  node.querySelector(".a-eyebrow").textContent = model ? `${t("assistant")} · ${model}` : t("assistant");
  node.querySelector(".a-text").textContent = text || t("noAnswer");

  const citeRow = node.querySelector(".cite-row");
  citations
    .filter((c) => c.source)
    .forEach((c) => {
      const chip = document.createElement("span");
      chip.className = "cite";
      const score = typeof c.score === "number" ? ` · ${(c.score * 100).toFixed(0)}%` : "";
      chip.innerHTML = `<span class="dot"></span>${escapeHtml(c.source)}${score}`;
      chip.title = c.snippet || "";
      citeRow.appendChild(chip);
    });

  thread.appendChild(node);
  thread.scrollTop = thread.scrollHeight;
}

function addError(message) {
  const node = tplAnswer.content.cloneNode(true);
  node.querySelector(".a-eyebrow").textContent = t("errorEyebrow");
  node.querySelector(".a-text").textContent = message;
  thread.appendChild(node);
  thread.scrollTop = thread.scrollHeight;
}

function escapeHtml(str) {
  const div = document.createElement("div");
  div.textContent = str;
  return div.innerHTML;
}

// ---------------- Knowledge base ----------------
const dropZone = document.getElementById("dropZone");
const fileInput = document.getElementById("fileInput");
const browseLink = document.getElementById("browseLink");
const kbStatus = document.getElementById("kbStatus");
const kbList = document.getElementById("kbList");
const kbEmpty = document.getElementById("kbEmpty");
const kbCount = document.getElementById("kbCount");
const tplDocRow = document.getElementById("tpl-doc-row");

browseLink.addEventListener("click", (e) => {
  e.stopPropagation();
  fileInput.click();
});
dropZone.addEventListener("click", () => fileInput.click());

fileInput.addEventListener("change", () => {
  if (fileInput.files[0]) uploadFile(fileInput.files[0]);
  fileInput.value = "";
});

["dragover", "dragenter"].forEach((evt) =>
  dropZone.addEventListener(evt, (e) => {
    e.preventDefault();
    dropZone.classList.add("dragover");
  })
);
["dragleave", "drop"].forEach((evt) =>
  dropZone.addEventListener(evt, (e) => {
    e.preventDefault();
    dropZone.classList.remove("dragover");
  })
);
dropZone.addEventListener("drop", (e) => {
  const file = e.dataTransfer.files[0];
  if (file) uploadFile(file);
});

async function uploadFile(file) {
  kbStatus.textContent = t("uploading")(file.name);
  kbStatus.className = "kb-status loading";

  const formData = new FormData();
  formData.append("file", file);

  try {
    const res = await fetch("/api/documents", { method: "POST", body: formData });
    const data = await res.json();

    if (!res.ok) {
      kbStatus.textContent = data.detail || t("uploadFailed");
      kbStatus.className = "kb-status err";
      return;
    }

    kbStatus.textContent = t("uploaded")(data.source, data.chunk_count);
    kbStatus.className = "kb-status ok";
    loadDocuments();
  } catch (err) {
    kbStatus.textContent = t("uploadConnError");
    kbStatus.className = "kb-status err";
  }
}

async function loadDocuments() {
  try {
    const res = await fetch("/api/documents");
    const docs = await res.json();

    kbCount.textContent = docs.length;
    kbList.querySelectorAll(".doc-row").forEach((el) => el.remove());
    kbEmpty.style.display = docs.length ? "none" : "block";

    docs.forEach((doc) => {
      const node = tplDocRow.content.cloneNode(true);
      node.querySelector(".doc-name").textContent = doc.source;
      const meta = [doc.file_type?.toUpperCase(), t("chunkCount")(doc.chunk_count)].filter(Boolean).join(" · ");
      node.querySelector(".doc-meta").textContent = meta;
      node.querySelector(".doc-delete").addEventListener("click", () => deleteDocument(doc.source));
      kbList.appendChild(node);
    });
  } catch (err) {
    kbStatus.textContent = t("loadDocsError");
    kbStatus.className = "kb-status err";
  }
}

async function deleteDocument(source) {
  if (!confirm(t("deleteConfirm")(source))) return;
  try {
    await fetch(`/api/documents/${encodeURIComponent(source)}`, { method: "DELETE" });
    loadDocuments();
  } catch (err) {
    kbStatus.textContent = t("deleteFailed");
    kbStatus.className = "kb-status err";
  }
}

applyTheme();
applyLanguage();
loadDocuments();
fetch("/api/health")
  .then((r) => r.json())
  .then((d) => (document.getElementById("footerModel").textContent = d.llm_model || "—"))
  .catch(() => {});