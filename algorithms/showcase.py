"""统一维护项目中的主题与示例。"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from algorithms.backtracking_search import (
    generate_permutations,
    solve_n_queens,
    subset_sum_exists,
)
from algorithms.divide_conquer import (
    closest_pair,
    polynomial_multiply,
    strassen_multiply,
)
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
from algorithms.sorting_search import (
    binary_search,
    deterministic_select,
    heap_sort,
    merge_sort,
    monte_carlo_pi,
    quick_sort,
)
from algorithms.theory import brute_force_sat, is_3sat_formula, verify_tsp_tour


@dataclass(frozen=True)
class ExampleResult:
    title: str
    value: object


@dataclass(frozen=True)
class TopicSpec:
    slug: str
    title: str
    description: str
    example_builder: Callable[[], list[ExampleResult]]


def _sorting_examples() -> list[ExampleResult]:
    nums = [7, 3, 9, 1, 5, 3]
    return [
        ExampleResult("快速排序", quick_sort(nums)),
        ExampleResult("归并排序", merge_sort(nums)),
        ExampleResult("堆排序", heap_sort(nums)),
        ExampleResult("二分查找 5", binary_search(sorted(nums), 5)),
        ExampleResult("第 3 小元素", deterministic_select(nums, 3)),
        ExampleResult("蒙特卡洛估计 pi", round(monte_carlo_pi(20_000), 4)),
    ]


def _dynamic_programming_examples() -> list[ExampleResult]:
    return [
        ExampleResult("0/1 背包", knapsack_01([2, 2, 6, 5, 4], [6, 3, 5, 4, 6], 10)),
        ExampleResult("LCS", longest_common_subsequence("ABCBDAB", "BDCABA")),
        ExampleResult("矩阵连乘", matrix_chain_order([30, 35, 15, 5, 10, 20, 25])),
        ExampleResult("钢条切割", rod_cutting([1, 5, 8, 9, 10, 17, 17, 20], 8)),
        ExampleResult("概率 DP 七局四胜 p=0.55", round(series_win_probability(0.55, 4), 4)),
        ExampleResult(
            "最优 BST",
            round(
                optimal_bst([0.15, 0.10, 0.05], [0.05, 0.10, 0.05, 0.05]).min_expected_cost,
                4,
            ),
        ),
    ]


def _graph_examples() -> list[ExampleResult]:
    graph = {0: [(1, 4), (2, 1)], 1: [(3, 1)], 2: [(1, 2), (3, 5)], 3: []}
    shortest = dijkstra(graph, 0)
    return [
        ExampleResult(
            "哈夫曼编码",
            huffman_codes({"a": 45, "b": 13, "c": 12, "d": 16, "e": 9, "f": 5}),
        ),
        ExampleResult("活动选择", activity_selection([(1, 4), (3, 5), (0, 6), (5, 7), (8, 9)])),
        ExampleResult(
            "Kruskal MST",
            kruskal_mst(4, [(0, 1, 1), (0, 2, 3), (1, 2, 2), (1, 3, 4), (2, 3, 5)]),
        ),
        ExampleResult("Dijkstra 距离", shortest.distances),
        ExampleResult("0 到 3 路径", reconstruct_path(shortest.previous, 3)),
    ]


def _divide_conquer_examples() -> list[ExampleResult]:
    return [
        ExampleResult("最近点对", closest_pair([(0, 0), (2, 2), (3, 4), (2.1, 2.1)])),
        ExampleResult("FFT 多项式乘法", polynomial_multiply([1, 2], [3, 4])),
        ExampleResult("Strassen", strassen_multiply([[1, 2], [3, 4]], [[5, 6], [7, 8]])),
    ]


def _theory_examples() -> list[ExampleResult]:
    dist = [
        [0, 10, 15, 20],
        [10, 0, 35, 25],
        [15, 35, 0, 30],
        [20, 25, 30, 0],
    ]
    formula = [[1, -2, 3], [-1, 2, 3], [1, 2, -3]]
    return [
        ExampleResult("TSP Held-Karp", tsp_held_karp(dist)),
        ExampleResult("是 3-SAT", is_3sat_formula(formula)),
        ExampleResult("SAT 暴力解", brute_force_sat(formula)),
        ExampleResult("TSP 路线验证", verify_tsp_tour(dist, [0, 1, 3, 2], 80)),
    ]


def _backtracking_examples() -> list[ExampleResult]:
    return [
        ExampleResult("4 皇后", solve_n_queens(4)),
        ExampleResult("子集和 target=9", subset_sum_exists([3, 34, 4, 12, 5, 2], 9)),
        ExampleResult("全排列 [1, 2, 3]", generate_permutations([1, 2, 3])),
    ]


TOPICS: dict[str, TopicSpec] = {
    "sorting": TopicSpec("sorting", "排序、查找、选择", "排序、查找、选择", _sorting_examples),
    "dp": TopicSpec("dp", "动态规划", "动态规划", _dynamic_programming_examples),
    "graph": TopicSpec("graph", "贪心与图算法", "贪心与图算法", _graph_examples),
    "divide": TopicSpec("divide", "分治、FFT、Strassen", "分治、FFT、Strassen", _divide_conquer_examples),
    "theory": TopicSpec("theory", "NP 完全、SAT、TSP", "NP 完全、SAT、TSP", _theory_examples),
    "backtracking": TopicSpec(
        "backtracking",
        "回溯与搜索",
        "回溯、剪枝、枚举生成",
        _backtracking_examples,
    ),
}


def list_topics() -> list[TopicSpec]:
    return list(TOPICS.values())


def build_topic_examples(slug: str) -> list[ExampleResult]:
    topic = TOPICS.get(slug)
    if topic is None:
        raise KeyError(slug)
    return topic.example_builder()
