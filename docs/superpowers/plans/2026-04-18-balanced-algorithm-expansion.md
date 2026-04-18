# Balanced Algorithm Expansion Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a backtracking topic, unify the example registry, and ship a zero-dependency browser visualizer with animated algorithm traces.

**Architecture:** Keep algorithm implementations in focused Python modules, add one shared showcase registry for `cli.py` and `demo.py`, and build a standard-library HTTP entrypoint that serves static assets plus JSON trace payloads. Visualization logic stays in the browser, while Python remains the source of truth for example data and trace generation.

**Tech Stack:** Python 3.10+, `unittest`, `http.server`, vanilla HTML/CSS/JavaScript

---

### Task 1: Add failing tests for new algorithm behaviors

**Files:**
- Modify: `tests/test_algorithms.py`

- [ ] **Step 1: Write failing tests for N 皇后、子集和、全排列和可视化 trace**
- [ ] **Step 2: Run the targeted tests and confirm they fail for missing imports/functions**
- [ ] **Step 3: Implement the minimal Python modules and public APIs**
- [ ] **Step 4: Re-run the targeted tests and confirm they pass**

### Task 2: Centralize showcase metadata

**Files:**
- Create: `algorithms/showcase.py`
- Modify: `cli.py`
- Modify: `demo.py`
- Test: `tests/test_algorithms.py`

- [ ] **Step 1: Add a failing test that exercises the shared topic registry**
- [ ] **Step 2: Run the focused test and confirm it fails because the registry does not exist**
- [ ] **Step 3: Implement the registry and migrate CLI/demo to it**
- [ ] **Step 4: Re-run focused and broader tests**

### Task 3: Add the browser visualizer

**Files:**
- Create: `algorithms/visualization.py`
- Create: `visualize.py`
- Create: `visualizer/index.html`
- Create: `visualizer/styles.css`
- Create: `visualizer/app.js`
- Test: `tests/test_algorithms.py`

- [ ] **Step 1: Add a failing test for visualization payload shape**
- [ ] **Step 2: Run the focused test and confirm it fails for missing module/function**
- [ ] **Step 3: Implement trace builders, HTTP entrypoint, and static frontend playback controls**
- [ ] **Step 4: Re-run the focused test and full suite**

### Task 4: Documentation and verification

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Update README with the new topic, visualizer command, and learning guidance**
- [ ] **Step 2: Run `python -m unittest`**
- [ ] **Step 3: Run `python cli.py --list`**
- [ ] **Step 4: Run `python visualize.py --dump-json` or equivalent smoke check**

## Self-Review

- Spec coverage: the plan covers the new topic, shared registry, browser visualizer, tests, and README updates.
- Placeholder scan: each task maps to concrete files and validation commands.
- Type consistency: algorithms return stable Python data structures, visualization payload stays JSON-serializable, and CLI/demo consume the same registry metadata.
