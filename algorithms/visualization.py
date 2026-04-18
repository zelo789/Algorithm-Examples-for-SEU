"""构造浏览器可视化所需的算法步骤数据。"""

from __future__ import annotations

import heapq
import random
from collections.abc import Callable

from algorithms.divide_conquer import closest_pair, polynomial_multiply, strassen_multiply
from algorithms.dynamic_programming import (
    knapsack_01,
    longest_common_subsequence,
    matrix_chain_order,
    optimal_bst,
    rod_cutting,
    series_win_probability,
    tsp_held_karp,
)
from algorithms.greedy_graph import (
    activity_selection,
    dijkstra,
    huffman_codes,
    kruskal_mst,
    reconstruct_path,
)
from algorithms.showcase import TOPICS
from algorithms.sorting_search import (
    binary_search,
    deterministic_select,
    heap_sort,
    merge_sort,
    quick_sort,
)
from algorithms.theory import brute_force_sat, is_3sat_formula, verify_tsp_tour

VisualizerAlgorithm = dict[str, object]
AlgorithmBuilder = Callable[[dict[str, object] | None], VisualizerAlgorithm]

MAX_N_QUEENS_SIZE = 6
MAX_SUBSET_SUM_ITEMS = 10
MAX_PERMUTATION_ITEMS = 6
MAX_SORT_ITEMS = 12

VISUALIZER_DEFAULTS: dict[str, dict[str, object]] = {
    "quick-sort": {"items": [7, 3, 9, 1, 5, 3]},
    "binary-search": {"items": [1, 3, 3, 5, 7, 9], "target": 5},
    "n-queens": {"n": 4},
    "subset-sum": {"numbers": [3, 34, 4, 12, 5, 2], "target": 9},
    "permutations": {"items": [1, 2, 3]},
}


def build_visualizer_payload(
    overrides: dict[str, dict[str, object]] | None = None,
) -> dict[str, object]:
    algorithms = [
        build_visualizer_algorithm(algorithm_id, (overrides or {}).get(algorithm_id))
        for algorithm_id in VISUALIZER_BUILDERS
    ]
    topic_counts: dict[str, int] = {slug: 0 for slug in TOPICS}
    for algorithm in algorithms:
        topic_counts[str(algorithm["topic"])] += 1

    topics = [
        {
            "slug": slug,
            "title": topic.title,
            "description": topic.description,
            "algorithm_count": topic_counts[slug],
        }
        for slug, topic in TOPICS.items()
    ]
    return {
        "title": "Algorithm Visualizer",
        "subtitle": "把仓库里的算法按步骤拆开，用最适合它们的方式动态观察。",
        "topics": topics,
        "algorithms": algorithms,
    }


def build_visualizer_algorithm(
    algorithm_id: str,
    overrides: dict[str, object] | None = None,
) -> VisualizerAlgorithm:
    builder = VISUALIZER_BUILDERS.get(algorithm_id)
    if builder is None:
        raise ValueError(f"unknown algorithm: {algorithm_id}")
    return builder(overrides)


def _sorting_algorithm(
    algorithm_id: str,
    title: str,
    description: str,
    meta: dict[str, object],
    steps: list[dict[str, object]],
    *,
    controls: list[dict[str, object]] | None = None,
) -> VisualizerAlgorithm:
    return {
        "id": algorithm_id,
        "topic": "sorting",
        "title": title,
        "description": description,
        "render_type": "array",
        "code": [
            "先确定当前要比较或划分的数据范围",
            "执行本轮核心操作",
            "记录中间状态，继续处理剩余部分",
            "得到最终结果后返回",
        ],
        "controls": controls or [],
        "meta": meta,
        "steps": steps,
    }


def _build_quick_sort_visualization(overrides: dict[str, object] | None = None) -> VisualizerAlgorithm:
    items = _bounded_int_list(
        _pick(overrides, "items", VISUALIZER_DEFAULTS["quick-sort"]["items"]),
        "items",
        MAX_SORT_ITEMS,
    )
    if not items:
        raise ValueError("items 不能为空")

    pivot_index = len(items) // 2
    pivot = items[pivot_index]
    less = [value for value in items if value < pivot]
    equal = [value for value in items if value == pivot]
    greater = [value for value in items if value > pivot]
    sorted_items = quick_sort(items)

    steps = [
        {
            "message": "从原数组开始，选择中间位置元素作为 pivot。",
            "items": items,
            "highlights": {"pivot": [pivot_index]},
            "stats": [["pivot", pivot], ["数组长度", len(items)]],
        },
        {
            "message": "按 pivot 把数组分成小于、等于、大于三段。",
            "items": items,
            "highlights": {
                "active": [index for index, value in enumerate(items) if value < pivot],
                "current": [index for index, value in enumerate(items) if value == pivot],
                "muted": [index for index, value in enumerate(items) if value > pivot],
            },
            "groups": [
                {"label": "less", "values": less},
                {"label": "equal", "values": equal},
                {"label": "greater", "values": greater},
            ],
            "stats": [["less", len(less)], ["equal", len(equal)], ["greater", len(greater)]],
        },
        {
            "message": "递归排好左右两边，再拼接得到最终有序数组。",
            "items": sorted_items,
            "highlights": {"sorted": list(range(len(sorted_items)))},
            "stats": [["结果", sorted_items]],
        },
    ]
    return _sorting_algorithm(
        "quick-sort",
        "快速排序",
        "用 pivot 划分数组，再递归处理左右两边。",
        {"items": items, "sorted": sorted_items},
        steps,
        controls=[
            {
                "name": "items",
                "label": "数组",
                "type": "text",
                "placeholder": "例如 7,3,9,1,5,3",
            }
        ],
    )


