const state = {
  payload: null,
  selectedId: null,
  currentStep: 0,
  timerId: null,
};

const elements = {
  pageTitle: document.getElementById("page-title"),
  pageSubtitle: document.getElementById("page-subtitle"),
  buttons: document.getElementById("algorithm-buttons"),
  title: document.getElementById("algorithm-title"),
  kicker: document.getElementById("algorithm-kicker"),
  description: document.getElementById("algorithm-description"),
  metaChips: document.getElementById("meta-chips"),
  stage: document.getElementById("stage"),
  playButton: document.getElementById("play-button"),
  resetButton: document.getElementById("reset-button"),
  stepRange: document.getElementById("step-range"),
  speedSelect: document.getElementById("speed-select"),
  customForm: document.getElementById("custom-form"),
  customFields: document.getElementById("custom-fields"),
  customError: document.getElementById("custom-error"),
  defaultsButton: document.getElementById("defaults-button"),
  stepMessage: document.getElementById("step-message"),
  codeList: document.getElementById("code-list"),
};

const getSelectedAlgorithm = () =>
  state.payload.algorithms.find((algorithm) => algorithm.id === state.selectedId);

const stopPlayback = () => {
  if (state.timerId !== null) {
    window.clearInterval(state.timerId);
    state.timerId = null;
  }
  elements.playButton.textContent = "播放";
};

const renderMeta = (algorithm) => {
  elements.metaChips.innerHTML = "";
  Object.entries(algorithm.meta || {}).forEach(([key, value]) => {
    const chip = document.createElement("div");
    chip.className = "meta-chip";
    chip.textContent = `${key}: ${Array.isArray(value) ? value.join(", ") : value}`;
    elements.metaChips.appendChild(chip);
  });
};

const renderCode = (algorithm) => {
  elements.codeList.innerHTML = "";
  algorithm.code.forEach((line) => {
    const item = document.createElement("li");
    item.textContent = line;
    elements.codeList.appendChild(item);
  });
};

const renderCustomInputs = (algorithm) => {
  elements.customFields.innerHTML = "";
  elements.customError.hidden = true;
  elements.customError.textContent = "";

  (algorithm.controls || []).forEach((control) => {
    const field = document.createElement("div");
    field.className = "field-group";

    const label = document.createElement("label");
    label.htmlFor = `control-${control.name}`;
    label.textContent = control.label;

    const input = document.createElement("input");
    input.id = `control-${control.name}`;
    input.name = control.name;
    input.type = control.type || "text";
    if (control.placeholder) {
      input.placeholder = control.placeholder;
    }
    if (control.min !== undefined) {
      input.min = String(control.min);
    }
    if (control.max !== undefined) {
      input.max = String(control.max);
    }
    if (control.step !== undefined) {
      input.step = String(control.step);
    }

    const value = algorithm.meta[control.name];
    input.value = Array.isArray(value) ? value.join(",") : String(value ?? "");

    field.appendChild(label);
    field.appendChild(input);
    elements.customFields.appendChild(field);
  });
};

const renderButtons = () => {
  elements.buttons.innerHTML = "";
  state.payload.algorithms.forEach((algorithm) => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = `algorithm-button${algorithm.id === state.selectedId ? " active" : ""}`;
    button.innerHTML = `<strong>${algorithm.title}</strong><span>${algorithm.description}</span>`;
    button.addEventListener("click", () => {
      stopPlayback();
      state.selectedId = algorithm.id;
      state.currentStep = 0;
      render();
    });
    elements.buttons.appendChild(button);
  });
};

const createStatGrid = (items) => {
  const grid = document.createElement("div");
  grid.className = "stat-grid";
  items.forEach(([label, value]) => {
    const card = document.createElement("div");
    card.className = "stat-card";
    card.innerHTML = `<small>${label}</small><strong>${value}</strong>`;
    grid.appendChild(card);
  });
  return grid;
};

