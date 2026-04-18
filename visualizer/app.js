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
  customizer: document.getElementById("customizer"),
  customForm: document.getElementById("custom-form"),
  customFields: document.getElementById("custom-fields"),
  customError: document.getElementById("custom-error"),
  defaultsButton: document.getElementById("defaults-button"),
  stepMessage: document.getElementById("step-message"),
  codeList: document.getElementById("code-list"),
};

const getSelectedAlgorithm = () =>
  state.payload.algorithms.find((algorithm) => algorithm.id === state.selectedId);

const toDisplay = (value) => {
  if (Array.isArray(value)) {
    return value.join(", ");
  }
  if (typeof value === "object" && value !== null) {
    return JSON.stringify(value);
  }
  return String(value);
};

const stopPlayback = () => {
  if (state.timerId !== null) {
    window.clearInterval(state.timerId);
    state.timerId = null;
  }
  elements.playButton.textContent = "播放";
};

const createStatGrid = (items = []) => {
  const grid = document.createElement("div");
  grid.className = "stat-grid";
  items.forEach(([label, value]) => {
    const card = document.createElement("div");
    card.className = "stat-card";
    card.innerHTML = `<small>${label}</small><strong>${toDisplay(value)}</strong>`;
    grid.appendChild(card);
  });
  return grid;
};

