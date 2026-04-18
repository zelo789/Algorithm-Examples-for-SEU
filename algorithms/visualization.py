"""构造浏览器可视化所需的算法步骤数据。"""

from __future__ import annotations

from collections.abc import Callable

VisualizerAlgorithm = dict[str, object]
AlgorithmBuilder = Callable[[dict[str, object] | None], VisualizerAlgorithm]

MAX_N_QUEENS_SIZE = 6
MAX_SUBSET_SUM_ITEMS = 10
MAX_PERMUTATION_ITEMS = 6

VISUALIZER_DEFAULTS: dict[str, dict[str, object]] = {
    "n-queens": {"n": 4},
    "subset-sum": {"numbers": [3, 34, 4, 12, 5, 2], "target": 9},
    "permutations": {"items": [1, 2, 3]},
}


def build_visualizer_payload(
    overrides: dict[str, dict[str, object]] | None = None,
) -> dict[str, object]:
    return {
        "title": "Algorithm Visualizer",
        "subtitle": "用动画观察回溯算法如何搜索、剪枝与回退",
        "algorithms": [
            build_visualizer_algorithm(algorithm_id, (overrides or {}).get(algorithm_id))
            for algorithm_id in VISUALIZER_BUILDERS
        ],
    }


def build_visualizer_algorithm(
    algorithm_id: str,
    overrides: dict[str, object] | None = None,
) -> VisualizerAlgorithm:
    builder = VISUALIZER_BUILDERS.get(algorithm_id)
    if builder is None:
        raise ValueError(f"unknown algorithm: {algorithm_id}")
    return builder(overrides)


def _build_n_queens_visualization(overrides: dict[str, object] | None = None) -> VisualizerAlgorithm:
    n = _positive_int(_pick(overrides, "n", VISUALIZER_DEFAULTS["n-queens"]["n"]), "n")
    if n > MAX_N_QUEENS_SIZE:
        raise ValueError(f"n 不能大于 {MAX_N_QUEENS_SIZE}")

    steps: list[dict[str, object]] = []
    placement: list[int] = []
    cols: set[int] = set()
    diag1: set[int] = set()
    diag2: set[int] = set()
    solutions = 0

    def snapshot(action: str, row: int, col: int | None, message: str) -> None:
        steps.append(
            {
                "action": action,
                "row": row,
                "col": col,
                "queens": placement.copy(),
                "message": message,
                "solutions": solutions,
            }
        )

    def backtrack(row: int) -> None:
        nonlocal solutions
        if row == n:
            solutions += 1
            snapshot("solution", row - 1, None, f"找到第 {solutions} 个解。")
            return

        for col in range(n):
            if col in cols or row - col in diag1 or row + col in diag2:
                snapshot("reject", row, col, f"第 {row + 1} 行第 {col + 1} 列冲突，跳过。")
                continue

            placement.append(col)
            cols.add(col)
            diag1.add(row - col)
            diag2.add(row + col)
            snapshot("place", row, col, f"在第 {row + 1} 行放置皇后。")

            backtrack(row + 1)

            placement.pop()
            diag2.remove(row + col)
            diag1.remove(row - col)
            cols.remove(col)
            snapshot("remove", row, col, f"回溯：撤销第 {row + 1} 行第 {col + 1} 列。")

    snapshot("start", 0, None, f"开始搜索 {n} 皇后问题。")
    backtrack(0)
    return {
        "id": "n-queens",
        "title": "N 皇后",
        "description": "观察皇后逐行放置、冲突剪枝和回溯撤销。",
        "code": [
            "逐行尝试每一列",
            "若列或对角线冲突则剪枝",
            "放置成功后递归下一行",
            "失败时撤销当前位置",
        ],
        "controls": [
            {
                "name": "n",
                "label": "棋盘规模",
                "type": "number",
                "min": 1,
                "max": MAX_N_QUEENS_SIZE,
                "step": 1,
            }
        ],
        "meta": {"size": n, "solutionCount": solutions},
        "steps": steps,
    }


