(() => {
  const MAX_FILE_BYTES = 2 * 1024 * 1024;
  const root = document.documentElement;
  const sessionToken = document.querySelector('meta[name="audit-session"]').content;
  const fileInput = document.getElementById("audit-file");
  const dropZone = document.getElementById("drop-zone");
  const fileName = document.getElementById("file-name");
  const emptyState = document.getElementById("empty-state");
  const loadingState = document.getElementById("loading-state");
  const preview = document.getElementById("audit-preview");
  const status = document.getElementById("status-message");
  const schemaStatus = document.getElementById("schema-status");
  const findingCount = document.getElementById("finding-count");
  const downloadButton = document.getElementById("download-html");
  const openButton = document.getElementById("open-preview");
  const clearButton = document.getElementById("clear-preview");
  const exampleButton = document.getElementById("load-example");
  const themeButton = document.getElementById("theme-toggle");
  let renderedUrl = null;
  let renderedName = "audit-map.html";

  function applyTheme(theme) {
    const dark = theme === "dark";
    root.dataset.theme = dark ? "dark" : "light";
    themeButton.setAttribute("aria-pressed", String(dark));
    themeButton.setAttribute("aria-label", dark ? "Use light theme" : "Use dark theme");
    themeButton.querySelector(".theme-label").textContent = dark ? "Light" : "Dark";
    document.querySelector('meta[name="theme-color"]').content = dark ? "#151b24" : "#f3ecdf";
    try { localStorage.setItem("local-audit-theme", root.dataset.theme); } catch (_) {}
  }

  function setStatus(message, isError = false) {
    status.textContent = message;
    status.classList.toggle("is-error", isError);
  }

  function setLoading(loading) {
    loadingState.hidden = !loading;
    loadingState.setAttribute("aria-hidden", String(!loading));
    if (loading) {
      emptyState.hidden = true;
      preview.hidden = true;
    }
  }

  function releasePreview() {
    if (renderedUrl) URL.revokeObjectURL(renderedUrl);
    renderedUrl = null;
    preview.removeAttribute("src");
  }

  function clearPreview() {
    releasePreview();
    preview.hidden = true;
    emptyState.hidden = false;
    loadingState.hidden = true;
    fileInput.value = "";
    fileName.textContent = "no audit selected";
    schemaStatus.textContent = "—";
    findingCount.textContent = "—";
    downloadButton.disabled = true;
    openButton.disabled = true;
    clearButton.disabled = true;
    setStatus("Choose JSON or load the teaching fixture.");
  }

  async function renderJson(raw, sourceName) {
    setLoading(true);
    fileName.textContent = sourceName;
    setStatus("Validating JSON with the canonical renderer…");
    try {
      const response = await fetch("/render", {
        method: "POST",
        headers: {"Content-Type": "application/json", "X-Audit-Session": sessionToken},
        body: JSON.stringify(raw),
      });
      if (!response.ok) {
        let message = `Renderer rejected the document (${response.status}).`;
        try { message = (await response.json()).error || message; } catch (_) {}
        throw new Error(message);
      }
      const html = await response.text();
      releasePreview();
      renderedUrl = URL.createObjectURL(new Blob([html], {type: "text/html"}));
      renderedName = sourceName.replace(/\.json$/i, "") + ".html";
      preview.src = renderedUrl;
      preview.hidden = false;
      emptyState.hidden = true;
      schemaStatus.textContent = "v1 · valid";
      findingCount.textContent = response.headers.get("X-Audit-Finding-Count") || "0";
      downloadButton.disabled = false;
      openButton.disabled = false;
      clearButton.disabled = false;
      setStatus("Rendered locally. No manuscript analysis was performed.");
    } catch (error) {
      releasePreview();
      preview.hidden = true;
      emptyState.hidden = false;
      schemaStatus.textContent = "invalid";
      findingCount.textContent = "—";
      downloadButton.disabled = true;
      openButton.disabled = true;
      clearButton.disabled = false;
      setStatus(error.message || "The local preview could not be created.", true);
    } finally {
      setLoading(false);
    }
  }

  async function useFile(file) {
    if (!file) return;
    if (file.size > MAX_FILE_BYTES) {
      fileName.textContent = file.name;
      setStatus("The selected file exceeds the 2 MiB local preview limit.", true);
      return;
    }
    try {
      const raw = JSON.parse(await file.text());
      await renderJson(raw, file.name || "local-audit.json");
    } catch (error) {
      fileName.textContent = file.name;
      schemaStatus.textContent = "invalid";
      setStatus(`Invalid JSON: ${error.message}`, true);
      clearButton.disabled = false;
    }
  }

  fileInput.addEventListener("change", () => useFile(fileInput.files[0]));
  ["dragenter", "dragover"].forEach((name) => dropZone.addEventListener(name, (event) => {
    event.preventDefault();
    dropZone.classList.add("is-dragging");
  }));
  ["dragleave", "drop"].forEach((name) => dropZone.addEventListener(name, (event) => {
    event.preventDefault();
    dropZone.classList.remove("is-dragging");
  }));
  dropZone.addEventListener("drop", (event) => useFile(event.dataTransfer.files[0]));

  exampleButton.addEventListener("click", async () => {
    try {
      const response = await fetch("/example.json", {cache: "no-store"});
      if (!response.ok) throw new Error("The teaching fixture is unavailable.");
      await renderJson(await response.json(), "section-audit-map.json");
    } catch (error) {
      setStatus(error.message, true);
    }
  });
  clearButton.addEventListener("click", clearPreview);
  downloadButton.addEventListener("click", () => {
    if (!renderedUrl) return;
    const link = document.createElement("a");
    link.href = renderedUrl;
    link.download = renderedName;
    link.click();
  });
  openButton.addEventListener("click", () => {
    if (renderedUrl) window.open(renderedUrl, "_blank", "noopener,noreferrer");
  });
  themeButton.addEventListener("click", () => applyTheme(root.dataset.theme === "dark" ? "light" : "dark"));

  let savedTheme = null;
  try { savedTheme = localStorage.getItem("local-audit-theme"); } catch (_) {}
  applyTheme(savedTheme || (window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light"));
  window.addEventListener("beforeunload", releasePreview);
})();