const renderNQueens = (algorithm, step) => {
  const size = algorithm.meta.size;
  const wrapper = document.createElement("div");
  const board = document.createElement("div");
  board.className = "board";
  board.style.gridTemplateRows = `repeat(${size}, 1fr)`;

  for (let row = 0; row < size; row += 1) {
    const rowElement = document.createElement("div");
    rowElement.className = "board-row";
    rowElement.style.gridTemplateColumns = `repeat(${size}, 1fr)`;

    for (let col = 0; col < size; col += 1) {
      const cell = document.createElement("div");
      const isDark = (row + col) % 2 === 1;
      cell.className = `cell${isDark ? " dark" : ""}`;

      if (step.queens[row] === col) {
        cell.classList.add("queen");
        cell.textContent = "♛";
      }
      if (step.row === row && step.col === col) {
        cell.classList.add("focus");
        if (step.action === "reject") {
          cell.classList.add("reject");
          cell.textContent = "×";
        }
      }
      rowElement.appendChild(cell);
    }

    board.appendChild(rowElement);
  }

  wrapper.appendChild(
    createStatGrid([
      ["棋盘规模", `${size} x ${size}`],
      ["当前已放置", `${step.queens.length}`],
      ["已找到解", `${step.solutions}`],
    ]),
  );
  wrapper.appendChild(board);
  return wrapper;
};

const renderSubsetSum = (algorithm, step) => {
  const wrapper = document.createElement("div");
  wrapper.className = "subset-layout";
  const numbers = algorithm.meta.numbers;

  const stats = createStatGrid([
    ["目标值", `${algorithm.meta.target}`],
    ["剩余值", `${step.remain}`],
    ["当前子集和", `${step.subset.reduce((total, value) => total + value, 0)}`],
  ]);
  wrapper.appendChild(stats);

  const strip = document.createElement("div");
  strip.className = "number-strip";
  numbers.forEach((value, index) => {
    const token = document.createElement("div");
    token.className = "token";
    token.textContent = value;
    if (step.selected_indexes.includes(index)) {
      token.classList.add("active");
    } else if (index === step.index) {
      token.classList.add("current");
    } else if (index < step.index) {
      token.classList.add("muted");
    }
    strip.appendChild(token);
  });

  const subsetTitle = document.createElement("p");
  subsetTitle.className = "viewer-description";
  subsetTitle.textContent = `当前路径：${step.subset.length ? step.subset.join(" + ") : "空集"}`;

  wrapper.appendChild(strip);
  wrapper.appendChild(subsetTitle);
  return wrapper;
};

const renderPermutations = (algorithm, step) => {
  const wrapper = document.createElement("div");
  wrapper.className = "permutation-layout";
  const items = algorithm.meta.items;

  wrapper.appendChild(
    createStatGrid([
      ["原始数组", items.join(", ")],
      ["路径长度", `${step.path.length}`],
      ["已生成排列", `${step.completed}`],
    ]),
  );

  const pathStrip = document.createElement("div");
  pathStrip.className = "path-strip";
  step.path.forEach((value) => {
    const token = document.createElement("div");
    token.className = "token active";
    token.textContent = value;
    pathStrip.appendChild(token);
  });
  if (step.path.length === 0) {
    const empty = document.createElement("div");
    empty.className = "token muted";
    empty.textContent = "空路径";
    pathStrip.appendChild(empty);
  }

  const remainingStrip = document.createElement("div");
  remainingStrip.className = "remaining-strip";
  items.forEach((value, index) => {
    const token = document.createElement("div");
    token.className = "token";
    token.textContent = value;
    if (step.used[index]) {
      token.classList.add("muted");
    } else if (index === step.index) {
      token.classList.add("current");
    }
    remainingStrip.appendChild(token);
  });

  const pathTitle = document.createElement("p");
  pathTitle.className = "viewer-description";
  pathTitle.textContent = "当前排列路径";

  const remainingTitle = document.createElement("p");
  remainingTitle.className = "viewer-description";
  remainingTitle.textContent = "还可选择的元素";

  wrapper.appendChild(pathTitle);
  wrapper.appendChild(pathStrip);
  wrapper.appendChild(remainingTitle);
  wrapper.appendChild(remainingStrip);
  return wrapper;
};