def _build_merge_sort_visualization(overrides: dict[str, object] | None = None) -> VisualizerAlgorithm:
    items = [7, 3, 9, 1, 5, 3]
    left = items[: len(items) // 2]
    right = items[len(items) // 2 :]
    sorted_left = merge_sort(left)
    sorted_right = merge_sort(right)
    merged = merge_sort(items)
    steps = [
        {
            "message": "先把数组递归拆成左右两半。",
            "items": items,
            "groups": [{"label": "left", "values": left}, {"label": "right", "values": right}],
        },
        {
            "message": "左右两半分别排好序。",
            "items": items,
            "groups": [
                {"label": "sorted left", "values": sorted_left},
                {"label": "sorted right", "values": sorted_right},
            ],
        },
        {
            "message": "最后按从小到大的顺序合并两个有序数组。",
            "items": merged,
            "highlights": {"sorted": list(range(len(merged)))},
        },
    ]
    return _sorting_algorithm(
        "merge-sort",
        "归并排序",
        "不断分半，最后把两个有序数组归并起来。",
        {"items": items, "sorted": merged},
        steps,
    )


def _build_heap_sort_visualization(overrides: dict[str, object] | None = None) -> VisualizerAlgorithm:
    items = [7, 3, 9, 1, 5, 3]
    heap = items.copy()
    heapq.heapify(heap)
    popped: list[int] = []
    pop_steps: list[dict[str, object]] = []
    while heap:
        popped.append(heapq.heappop(heap))
        pop_steps.append({"label": "已弹出", "values": popped.copy()})
    steps = [
        {
            "message": "先把原数组建成小根堆。",
            "items": items,
            "groups": [{"label": "heap", "values": items if not heap else sorted(items)}],
        },
        {
            "message": "不断弹出堆顶，弹出的顺序就是升序结果。",
            "items": popped,
            "groups": pop_steps[:3],
            "highlights": {"sorted": list(range(len(popped)))},
        },
    ]
    return _sorting_algorithm(
        "heap-sort",
        "堆排序",
        "利用堆顶总是最小元素的性质依次输出排序结果。",
        {"items": items, "sorted": heap_sort(items)},
        steps,
    )


def _build_binary_search_visualization(overrides: dict[str, object] | None = None) -> VisualizerAlgorithm:
    items = _bounded_int_list(
        _pick(overrides, "items", VISUALIZER_DEFAULTS["binary-search"]["items"]),
        "items",
        MAX_SORT_ITEMS,
    )
    if not items:
        raise ValueError("items 不能为空")
    items = sorted(items)
    target = _parse_int(_pick(overrides, "target", VISUALIZER_DEFAULTS["binary-search"]["target"]), "target")

    left = 0
    right = len(items) - 1
    steps: list[dict[str, object]] = []
    while left <= right:
        mid = left + (right - left) // 2
        steps.append(
            {
                "message": f"检查中点 {mid}，值为 {items[mid]}。",
                "items": items,
                "highlights": {"active": list(range(left, right + 1)), "current": [mid]},
                "stats": [["left", left], ["mid", mid], ["right", right], ["target", target]],
            }
        )
        if items[mid] == target:
            steps.append(
                {
                    "message": f"找到目标值 {target}，返回下标 {mid}。",
                    "items": items,
                    "highlights": {"sorted": [mid]},
                    "stats": [["result", mid]],
                }
            )
            break
        if items[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    else:
        steps.append(
            {
                "message": f"搜索区间为空，目标值 {target} 不存在。",
                "items": items,
                "highlights": {"muted": list(range(len(items)))},
                "stats": [["result", -1]],
            }
        )

    return _sorting_algorithm(
        "binary-search",
        "二分查找",
        "在有序数组里每一步排除掉一半搜索区间。",
        {"items": items, "target": target, "result": binary_search(items, target)},
        steps,
        controls=[
            {"name": "items", "label": "有序数组", "type": "text", "placeholder": "例如 1,3,3,5,7,9"},
            {"name": "target", "label": "目标值", "type": "number", "step": 1},
        ],
    )


def _build_deterministic_select_visualization(overrides: dict[str, object] | None = None) -> VisualizerAlgorithm:
    items = [7, 3, 9, 1, 5, 3, 8, 2, 6]
    k = 4
    groups = [items[i : i + 5] for i in range(0, len(items), 5)]
    medians = [sorted(group)[len(group) // 2] for group in groups]
    pivot = deterministic_select(medians, (len(medians) + 1) // 2)
    result = deterministic_select(items, k)
    steps = [
        {
            "message": "先把元素每 5 个分为一组。",
            "items": items,
            "groups": [{"label": f"group {index + 1}", "values": group} for index, group in enumerate(groups)],
        },
        {
            "message": "每组取中位数，再递归求这些中位数的中位数作为 pivot。",
            "items": medians,
            "highlights": {"pivot": [medians.index(pivot)]},
            "stats": [["pivot", pivot], ["k", k]],
        },
        {
            "message": "根据 pivot 划分后，只递归进入包含第 k 小元素的一边。",
            "items": sorted(items),
            "highlights": {"sorted": [k - 1]},
            "stats": [["第 k 小", result]],
        },
    ]
    return _sorting_algorithm(
        "deterministic-select",
        "线性选择",
        "通过 Median of Medians 选较好的 pivot，保证最坏 O(n)。",
        {"items": items, "k": k, "result": result},
        steps,
    )


def _build_monte_carlo_pi_visualization(overrides: dict[str, object] | None = None) -> VisualizerAlgorithm:
    rng = random.Random(42)
    checkpoints = [200, 1000, 5000]
    inside = 0
    cards: list[dict[str, object]] = []
    for sample in range(1, checkpoints[-1] + 1):
        x = rng.random()
        y = rng.random()
        if x * x + y * y <= 1:
            inside += 1
        if sample in checkpoints:
            cards.append(
                {
                    "sample": sample,
                    "inside": inside,
                    "estimate": round(4 * inside / sample, 4),
                }
            )

    steps = [
        {
            "message": "在单位正方形中随机撒点，统计落入 1/4 圆内的比例。",
            "cards": cards[:1],
            "stats": [["样本数", cards[0]["sample"]], ["估计值", cards[0]["estimate"]]],
        },
        {
            "message": "样本数增加后，估计值会逐渐稳定。",
            "cards": cards,
            "stats": [["最终估计", cards[-1]["estimate"]]],
        },
    ]
    return {
        "id": "monte-carlo-pi",
        "topic": "sorting",
        "title": "蒙特卡洛估计 pi",
        "description": "通过随机采样观察估计值如何逼近真实圆周率。",
        "render_type": "cards",
        "code": [
            "随机生成点 (x, y)",
            "判断它是否落在四分之一圆内",
            "计算 inside / samples * 4",
        ],
        "controls": [],
        "meta": {"checkpoints": checkpoints, "estimate": cards[-1]["estimate"]},
        "steps": steps,
    }


def _matrix_algorithm(
    algorithm_id: str,
    topic: str,
    title: str,
    description: str,
    meta: dict[str, object],
    steps: list[dict[str, object]],
) -> VisualizerAlgorithm:
    return {
        "id": algorithm_id,
        "topic": topic,
        "title": title,
        "description": description,
        "render_type": "matrix",
        "code": [
            "定义状态或表格含义",
            "按依赖顺序更新表格",
            "从表格末端读取答案或还原方案",
        ],
        "controls": [],
        "meta": meta,
        "steps": steps,
    }


def _build_knapsack_visualization(overrides: dict[str, object] | None = None) -> VisualizerAlgorithm:
    weights = [2, 2, 6, 5, 4]
    values = [6, 3, 5, 4, 6]
    capacity = 10
    result = knapsack_01(weights, values, capacity)
    dp = [[0] * (capacity + 1) for _ in range(len(weights) + 1)]
    steps: list[dict[str, object]] = [
        {
            "message": "第 0 行表示还没考虑任何物品，初始化全为 0。",
            "matrix": [row.copy() for row in dp],
            "row_labels": [f"i={index}" for index in range(len(dp))],
            "col_labels": [str(col) for col in range(capacity + 1)],
        }
    ]
    for i in range(1, len(weights) + 1):
        weight = weights[i - 1]
        value = values[i - 1]
        for c in range(capacity + 1):
            dp[i][c] = dp[i - 1][c]
            if c >= weight:
                dp[i][c] = max(dp[i][c], dp[i - 1][c - weight] + value)
        steps.append(
            {
                "message": f"处理第 {i} 件物品（重量 {weight}，价值 {value}）后的状态。",
                "matrix": [row.copy() for row in dp],
                "row_labels": [f"i={index}" for index in range(len(dp))],
                "col_labels": [str(col) for col in range(capacity + 1)],
                "highlights": [[i, col] for col in range(capacity + 1)],
                "stats": [["当前最优", dp[i][capacity]]],
            }
        )

    return _matrix_algorithm(
        "knapsack-01",
        "dp",
        "0/1 背包",
        "观察 DP 表如何随着物品一行一行被填出来。",
        {"weights": weights, "values": values, "capacity": capacity, "result": result.max_value},
        steps,
    )


def _build_lcs_visualization(overrides: dict[str, object] | None = None) -> VisualizerAlgorithm:
    a = "ABCBDAB"
    b = "BDCABA"
    result = longest_common_subsequence(a, b)
    dp = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
    checkpoints = [(1, 1), (4, 4), (len(a), len(b))]
    steps: list[dict[str, object]] = []
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
            if (i, j) in checkpoints:
                steps.append(
                    {
                        "message": f"比较 a[{i - 1}]={a[i - 1]} 与 b[{j - 1}]={b[j - 1]} 后的表格。",
                        "matrix": [row.copy() for row in dp],
                        "row_labels": ["-"] + list(a),
                        "col_labels": ["-"] + list(b),
                        "highlights": [[i, j]],
                    }
                )
    steps.append(
        {
            "message": f"最终 LCS 长度为 {result.length}，其中一个解是 {result.sequence}。",
            "matrix": [row.copy() for row in dp],
            "row_labels": ["-"] + list(a),
            "col_labels": ["-"] + list(b),
            "stats": [["length", result.length], ["sequence", result.sequence]],
        }
    )
    return _matrix_algorithm(
        "lcs",
        "dp",
        "最长公共子序列",
        "用二维表记录两个前缀的最优公共子序列长度。",
        {"a": a, "b": b, "length": result.length, "sequence": result.sequence},
        steps,
    )


def _build_matrix_chain_visualization(overrides: dict[str, object] | None = None) -> VisualizerAlgorithm:
    dimensions = [30, 35, 15, 5, 10, 20, 25]
    result = matrix_chain_order(dimensions)
    n = len(dimensions) - 1
    dp = [[0] * n for _ in range(n)]
    steps: list[dict[str, object]] = []
    for length in range(2, n + 1):
        for i in range(0, n - length + 1):
            j = i + length - 1
            best = float("inf")
            for k in range(i, j):
                cost = dp[i][k] + dp[k + 1][j] + dimensions[i] * dimensions[k + 1] * dimensions[j + 1]
                best = min(best, cost)
            dp[i][j] = int(best)
        steps.append(
            {
                "message": f"处理链长为 {length} 的所有子问题。",
                "matrix": [row.copy() for row in dp],
                "row_labels": [f"A{index + 1}" for index in range(n)],
                "col_labels": [f"A{index + 1}" for index in range(n)],
            }
        )
    steps.append(
        {
            "message": f"最终最小代价为 {result.min_cost}，最优括号化为 {result.parenthesization}。",
            "matrix": [row.copy() for row in dp],
            "row_labels": [f"A{index + 1}" for index in range(n)],
            "col_labels": [f"A{index + 1}" for index in range(n)],
            "stats": [["min cost", result.min_cost], ["plan", result.parenthesization]],
        }
    )
    return _matrix_algorithm(
        "matrix-chain",
        "dp",
        "矩阵连乘",
        "通过区间 DP 比较不同断点带来的乘法代价。",
        {"dimensions": dimensions, "min_cost": result.min_cost, "plan": result.parenthesization},
        steps,
    )


def _build_rod_cutting_visualization(overrides: dict[str, object] | None = None) -> VisualizerAlgorithm:
    prices = [1, 5, 8, 9, 10, 17, 17, 20]
    length = 8
    result = rod_cutting(prices, length)
    dp = [0] * (length + 1)
    steps: list[dict[str, object]] = []
    for current in range(1, length + 1):
        best = 0
        for cut in range(1, current + 1):
            best = max(best, prices[cut - 1] + dp[current - cut])
        dp[current] = best
        steps.append(
            {
                "message": f"求长度 {current} 的最优收益。",
                "items": dp.copy(),
                "highlights": {"current": [current]},
                "stats": [["best revenue", dp[current]]],
            }
        )
    return _sorting_algorithm(
        "rod-cutting",
        "钢条切割",
        "一维 DP：枚举第一刀长度，逐步填出每个长度的最优收益。",
        {"prices": prices, "length": length, "result": result.max_revenue},
        steps,
    ) | {"topic": "dp"}


def _build_series_probability_visualization(overrides: dict[str, object] | None = None) -> VisualizerAlgorithm:
    p = 0.55
    need_wins = 4
    result = series_win_probability(p, need_wins)
    dp = [[0.0] * (need_wins + 1) for _ in range(need_wins + 1)]
    for j in range(need_wins + 1):
        dp[need_wins][j] = 1.0
    for i in range(need_wins):
        dp[i][need_wins] = 0.0
    steps = [
        {
            "message": "先初始化边界：我方已达标时概率为 1，对方已达标时概率为 0。",
            "matrix": [[round(value, 3) for value in row] for row in dp],
            "row_labels": [str(index) for index in range(need_wins + 1)],
            "col_labels": [str(index) for index in range(need_wins + 1)],
        }
    ]
    for i in range(need_wins - 1, -1, -1):
        for j in range(need_wins - 1, -1, -1):
            dp[i][j] = p * dp[i + 1][j] + (1 - p) * dp[i][j + 1]
        steps.append(
            {
                "message": f"填完我方已赢 {i} 场这一行。",
                "matrix": [[round(value, 3) for value in row] for row in dp],
                "row_labels": [str(index) for index in range(need_wins + 1)],
                "col_labels": [str(index) for index in range(need_wins + 1)],
            }
        )
    steps.append(
        {
            "message": f"系列赛开始时，我方最终获胜概率为 {result:.4f}。",
            "matrix": [[round(value, 3) for value in row] for row in dp],
            "row_labels": [str(index) for index in range(need_wins + 1)],
            "col_labels": [str(index) for index in range(need_wins + 1)],
            "stats": [["p", p], ["result", round(result, 4)]],
        }
    )
    return _matrix_algorithm(
        "series-win-probability",
        "dp",
        "概率 DP",
        "用比分状态表倒推系列赛最终胜率。",
        {"p": p, "need_wins": need_wins, "result": round(result, 6)},
        steps,
    )


def _build_optimal_bst_visualization(overrides: dict[str, object] | None = None) -> VisualizerAlgorithm:
    success_prob = [0.15, 0.10, 0.05]
    fail_prob = [0.05, 0.10, 0.05, 0.05]
    result = optimal_bst(success_prob, fail_prob)
    n = len(success_prob)
    e = [[0.0] * (n + 2) for _ in range(n + 2)]
    w = [[0.0] * (n + 2) for _ in range(n + 2)]
    root = [[0] * (n + 1) for _ in range(n + 1)]
    for i in range(1, n + 2):
        e[i][i - 1] = fail_prob[i - 1]
        w[i][i - 1] = fail_prob[i - 1]
    steps: list[dict[str, object]] = []
    for length in range(1, n + 1):
        for i in range(1, n - length + 2):
            j = i + length - 1
            e[i][j] = float("inf")
            w[i][j] = w[i][j - 1] + success_prob[j - 1] + fail_prob[j]
            for r in range(i, j + 1):
                cost = e[i][r - 1] + e[r + 1][j] + w[i][j]
                if cost < e[i][j]:
                    e[i][j] = cost
                    root[i][j] = r
        steps.append(
            {
                "message": f"处理区间长度为 {length} 的最优 BST。",
                "matrix": [[round(e[i][j], 3) for j in range(n + 1)] for i in range(1, n + 2)],
                "row_labels": [str(i) for i in range(1, n + 2)],
                "col_labels": [str(j) for j in range(n + 1)],
            }
        )
    steps.append(
        {
            "message": f"最终期望代价为 {result.min_expected_cost:.3f}。",
            "matrix": [row[1:] for row in result.root_table[1:]],
            "row_labels": [str(i) for i in range(1, n + 1)],
            "col_labels": [str(j) for j in range(1, n + 1)],
            "stats": [["expected cost", round(result.min_expected_cost, 4)]],
        }
    )
    return _matrix_algorithm(
        "optimal-bst",
        "dp",
        "最优 BST",
        "区间 DP：为每段关键字选择根，最小化整体期望代价。",
        {"success_prob": success_prob, "fail_prob": fail_prob, "cost": result.min_expected_cost},
        steps,
    )


def _graph_algorithm(
    algorithm_id: str,
    title: str,
    description: str,
    meta: dict[str, object],
    steps: list[dict[str, object]],
) -> VisualizerAlgorithm:
    return {
        "id": algorithm_id,
        "topic": "graph",
        "title": title,
        "description": description,
        "render_type": "graph",
        "code": [
            "维护图上的状态",
            "每一步只更新最关键的一部分边或点",
            "把结果逐步累积成最终解",
        ],
        "controls": [],
        "meta": meta,
        "steps": steps,
    }


def _build_huffman_visualization(overrides: dict[str, object] | None = None) -> VisualizerAlgorithm:
    frequencies = {"a": 45, "b": 13, "c": 12, "d": 16, "e": 9, "f": 5}
    codes = huffman_codes(frequencies)
    forest = [[char, freq] for char, freq in sorted(frequencies.items(), key=lambda item: item[1])]
    step_forest = [
        {"label": "初始森林", "values": [f"{char}:{freq}" for char, freq in forest]},
        {"label": "先合并最小两个", "values": ["f:5", "e:9", "-> 14"]},
        {"label": "继续合并直到只剩一棵树", "values": [f"{char}:{code}" for char, code in codes.items()]},
    ]
    steps = [
        {
            "message": "开始时，每个字符都是一棵独立的树。",
            "nodes": [{"id": char, "label": f"{char}:{freq}", "status": "default"} for char, freq in frequencies.items()],
            "cards": step_forest[:1],
        },
        {
            "message": "每一步都合并当前频率最小的两棵树。",
            "nodes": [{"id": char, "label": f"{char}:{freq}", "status": "active"} for char, freq in frequencies.items()],
            "cards": step_forest[:2],
        },
        {
            "message": "最终得到一棵哈夫曼树，并读出前缀码。",
            "nodes": [{"id": char, "label": f"{char}:{code}", "status": "selected"} for char, code in codes.items()],
            "cards": step_forest,
        },
    ]
    return _graph_algorithm(
        "huffman-codes",
        "哈夫曼编码",
        "不断合并最小权值树，最终构造最优前缀码。",
        {"frequencies": frequencies, "codes": codes},
        steps,
    )


def _build_activity_selection_visualization(overrides: dict[str, object] | None = None) -> VisualizerAlgorithm:
    activities = [(1, 4), (3, 5), (0, 6), (5, 7), (8, 9)]
    sorted_activities = sorted(activities, key=lambda item: item[1])
    selected = activity_selection(activities)
    steps = [
        {
            "message": "先按结束时间从早到晚排序。",
            "items": [f"{start}-{finish}" for start, finish in sorted_activities],
            "groups": [{"label": "按结束时间排序", "values": [f"{start}-{finish}" for start, finish in sorted_activities]}],
        },
        {
            "message": "从前往后扫描，只要活动与已选集合兼容就选上。",
            "items": [f"{start}-{finish}" for start, finish in sorted_activities],
            "groups": [{"label": "selected", "values": [f"{start}-{finish}" for start, finish in selected]}],
        },
    ]
    return {
        "id": "activity-selection",
        "topic": "graph",
        "title": "活动选择",
        "description": "总是选择结束最早且与当前集合兼容的活动。",
        "render_type": "array",
        "code": [
            "按结束时间排序",
            "从前往后扫描活动",
            "兼容就加入答案",
        ],
        "controls": [],
        "meta": {"activities": activities, "selected": selected},
        "steps": steps,
    }


def _build_kruskal_visualization(overrides: dict[str, object] | None = None) -> VisualizerAlgorithm:
    edges = [(0, 1, 1), (0, 2, 3), (1, 2, 2), (1, 3, 4), (2, 3, 5)]
    mst = kruskal_mst(4, edges)
    sorted_edges = sorted(edges, key=lambda edge: edge[2])
    steps = [
        {
            "message": "先按边权从小到大排序。",
            "nodes": [{"id": str(node), "label": f"v{node}", "status": "default"} for node in range(4)],
            "edges": [
                {"from": u, "to": v, "label": str(weight), "status": "default"} for u, v, weight in sorted_edges
            ],
        },
        {
            "message": "依次尝试加入最小边，只要不成环就保留。",
            "nodes": [{"id": str(node), "label": f"v{node}", "status": "default"} for node in range(4)],
            "edges": [
                {
                    "from": u,
                    "to": v,
                    "label": str(weight),
                    "status": "selected" if (u, v, weight) in mst.edges else "muted",
                }
                for u, v, weight in sorted_edges
            ],
            "stats": [["total weight", mst.total_weight]],
        },
    ]
    return _graph_algorithm(
        "kruskal",
        "Kruskal 最小生成树",
        "把边按权值排序后，用并查集避开成环边。",
        {"edges": edges, "mst": mst.total_weight},
        steps,
    )


def _build_dijkstra_visualization(overrides: dict[str, object] | None = None) -> VisualizerAlgorithm:
    graph = {0: [(1, 4), (2, 1)], 1: [(3, 1)], 2: [(1, 2), (3, 5)], 3: []}
    result = dijkstra(graph, 0)
    path = reconstruct_path(result.previous, 3)
    steps = [
        {
            "message": "初始化时，源点距离为 0，其他点为无穷大。",
            "nodes": [
                {"id": str(node), "label": f"v{node}:{result.distances[node] if node == 0 else '∞'}", "status": "default"}
                for node in range(4)
            ],
            "edges": [
                {"from": u, "to": v, "label": str(weight), "status": "default"}
                for u, neighbors in graph.items()
                for v, weight in neighbors
            ],
        },
        {
            "message": "每次从优先队列中取出当前距离最小的点，松弛它的出边。",
            "nodes": [
                {"id": str(node), "label": f"v{node}:{result.distances[node]}", "status": "active" if node in path else "default"}
                for node in range(4)
            ],
            "edges": [
                {
                    "from": u,
                    "to": v,
                    "label": str(weight),
                    "status": "selected" if [u, v] in list(zip(path, path[1:])) else "default",
                }
                for u, neighbors in graph.items()
                for v, weight in neighbors
            ],
        },
        {
            "message": f"最终从 0 到 3 的最短路径是 {path}，距离为 {result.distances[3]}。",
            "nodes": [
                {"id": str(node), "label": f"v{node}:{result.distances[node]}", "status": "selected" if node in path else "muted"}
                for node in range(4)
            ],
            "edges": [
                {
                    "from": u,
                    "to": v,
                    "label": str(weight),
                    "status": "selected" if [u, v] in list(zip(path, path[1:])) else "muted",
                }
                for u, neighbors in graph.items()
                for v, weight in neighbors
            ],
            "stats": [["path", path], ["distance", result.distances[3]]],
        },
    ]
    return _graph_algorithm(
        "dijkstra",
        "Dijkstra 最短路",
        "从源点开始，不断确定当前距离最小的未确定点。",
        {"graph": graph, "distances": result.distances, "path": path},
        steps,
    )


def _build_closest_pair_visualization(overrides: dict[str, object] | None = None) -> VisualizerAlgorithm:
    points = [(0, 0), (2, 2), (3, 4), (2.1, 2.1)]
    distance, pair = closest_pair(points)
    mid_x = sorted(points)[len(points) // 2][0]
    steps = [
        {
            "message": "先按 x 坐标把点分成左右两半。",
            "points": [
                {"x": x, "y": y, "label": f"({x},{y})", "status": "active" if x <= mid_x else "default"} for x, y in points
            ],
            "stats": [["mid x", mid_x]],
        },
        {
            "message": "分别计算左右部分的最近距离，再检查中线附近的条带。",
            "points": [
                {"x": x, "y": y, "label": f"({x},{y})", "status": "current" if pair and (x, y) in pair else "default"} for x, y in points
            ],
        },
        {
            "message": f"最终最近点对是 {pair}，距离约为 {distance:.4f}。",
            "points": [
                {"x": x, "y": y, "label": f"({x},{y})", "status": "selected" if pair and (x, y) in pair else "muted"} for x, y in points
            ],
            "stats": [["pair", pair], ["distance", round(distance, 4)]],
        },
    ]
    return {
        "id": "closest-pair",
        "topic": "divide",
        "title": "最近点对",
        "description": "分治处理左右两部分，再检查中线附近的候选点。",
        "render_type": "points",
        "code": [
            "按 x 排序并分成左右两半",
            "分别求左右内部最近距离",
            "在中线附近的条带里补充检查",
        ],
        "controls": [],
        "meta": {"points": points, "pair": pair, "distance": distance},
        "steps": steps,
    }


def _build_polynomial_multiply_visualization(overrides: dict[str, object] | None = None) -> VisualizerAlgorithm:
    a = [1, 2]
    b = [3, 4]
    result = polynomial_multiply(a, b)
    steps = [
        {
            "message": "把两个多项式补齐到同样长度，并映射到点值表示。",
            "items": a + b,
            "groups": [{"label": "A", "values": a}, {"label": "B", "values": b}],
        },
        {
            "message": "在点值表示下逐点相乘，再做逆变换恢复系数。",
            "items": result,
            "groups": [{"label": "结果系数", "values": result}],
        },
    ]
    return {
        "id": "polynomial-multiply",
        "topic": "divide",
        "title": "FFT 多项式乘法",
        "description": "先做 FFT，再把点值相乘，最后用逆 FFT 恢复系数。",
        "render_type": "array",
        "code": [
            "把系数补齐到 2 的幂长度",
            "对两个多项式分别做 FFT",
            "逐点相乘后做逆变换",
        ],
        "controls": [],
        "meta": {"a": a, "b": b, "result": result},
        "steps": steps,
    }


def _build_strassen_visualization(overrides: dict[str, object] | None = None) -> VisualizerAlgorithm:
    a = [[1, 2], [3, 4]]
    b = [[5, 6], [7, 8]]
    result = strassen_multiply(a, b)
    steps = [
        {
            "message": "先把矩阵按象限拆成四块。",
            "matrix": a,
            "row_labels": ["r1", "r2"],
            "col_labels": ["c1", "c2"],
            "stats": [["A", a], ["B", b]],
        },
        {
            "message": "用 7 次子矩阵乘法替代普通分块乘法里的 8 次。",
            "matrix": [[7, 0], [0, 7]],
            "row_labels": ["M", " "],
            "col_labels": ["次数", " "],
            "stats": [["思想", "7 次子乘法 + 若干加减法"]],
        },
        {
            "message": "组合 7 个中间结果，恢复最终矩阵乘积。",
            "matrix": result,
            "row_labels": ["r1", "r2"],
            "col_labels": ["c1", "c2"],
        },
    ]
    return _matrix_algorithm(
        "strassen",
        "divide",
        "Strassen 矩阵乘法",
        "利用更少的子矩阵乘法降低渐进复杂度。",
        {"a": a, "b": b, "result": result},
        steps,
    )


def _build_sat_solver_visualization(overrides: dict[str, object] | None = None) -> VisualizerAlgorithm:
    formula = [[1, -2, 3], [-1, 2, 3], [1, 2, -3]]
    assignment = brute_force_sat(formula)
    steps = [
        {
            "message": "SAT 公式由若干子句组成，每个子句里是若干文字的“或”。",
            "clauses": formula,
            "assignment": {},
            "clause_status": ["unknown"] * len(formula),
        },
        {
            "message": "暴力求解会枚举变量赋值，并逐个检查公式是否满足。",
            "clauses": formula,
            "assignment": {1: False, 2: False, 3: False},
            "clause_status": ["fail", "pass", "fail"],
        },
        {
            "message": f"最终找到一个满足赋值：{assignment}。",
            "clauses": formula,
            "assignment": assignment or {},
            "clause_status": ["pass"] * len(formula),
        },
    ]
    return {
        "id": "sat-solver",
        "topic": "theory",
        "title": "SAT 暴力求解",
        "description": "通过枚举赋值理解 SAT 属于指数级搜索问题。",
        "render_type": "formula",
        "code": [
            "收集公式中的变量",
            "枚举所有 True / False 赋值",
            "检查当前赋值是否满足全部子句",
        ],
        "controls": [],
        "meta": {"formula": formula, "assignment": assignment},
        "steps": steps,
    }


def _build_three_sat_visualization(overrides: dict[str, object] | None = None) -> VisualizerAlgorithm:
    formula = [[1, -2, 3], [-1, 2, 3], [1, 2, -3]]
    result = is_3sat_formula(formula)
    steps = [
        {
            "message": "3-SAT 要求每个子句都恰好包含 3 个文字。",
            "clauses": formula,
            "assignment": {},
            "clause_status": ["pass" if len(clause) == 3 else "fail" for clause in formula],
        },
        {
            "message": f"当前公式的检查结果是 {result}。",
            "clauses": formula,
            "assignment": {},
            "clause_status": ["pass" if len(clause) == 3 else "fail" for clause in formula],
            "stats": [["is 3-SAT", result]],
        },
    ]
    return {
        "id": "three-sat-checker",
        "topic": "theory",
        "title": "3-SAT 形式判断",
        "description": "检查每个子句是否恰好有 3 个文字。",
        "render_type": "formula",
        "code": [
            "逐个读取子句",
            "统计子句中的文字数量",
            "只要有一个不等于 3 就返回 False",
        ],
        "controls": [],
        "meta": {"formula": formula, "result": result},
        "steps": steps,
    }


def _build_tsp_verifier_visualization(overrides: dict[str, object] | None = None) -> VisualizerAlgorithm:
    dist = [
        [0, 10, 15, 20],
        [10, 0, 35, 25],
        [15, 35, 0, 30],
        [20, 25, 30, 0],
    ]
    tour = [0, 1, 3, 2]
    limit = 80
    result = verify_tsp_tour(dist, tour, limit)
    total = sum(dist[tour[index]][tour[(index + 1) % len(tour)]] for index in range(len(tour)))
    edges = list(zip(tour, tour[1:] + [tour[0]]))
    steps = [
        {
            "message": "先检查路线是否恰好访问所有城市一次。",
            "nodes": [{"id": str(city), "label": f"city {city}", "status": "selected"} for city in tour],
            "edges": [{"from": u, "to": v, "label": str(dist[u][v]), "status": "selected"} for u, v in edges],
            "stats": [["tour", tour]],
        },
        {
            "message": f"再累加整条路线的长度，并与上界 {limit} 比较。",
            "nodes": [{"id": str(city), "label": f"city {city}", "status": "selected"} for city in tour],
            "edges": [{"from": u, "to": v, "label": str(dist[u][v]), "status": "selected"} for u, v in edges],
            "stats": [["total", total], ["limit", limit], ["valid", result]],
        },
    ]
    return {
        "id": "tsp-verifier",
        "topic": "theory",
        "title": "TSP 路线验证",
        "description": "给定一条路线，检查它是否访问所有城市且长度不超过限制。",
        "render_type": "graph",
        "code": [
            "验证 tour 是否是 0..n-1 的一个排列",
            "累加相邻城市与回到起点的距离",
            "比较总长度与限制值",
        ],
        "controls": [],
        "meta": {"tour": tour, "limit": limit, "valid": result},
        "steps": steps,
    }


def _build_tsp_dp_visualization(overrides: dict[str, object] | None = None) -> VisualizerAlgorithm:
    dist = [
        [0, 10, 15, 20],
        [10, 0, 35, 25],
        [15, 35, 0, 30],
        [20, 25, 30, 0],
    ]
    result = tsp_held_karp(dist)
    steps = [
        {
            "message": "状态 dp[(mask, j)] 表示从 0 出发，访问 mask 后停在 j 的最小代价。",
            "cards": [{"state": "(0001,0)", "cost": 0.0}],
        },
        {
            "message": "逐步扩展访问集合，把新城市加入状态。",
            "cards": [
                {"state": "(0011,1)", "cost": 10.0},
                {"state": "(0101,2)", "cost": 15.0},
                {"state": "(1001,3)", "cost": 20.0},
            ],
        },
        {
            "message": f"遍历完所有集合后，补上回到起点的代价，得到最短巡回长度 {result}。",
            "cards": [{"state": "(1111,1/2/3)", "cost": result}],
            "stats": [["result", result]],
        },
    ]
    return {
        "id": "tsp-held-karp",
        "topic": "dp",
        "title": "Held-Karp TSP",
        "description": "用状态压缩 DP 处理小规模旅行商问题。",
        "render_type": "cards",
        "code": [
            "定义 dp[(mask, j)]",
            "枚举下一个要访问的城市",
            "最后补上回到起点的代价",
        ],
        "controls": [],
        "meta": {"result": result},
        "steps": steps,
    }


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
                "stats": [["size", n], ["solutions", solutions]],
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
        "topic": "backtracking",
        "title": "N 皇后",
        "description": "观察皇后逐行放置、冲突剪枝和回溯撤销。",
        "render_type": "board",
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


def _build_subset_sum_visualization(overrides: dict[str, object] | None = None) -> VisualizerAlgorithm:
    numbers = _bounded_int_list(
        _pick(overrides, "numbers", VISUALIZER_DEFAULTS["subset-sum"]["numbers"]),
        "numbers",
        MAX_SUBSET_SUM_ITEMS,
    )
    target = _non_negative_int(_pick(overrides, "target", VISUALIZER_DEFAULTS["subset-sum"]["target"]), "target")
    if not numbers:
        raise ValueError("numbers 不能为空")
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
                "stats": [["target", target], ["remain", remain]],
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
        "topic": "backtracking",
        "title": "子集和",
        "description": "观察 DFS 如何选择、回退，并利用剩余目标值判断死路。",
        "render_type": "array",
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
        "steps": [
            {
                **step,
                "items": numbers,
                "highlights": {
                    "active": step["selected_indexes"],
                    "current": [step["index"]] if step["index"] < len(numbers) else [],
                },
            }
            for step in steps
        ],
    }


def _build_permutations_visualization(overrides: dict[str, object] | None = None) -> VisualizerAlgorithm:
    items = _bounded_int_list(
        _pick(overrides, "items", VISUALIZER_DEFAULTS["permutations"]["items"]),
        "items",
        MAX_PERMUTATION_ITEMS,
    )
    if not items:
        raise ValueError("items 不能为空")

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
                "stats": [["path length", len(path)], ["completed", completed]],
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
        "topic": "backtracking",
        "title": "全排列",
        "description": "观察路径如何逐步构造，并在返回上一层时恢复可选元素。",
        "render_type": "array",
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
        "steps": [
            {
                **step,
                "groups": [{"label": "path", "values": step["path"]}],
                "highlights": {
                    "active": [index for index, flag in enumerate(step["used"]) if flag],
                    "current": [step["index"]] if step["index"] is not None else [],
                },
            }
            for step in steps
        ],
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


def _bounded_int_list(value: object, name: str, limit: int) -> list[int]:
    items = _int_list(value, name)
    if len(items) > limit:
        raise ValueError(f"{name} 最多支持 {limit} 个元素")
    return items


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
    "quick-sort": _build_quick_sort_visualization,
    "merge-sort": _build_merge_sort_visualization,
    "heap-sort": _build_heap_sort_visualization,
    "binary-search": _build_binary_search_visualization,
    "deterministic-select": _build_deterministic_select_visualization,
    "monte-carlo-pi": _build_monte_carlo_pi_visualization,
    "knapsack-01": _build_knapsack_visualization,
    "lcs": _build_lcs_visualization,
    "matrix-chain": _build_matrix_chain_visualization,
    "rod-cutting": _build_rod_cutting_visualization,
    "series-win-probability": _build_series_probability_visualization,
    "optimal-bst": _build_optimal_bst_visualization,
    "tsp-held-karp": _build_tsp_dp_visualization,
    "huffman-codes": _build_huffman_visualization,
    "activity-selection": _build_activity_selection_visualization,
    "kruskal": _build_kruskal_visualization,
    "dijkstra": _build_dijkstra_visualization,
    "closest-pair": _build_closest_pair_visualization,
    "polynomial-multiply": _build_polynomial_multiply_visualization,
    "strassen": _build_strassen_visualization,
    "sat-solver": _build_sat_solver_visualization,
    "three-sat-checker": _build_three_sat_visualization,
    "tsp-verifier": _build_tsp_verifier_visualization,
    "n-queens": _build_n_queens_visualization,
    "subset-sum": _build_subset_sum_visualization,
    "permutations": _build_permutations_visualization,
}