const renderMeta = (algorithm) => {
  elements.metaChips.innerHTML = "";
  Object.entries(algorithm.meta || {}).forEach(([key, value]) => {
    const chip = document.createElement("div");
    chip.className = "meta-chip";
    chip.textContent = `${key}: ${toDisplay(value)}`;
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

  const controls = algorithm.controls || [];
  elements.customizer.hidden = controls.length === 0;
  elements.customForm.hidden = controls.length === 0;
  if (controls.length === 0) {
    return;
  }

  controls.forEach((control) => {
    const field = document.createElement("div");
    field.className = "field-group";

    const label = document.createElement("label");
    label.htmlFor = `control-${control.name}`;
    label.textContent = control.label;

    const input = document.createElement("input");
    input.id = `control-${control.name}`;
    input.name = control.name;
    input.type = control.type || "text";
    if (control.placeholder) input.placeholder = control.placeholder;
    if (control.min !== undefined) input.min = String(control.min);
    if (control.max !== undefined) input.max = String(control.max);
    if (control.step !== undefined) input.step = String(control.step);

    const value = algorithm.meta[control.name];
    input.value = Array.isArray(value) ? value.join(",") : String(value ?? "");

    field.append(label, input);
    elements.customFields.appendChild(field);
  });
};

const renderButtons = () => {
  elements.buttons.innerHTML = "";

  state.payload.topics.forEach((topic) => {
    const wrapper = document.createElement("section");
    wrapper.className = "topic-group";

    const heading = document.createElement("div");
    heading.className = "topic-heading";
    heading.innerHTML = `<strong>${topic.title}</strong><span>${topic.algorithm_count} 个算法</span>`;
    wrapper.appendChild(heading);

    const list = document.createElement("div");
    list.className = "topic-buttons";

    state.payload.algorithms
      .filter((algorithm) => algorithm.topic === topic.slug)
      .forEach((algorithm) => {
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
        list.appendChild(button);
      });

    wrapper.appendChild(list);
    elements.buttons.appendChild(wrapper);
  });
};

const createTokenStrip = (items, highlights = {}) => {
  const strip = document.createElement("div");
  strip.className = "number-strip";
  const indexToClasses = new Map();

  Object.entries(highlights).forEach(([className, indexes]) => {
    (indexes || []).forEach((index) => {
      const classes = indexToClasses.get(index) || [];
      classes.push(className);
      indexToClasses.set(index, classes);
    });
  });

  items.forEach((value, index) => {
    const token = document.createElement("div");
    token.className = "token";
    token.textContent = value;
    (indexToClasses.get(index) || []).forEach((className) => token.classList.add(className));
    strip.appendChild(token);
  });
  return strip;
};

const createGroups = (groups = []) => {
  if (groups.length === 0) {
    return null;
  }

  const container = document.createElement("div");
  container.className = "group-grid";
  groups.forEach((group) => {
    const card = document.createElement("div");
    card.className = "group-card";
    card.innerHTML = `<small>${group.label}</small><strong>${(group.values || []).join(", ") || "空"}</strong>`;
    container.appendChild(card);
  });
  return container;
};

const renderArray = (algorithm, step) => {
  const wrapper = document.createElement("div");
  wrapper.className = "array-layout";
  const items = step.items || algorithm.meta.items || algorithm.meta.numbers || [];
  if (step.stats) {
    wrapper.appendChild(createStatGrid(step.stats));
  }
  if (items.length > 0) {
    wrapper.appendChild(createTokenStrip(items, step.highlights));
  }
  const groups = createGroups(step.groups);
  if (groups) {
    wrapper.appendChild(groups);
  }
  return wrapper;
};

const renderMatrix = (algorithm, step) => {
  const wrapper = document.createElement("div");
  wrapper.className = "matrix-layout";
  if (step.stats) {
    wrapper.appendChild(createStatGrid(step.stats));
  }

  const table = document.createElement("table");
  table.className = "matrix-table";

  const headRow = document.createElement("tr");
  headRow.appendChild(document.createElement("th"));
  (step.col_labels || []).forEach((label) => {
    const cell = document.createElement("th");
    cell.textContent = label;
    headRow.appendChild(cell);
  });
  table.appendChild(headRow);

  const highlighted = new Set((step.highlights || []).map(([row, col]) => `${row}-${col}`));
  (step.matrix || []).forEach((rowValues, rowIndex) => {
    const row = document.createElement("tr");
    const labelCell = document.createElement("th");
    labelCell.textContent = step.row_labels?.[rowIndex] ?? String(rowIndex);
    row.appendChild(labelCell);

    rowValues.forEach((value, colIndex) => {
      const cell = document.createElement("td");
      cell.textContent = toDisplay(value);
      if (highlighted.has(`${rowIndex}-${colIndex}`)) {
        cell.classList.add("highlight");
      }
      row.appendChild(cell);
    });
    table.appendChild(row);
  });

  wrapper.appendChild(table);
  return wrapper;
};

const renderGraph = (algorithm, step) => {
  const wrapper = document.createElement("div");
  wrapper.className = "graph-layout";
  if (step.stats) {
    wrapper.appendChild(createStatGrid(step.stats));
  }

  const nodes = document.createElement("div");
  nodes.className = "node-strip";
  (step.nodes || []).forEach((node) => {
    const chip = document.createElement("div");
    chip.className = `node-chip ${node.status || "default"}`;
    chip.textContent = node.label;
    nodes.appendChild(chip);
  });
  wrapper.appendChild(nodes);

  const edges = document.createElement("div");
  edges.className = "edge-list";
  (step.edges || []).forEach((edge) => {
    const item = document.createElement("div");
    item.className = `edge-item ${edge.status || "default"}`;
    item.textContent = `${edge.from} -> ${edge.to} (w=${edge.label})`;
    edges.appendChild(item);
  });
  wrapper.appendChild(edges);

  if (step.cards) {
    wrapper.appendChild(renderCards(algorithm, step));
  }
  return wrapper;
};

const renderFormula = (algorithm, step) => {
  const wrapper = document.createElement("div");
  wrapper.className = "formula-layout";
  if (step.stats) {
    wrapper.appendChild(createStatGrid(step.stats));
  }

  const clauses = document.createElement("div");
  clauses.className = "clause-grid";
  (step.clauses || []).forEach((clause, index) => {
    const item = document.createElement("div");
    item.className = `clause-card ${(step.clause_status || [])[index] || "unknown"}`;
    item.innerHTML = `<small>Clause ${index + 1}</small><strong>${clause.join(" OR ")}</strong>`;
    clauses.appendChild(item);
  });
  wrapper.appendChild(clauses);

  const assignment = Object.entries(step.assignment || {});
  if (assignment.length > 0) {
    const tokens = document.createElement("div");
    tokens.className = "number-strip";
    assignment.forEach(([key, value]) => {
      const token = document.createElement("div");
      token.className = `token ${value ? "active" : "muted"}`;
      token.textContent = `x${key}=${value ? "T" : "F"}`;
      tokens.appendChild(token);
    });
    wrapper.appendChild(tokens);
  }
  return wrapper;
};

const renderCards = (algorithm, step) => {
  const wrapper = document.createElement("div");
  wrapper.className = "cards-layout";
  if (step.stats) {
    wrapper.appendChild(createStatGrid(step.stats));
  }
  const cards = document.createElement("div");
  cards.className = "group-grid";
  (step.cards || []).forEach((cardData) => {
    const card = document.createElement("div");
    card.className = "group-card";
    card.innerHTML = Object.entries(cardData)
      .map(([label, value]) => `<small>${label}</small><strong>${toDisplay(value)}</strong>`)
      .join("");
    cards.appendChild(card);
  });
  wrapper.appendChild(cards);
  return wrapper;
};

const renderPoints = (algorithm, step) => {
  const wrapper = document.createElement("div");
  wrapper.className = "points-layout";
  if (step.stats) {
    wrapper.appendChild(createStatGrid(step.stats));
  }

  const width = 420;
  const height = 280;
  const padding = 24;
  const xs = step.points.map((point) => point.x);
  const ys = step.points.map((point) => point.y);
  const minX = Math.min(...xs);
  const maxX = Math.max(...xs);
  const minY = Math.min(...ys);
  const maxY = Math.max(...ys);
  const scaleX = (value) =>
    padding + ((value - minX) / Math.max(maxX - minX, 1)) * (width - padding * 2);
  const scaleY = (value) =>
    height - padding - ((value - minY) / Math.max(maxY - minY, 1)) * (height - padding * 2);

  const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
  svg.setAttribute("viewBox", `0 0 ${width} ${height}`);
  svg.classList.add("points-plane");

  step.points.forEach((point) => {
    const circle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
    circle.setAttribute("cx", scaleX(point.x));
    circle.setAttribute("cy", scaleY(point.y));
    circle.setAttribute("r", "10");
    circle.setAttribute("class", `point ${point.status || "default"}`);
    svg.appendChild(circle);

    const text = document.createElementNS("http://www.w3.org/2000/svg", "text");
    text.setAttribute("x", scaleX(point.x));
    text.setAttribute("y", scaleY(point.y) - 14);
    text.setAttribute("text-anchor", "middle");
    text.setAttribute("class", "point-label");
    text.textContent = point.label;
    svg.appendChild(text);
  });
  wrapper.appendChild(svg);
  return wrapper;
};

const renderBoard = (algorithm, step) => {
  const size = algorithm.meta.size;
  const wrapper = document.createElement("div");
  wrapper.className = "board-layout";
  if (step.stats) {
    wrapper.appendChild(createStatGrid(step.stats));
  }
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

  wrapper.appendChild(board);
  return wrapper;
};

const renderStage = (algorithm, step) => {
  elements.stage.innerHTML = "";
  const renderers = {
    array: renderArray,
    matrix: renderMatrix,
    graph: renderGraph,
    formula: renderFormula,
    cards: renderCards,
    points: renderPoints,
    board: renderBoard,
  };
  const renderer = renderers[algorithm.render_type] || renderCards;
  elements.stage.appendChild(renderer(algorithm, step));
};

const render = () => {
  renderButtons();
  const algorithm = getSelectedAlgorithm();
  const step = algorithm.steps[state.currentStep];

  elements.kicker.textContent = `${TOPICS_LABELS[algorithm.topic] || algorithm.topic} · Step ${state.currentStep + 1} / ${algorithm.steps.length}`;
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

const TOPICS_LABELS = {};

const bootstrap = async () => {
  const response = await fetch("/api/data");
  state.payload = await response.json();
  state.selectedId = state.payload.algorithms[0].id;

  state.payload.topics.forEach((topic) => {
    TOPICS_LABELS[topic.slug] = topic.title;
  });

  elements.pageTitle.textContent = state.payload.title;
  elements.pageSubtitle.textContent = state.payload.subtitle;

  wireControls();
  render();
};

bootstrap().catch((error) => {
  elements.stage.innerHTML = `<p>加载失败：${error.message}</p>`;
});