const renderStage = (algorithm, step) => {
  elements.stage.innerHTML = "";
  if (algorithm.id === "n-queens") {
    elements.stage.appendChild(renderNQueens(algorithm, step));
    return;
  }
  if (algorithm.id === "subset-sum") {
    elements.stage.appendChild(renderSubsetSum(algorithm, step));
    return;
  }
  elements.stage.appendChild(renderPermutations(algorithm, step));
};

const render = () => {
  renderButtons();
  const algorithm = getSelectedAlgorithm();
  const step = algorithm.steps[state.currentStep];

  elements.kicker.textContent = `Step ${state.currentStep + 1} / ${algorithm.steps.length}`;
  elements.title.textContent = algorithm.title;
  elements.description.textContent = algorithm.description;
  elements.stepMessage.textContent = step.message;
  elements.stepRange.max = String(algorithm.steps.length - 1);
  elements.stepRange.value = String(state.currentStep);

  renderMeta(algorithm);
  renderCode(algorithm);
  renderCustomInputs(algorithm);
  renderStage(algorithm, step);
};

const replaceSelectedAlgorithm = (nextAlgorithm) => {
  state.payload.algorithms = state.payload.algorithms.map((algorithm) =>
    algorithm.id === nextAlgorithm.id ? nextAlgorithm : algorithm,
  );
};

const buildAlgorithmQuery = (algorithmId, values) => {
  const query = new URLSearchParams({ algorithm: algorithmId });
  Object.entries(values).forEach(([key, value]) => {
    if (value !== "") {
      query.set(key, value);
    }
  });
  return query.toString();
};

const collectCustomValues = () => {
  const formData = new FormData(elements.customForm);
  return Object.fromEntries(formData.entries());
};

const applyCustomInputs = async (values) => {
  const algorithm = getSelectedAlgorithm();
  const query = buildAlgorithmQuery(algorithm.id, values);
  const response = await fetch(`/api/algorithm?${query}`);
  const payload = await response.json();

  if (!response.ok) {
    throw new Error(payload.error || "自定义输入加载失败");
  }

  stopPlayback();
  state.currentStep = 0;
  replaceSelectedAlgorithm(payload);
  render();
};

const play = () => {
  const delay = Number(elements.speedSelect.value);
  const algorithm = getSelectedAlgorithm();

  if (state.currentStep >= algorithm.steps.length - 1) {
    state.currentStep = 0;
  }

  elements.playButton.textContent = "暂停";
  state.timerId = window.setInterval(() => {
    if (state.currentStep >= algorithm.steps.length - 1) {
      stopPlayback();
      return;
    }
    state.currentStep += 1;
    render();
  }, delay);
};

const wireControls = () => {
  elements.playButton.addEventListener("click", () => {
    if (state.timerId !== null) {
      stopPlayback();
      return;
    }
    play();
  });

  elements.resetButton.addEventListener("click", () => {
    stopPlayback();
    state.currentStep = 0;
    render();
  });

  elements.stepRange.addEventListener("input", (event) => {
    stopPlayback();
    state.currentStep = Number(event.target.value);
    render();
  });

  elements.speedSelect.addEventListener("change", () => {
    if (state.timerId !== null) {
      stopPlayback();
      play();
    }
  });

  elements.customForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    try {
      await applyCustomInputs(collectCustomValues());
    } catch (error) {
      elements.customError.hidden = false;
      elements.customError.textContent = error.message;
    }
  });

  elements.defaultsButton.addEventListener("click", async () => {
    try {
      await applyCustomInputs({});
    } catch (error) {
      elements.customError.hidden = false;
      elements.customError.textContent = error.message;
    }
  });
};

const bootstrap = async () => {
  const response = await fetch("/api/data");
  state.payload = await response.json();
  state.selectedId = state.payload.algorithms[0].id;

  elements.pageTitle.textContent = state.payload.title;
  elements.pageSubtitle.textContent = state.payload.subtitle;

  wireControls();
  render();
};

bootstrap().catch((error) => {
  elements.stage.innerHTML = `<p>加载失败：${error.message}</p>`;
});
