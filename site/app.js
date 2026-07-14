(() => {
  const root = document.documentElement;
  const themeButton = document.getElementById("theme-toggle");
  const copyButton = document.getElementById("copy-command");
  const command = document.getElementById("install-command");
  const copyStatus = document.getElementById("copy-status");

  function applyTheme(theme) {
    const dark = theme === "dark";
    root.dataset.theme = dark ? "dark" : "light";
    themeButton.setAttribute("aria-pressed", String(dark));
    themeButton.setAttribute("aria-label", dark ? "Use light theme" : "Use dark theme");
    document.querySelector('meta[name="theme-color"]').content = dark ? "#151b24" : "#f2ecdf";
    try {
      localStorage.setItem("paper-writing-site-theme", root.dataset.theme);
    } catch (_) {
      // A blocked storage API should not prevent theme switching.
    }
  }

  let savedTheme = null;
  try {
    savedTheme = localStorage.getItem("paper-writing-site-theme");
  } catch (_) {
    // Use the system preference when local storage is unavailable.
  }
  const systemTheme = window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
  applyTheme(savedTheme || systemTheme);

  themeButton.addEventListener("click", () => {
    applyTheme(root.dataset.theme === "dark" ? "light" : "dark");
  });

  copyButton.addEventListener("click", async () => {
    try {
      await navigator.clipboard.writeText(command.textContent.trim());
      copyStatus.textContent = "Command copied.";
      copyButton.querySelector("span").textContent = "Copied";
    } catch (_) {
      copyStatus.textContent = "Copy unavailable. Select the command manually.";
    }
    window.setTimeout(() => {
      copyStatus.textContent = "";
      copyButton.querySelector("span").textContent = "Copy command";
    }, 2400);
  });
})();
