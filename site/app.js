(() => {
  const root = document.documentElement;
  const themeButton = document.getElementById("theme-toggle");
  const copyButtons = [...document.querySelectorAll("[data-copy]")];
  const copyStatus = document.getElementById("copy-status");
  const agentButtons = [...document.querySelectorAll(".agent-choice")];
  const installPrompt = document.getElementById("install-prompt");
  const installCommand = document.getElementById("install-command");
  const installGuidance = document.getElementById("install-guidance");
  const exampleButtons = [...document.querySelectorAll(".example-choice")];
  const previewFrame = document.getElementById("preview-frame");
  const previewFilename = document.getElementById("preview-filename");
  const previewJson = document.getElementById("preview-json");
  const previewHtml = document.getElementById("preview-html");
  const previewOpen = document.getElementById("preview-open");
  const masthead = document.getElementById("masthead");
  const hero = document.querySelector(".hero");
  const shader = document.getElementById("sky-shader");

  /* ---------------------------------------------------------------- theme */

  function applyTheme(theme) {
    const dark = theme === "dark";
    root.dataset.theme = dark ? "dark" : "light";
    themeButton.setAttribute("aria-pressed", String(dark));
    themeButton.setAttribute("aria-label", dark ? "Use light theme" : "Use dark theme");
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

  /* --------------------------------------------------------- agent install */

  const installTargets = {
    codex: {
      name: "Codex",
      prompt: "$",
      command: "npx skills add https://github.com/huguryildiz/ieee-acm-paper-writing/tree/v0.5.0 -a codex -y",
      guidance: "Run this in your manuscript project, then start a new Codex session.",
    },
    "claude-code": {
      name: "Claude Code",
      prompt: "›",
      command:
        "/plugin marketplace add huguryildiz/ieee-acm-paper-writing\n/plugin install ieee-acm-paper-writing",
      guidance: "Enter both lines in Claude Code, then restart the session.",
    },
  };

  function selectAgent(button) {
    const target = installTargets[button.dataset.agent];
    agentButtons.forEach((candidate) => {
      const selected = candidate === button;
      candidate.classList.toggle("is-active", selected);
      candidate.setAttribute("aria-pressed", String(selected));
    });
    installPrompt.textContent = target.prompt;
    installCommand.textContent = target.command;
    installGuidance.textContent = target.guidance;
    const copyButton = document.querySelector('[data-copy="install-command"]');
    copyButton.setAttribute("aria-label", `Copy the ${target.name} install command`);
  }

  agentButtons.forEach((button) => {
    button.addEventListener("click", () => selectAgent(button));
  });

  /* ------------------------------------------------------- worked examples */

  function selectExample(button) {
    exampleButtons.forEach((candidate) => {
      const selected = candidate === button;
      candidate.classList.toggle("is-active", selected);
      candidate.setAttribute("aria-pressed", String(selected));
    });
    previewFrame.src = button.dataset.exampleHtml;
    previewFrame.title = button.dataset.exampleTitle;
    previewFilename.textContent = button.dataset.exampleFile;
    previewJson.href = button.dataset.exampleJson;
    previewHtml.href = button.dataset.exampleHtml;
    previewOpen.href = button.dataset.exampleHtml;
  }

  exampleButtons.forEach((button) => {
    button.addEventListener("click", () => selectExample(button));
  });

  /* -------------------------------------------------------- copy commands */

  let copyTimer = 0;

  copyButtons.forEach((button) => {
    button.addEventListener("click", async () => {
      const source = document.getElementById(button.dataset.copy);
      try {
        await navigator.clipboard.writeText(source.textContent.trim());
        const label = button.dataset.copyLabel || "text";
        copyStatus.textContent = `${label[0].toUpperCase()}${label.slice(1)} copied.`;
        button.textContent = "Copied";
        button.classList.add("is-done");
      } catch (_) {
        copyStatus.textContent = "Copy unavailable. Select the command manually.";
      }
      window.clearTimeout(copyTimer);
      copyTimer = window.setTimeout(() => {
        copyStatus.textContent = "";
        button.textContent = "Copy";
        button.classList.remove("is-done");
      }, 2400);
    });
  });

  /* ------------------------------------------------------------- masthead */

  if ("IntersectionObserver" in window) {
    new IntersectionObserver(
      ([entry]) => masthead.classList.toggle("is-lifted", !entry.isIntersecting),
      { rootMargin: "-64px 0px 0px 0px" }
    ).observe(hero);
  }

  /* ---------------------------------------------------------------- sky */

  // The poster already paints the hero. The shader is an upgrade, so it only
  // loads where it can run well: skip it on metered connections, on machines
  // with little to spare, and anywhere WebGL is unavailable.
  function shaderIsWorthwhile() {
    if (!shader) return false;
    if (navigator.connection && navigator.connection.saveData) return false;
    if (typeof navigator.deviceMemory === "number" && navigator.deviceMemory < 4) return false;
    try {
      const probe = document.createElement("canvas");
      return Boolean(
        window.WebGLRenderingContext &&
          (probe.getContext("webgl") || probe.getContext("experimental-webgl"))
      );
    } catch (_) {
      return false;
    }
  }

  // Portrait screens get a sparser, slower field: less to read through, and
  // less to draw on a phone GPU.
  const narrow = window.matchMedia("(max-width: 760px)");

  function skyParams() {
    return narrow.matches
      ? { ROTATION_SPEED: 0.09, PATTERN_COMPLEXITY: 0.52, PATTERN: 0.12 }
      : { ROTATION_SPEED: 0.12, PATTERN_COMPLEXITY: 0.72, PATTERN: 0.12 };
  }

  function pushParams() {
    if (!shader.contentWindow) return;
    Object.entries(skyParams()).forEach(([name, value]) => {
      shader.contentWindow.postMessage({ type: "param", name, value }, "*");
    });
  }

  if (shaderIsWorthwhile()) {
    shader.addEventListener("load", () => {
      pushParams();
      shader.classList.add("is-live");
    });
    shader.src = "/shader/sacred-strange.html";

    narrow.addEventListener("change", pushParams);

    // Off-screen the shader has nothing to say; stop paying for its frames.
    if ("IntersectionObserver" in window) {
      new IntersectionObserver(([entry]) => {
        if (!shader.contentWindow) return;
        shader.contentWindow.postMessage({ type: "run", value: entry.isIntersecting }, "*");
      }).observe(hero);
    }
  }
})();
