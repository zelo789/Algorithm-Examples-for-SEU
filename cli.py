"""算法样例命令行入口。

运行方式：
python cli.py --list
python cli.py quick-sort
python cli.py all
"""

from __future__ import annotations

import argparse
from collections.abc import Callable

from algorithms.divide_conquer import (
    closest_pair,
    polynomial_multiply,
    strassen_multiply,
)
from algorithms.dynamic_programming import (
    knapsack_01,
    longest_common_subsequence,
    matrix_chain_order,
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
    quick_sort,
)
from algorithms.theory import brute_force_sat, is_3sat_formula, verify_tsp_tour


def _show(title: str, result: object) -> None:
    print(f"\n[{title}]")
    print(result)


def run_sorting() -> None:
    nums = [7, 3, 9, 1, 5, 3]
    _show("快速排序", quick_sort(nums))
    _show("归并排序", merge_sort(nums))
    _show("堆排序", heap_sort(nums))
    _show("二分查找 5", binary_search(sorted(nums), 5))
    _show("第 3 小元素", deterministic_select(nums, 3))


def run_dynamic_programming() -> None:
    _show("0/1 背包", knapsack_01([2, 2, 6, 5, 4], [6, 3, 5, 4, 6], 10))
    _show("LCS", longest_common_subsequence("ABCBDAB", "BDCABA"))
    _show("矩阵连乘", matrix_chain_order([30, 35, 15, 5, 10, 20, 25]))
    _show("钢条切割", rod_cutting([1, 5, 8, 9, 10, 17, 17, 20], 8))
    _show("概率 DP 七局四胜 p=0.55", round(series_win_probability(0.55, 4), 4))


def run_graph() -> None:
    _show("哈夫曼编码", huffman_codes({"a": 45, "b": 13, "c": 12, "d": 16, "e": 9, "f": 5}))
    _show("活动选择", activity_selection([(1, 4), (3, 5), (0, 6), (5, 7), (8, 9)]))
    _show("Kruskal MST", kruskal_mst(4, [(0, 1, 1), (0, 2, 3), (1, 2, 2), (1, 3, 4), (2, 3, 5)]))

    graph = {0: [(1, 4), (2, 1)], 1: [(3, 1)], 2: [(1, 2), (3, 5)], 3: []}
    shortest = dijkstra(graph, 0)
    _show("Dijkstra 距离", shortest.distances)
    _show("0 到 3 路径", reconstruct_path(shortest.previous, 3))


def run_divide_conquer() -> None:
    _show("最近点对", closest_pair([(0, 0), (2, 2), (3, 4), (2.1, 2.1)]))
    _show("FFT 多项式乘法", polynomial_multiply([1, 2], [3, 4]))
    _show("Strassen", strassen_multiply([[1, 2], [3, 4]], [[5, 6], [7, 8]]))


def run_theory() -> None:
    dist = [
        [0, 10, 15, 20],
        [10, 0, 35, 25],
        [15, 35, 0, 30],
        [20, 25, 30, 0],
    ]
    formula = [[1, -2, 3], [-1, 2, 3], [1, 2, -3]]
    _show("TSP Held-Karp", tsp_held_karp(dist))
    _show("是 3-SAT", is_3sat_formula(formula))
    _show("SAT 暴力解", brute_force_sat(formula))
    _show("TSP 路线验证", verify_tsp_tour(dist, [0, 1, 3, 2], 80))


COMMANDS: dict[str, tuple[str, Callable[[], None]]] = {
    "sorting": ("排序、查找、选择", run_sorting),
    "dp": ("动态规划", run_dynamic_programming),
    "graph": ("贪心与图算法", run_graph),
    "divide": ("分治、FFT、Strassen", run_divide_conquer),
    "theory": ("NP 完全、SAT、TSP", run_theory),
}


def run_all() -> None:
    for _, runner in COMMANDS.values():
        runner()


def main() -> None:
    parser = argparse.ArgumentParser(description="Python 算法样例命令行入口")
    parser.add_argument(
        "topic",
        nargs="?",
        default="all",
        help="可选：all, sorting, dp, graph, divide, theory",
    )
    parser.add_argument("--list", action="store_true", help="列出可运行主题")
    args = parser.parse_args()

    if args.list:
        for name, (description, _) in COMMANDS.items():
            print(f"{name:8s} {description}")
        print("all      运行全部示例")
        return

    if args.topic == "all":
        run_all()
        return

    command = COMMANDS.get(args.topic)
    if command is None:
        parser.error(f"未知主题：{args.topic}")
    command[1]()


if __name__ == "__main__":
    main()