def _build_subset_sum_visualization(
    overrides: dict[str, object] | None = None,
) -> VisualizerAlgorithm:
    numbers = _int_list(
        _pick(overrides, "numbers", VISUALIZER_DEFAULTS["subset-sum"]["numbers"]),
        "numbers",
    )
    target = _non_negative_int(
        _pick(overrides, "target", VISUALIZER_DEFAULTS["subset-sum"]["target"]),
        "target",
    )
    if not numbers:
        raise ValueError("numbers 不能为空")
    if len(numbers) > MAX_SUBSET_SUM_ITEMS:
        raise ValueError(f"numbers 最多支持 {MAX_SUBSET_SUM_ITEMS} 个元素")
    if any(number < 0 for number in numbers):
        raise ValueError("numbers 不能包含负数")

    steps: list[dict[str, object]] = []
    subset: list[int] = []
    selected_indexes: list[int] = []
    solved_subset: list[int] | None = None

    def snapshot(action: str, index: int, remain: int, message: str) -> None:
        steps.append(
            {
                "action": action,
                "index": index,
                "remain": remain,
                "subset": subset.copy(),
                "selected_indexes": selected_indexes.copy(),
                "message": message,
            }
        )

    def search(index: int, remain: int) -> bool:
        nonlocal solved_subset
        if remain == 0:
            solved_subset = subset.copy()
            snapshot("solution", index, remain, "找到满足目标和的子集。")
            return True
        if index == len(numbers) or remain < 0:
            snapshot("dead-end", index, remain, "无法继续满足目标，回退。")
            return False

        subset.append(numbers[index])
        selected_indexes.append(index)
        snapshot("choose", index, remain, f"选择 {numbers[index]}，继续向下搜索。")
        if search(index + 1, remain - numbers[index]):
            return True

        subset.pop()
        selected_indexes.pop()
        snapshot("undo", index, remain, f"撤销 {numbers[index]}，尝试不选它。")
        return search(index + 1, remain)

    snapshot("start", 0, target, "开始搜索子集和。")
    search(0, target)
    return {
        "id": "subset-sum",
        "title": "子集和",
        "description": "观察 DFS 如何选择、回退，并利用剩余目标值判断死路。",
        "code": [
            "从左到右决定每个数选或不选",
            "remain == 0 时找到答案",
            "remain < 0 或数组结束时回退",
            "先选当前数，再尝试跳过它",
        ],
        "controls": [
            {
                "name": "numbers",
                "label": "数字列表",
                "type": "text",
                "placeholder": "例如 3,34,4,12,5,2",
            },
            {
                "name": "target",
                "label": "目标值",
                "type": "number",
                "min": 0,
                "step": 1,
            },
        ],
        "meta": {"numbers": numbers, "target": target, "solution": solved_subset},
        "steps": steps,
    }


def _build_permutations_visualization(
    overrides: dict[str, object] | None = None,
) -> VisualizerAlgorithm:
    items = _int_list(
        _pick(overrides, "items", VISUALIZER_DEFAULTS["permutations"]["items"]),
        "items",
    )
    if not items:
        raise ValueError("items 不能为空")
    if len(items) > MAX_PERMUTATION_ITEMS:
        raise ValueError(f"items 最多支持 {MAX_PERMUTATION_ITEMS} 个元素")

    steps: list[dict[str, object]] = []
    path: list[int] = []
    used = [False] * len(items)
    completed = 0

    def snapshot(action: str, index: int | None, message: str) -> None:
        steps.append(
            {
                "action": action,
                "index": index,
                "path": path.copy(),
                "used": used.copy(),
                "message": message,
                "completed": completed,
            }
        )

    def backtrack() -> None:
        nonlocal completed
        if len(path) == len(items):
            completed += 1
            snapshot("solution", None, f"得到第 {completed} 个排列。")
            return

        for index, item in enumerate(items):
            if used[index]:
                continue
            used[index] = True
            path.append(item)
            snapshot("choose", index, f"把 {item} 放到当前排列的下一个位置。")
            backtrack()
            path.pop()
            used[index] = False
            snapshot("undo", index, f"撤销 {item}，尝试其他候选。")

    snapshot("start", None, "开始生成全排列。")
    backtrack()
    return {
        "id": "permutations",
        "title": "全排列",
        "description": "观察路径如何逐步构造，并在返回上一层时恢复可选元素。",
        "code": [
            "每层挑一个还没使用过的元素",
            "加入路径后递归处理下一位",
            "路径长度等于数组长度时得到一个排列",
            "返回上一层时恢复 used 状态",
        ],
        "controls": [
            {
                "name": "items",
                "label": "元素列表",
                "type": "text",
                "placeholder": "例如 1,2,3",
            }
        ],
        "meta": {"items": items, "count": completed},
        "steps": steps,
    }


def _pick(overrides: dict[str, object] | None, key: str, default: object) -> object:
    if overrides is None:
        return default
    return overrides.get(key, default)


def _positive_int(value: object, name: str) -> int:
    parsed = _parse_int(value, name)
    if parsed <= 0:
        raise ValueError(f"{name} 必须为正整数")
    return parsed


def _non_negative_int(value: object, name: str) -> int:
    parsed = _parse_int(value, name)
    if parsed < 0:
        raise ValueError(f"{name} 不能为负")
    return parsed


def _parse_int(value: object, name: str) -> int:
    if isinstance(value, bool):
        raise ValueError(f"{name} 必须是整数")
    try:
        return int(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{name} 必须是整数") from exc


def _int_list(value: object, name: str) -> list[int]:
    if isinstance(value, str):
        parts = [part.strip() for part in value.split(",") if part.strip()]
        if not parts:
            return []
        return [_parse_int(part, name) for part in parts]
    if isinstance(value, list):
        return [_parse_int(item, name) for item in value]
    raise ValueError(f"{name} 必须是整数列表")


VISUALIZER_BUILDERS: dict[str, AlgorithmBuilder] = {
    "n-queens": _build_n_queens_visualization,
    "subset-sum": _build_subset_sum_visualization,
    "permutations": _build_permutations_visualization,
}
