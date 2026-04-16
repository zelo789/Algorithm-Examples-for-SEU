"""运行方式：python demo.py

这个文件不是完整单元测试，而是给你快速观察算法输入输出的示例。
"""

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


def main() -> None:
    nums = [7, 3, 9, 1, 5, 3]
    print("快速排序:", quick_sort(nums))
    print("归并排序:", merge_sort(nums))
    print("堆排序:", heap_sort(nums))
    print("二分查找 5:", binary_search(sorted(nums), 5))
    print("第 3 小元素:", deterministic_select(nums, 3))

    print("0/1 背包:", knapsack_01([2, 2, 6, 5, 4], [6, 3, 5, 4, 6], 10))
    print("LCS:", longest_common_subsequence("ABCBDAB", "BDCABA"))
    print("矩阵连乘:", matrix_chain_order([30, 35, 15, 5, 10, 20, 25]))
    print("钢条切割:", rod_cutting([1, 5, 8, 9, 10, 17, 17, 20], 8))
    print("概率 DP 七局四胜 p=0.55:", round(series_win_probability(0.55, 4), 4))
    print("最优 BST:", round(optimal_bst([0.15, 0.10, 0.05], [0.05, 0.10, 0.05, 0.05]).min_expected_cost, 4))

    print("哈夫曼编码:", huffman_codes({"a": 45, "b": 13, "c": 12, "d": 16, "e": 9, "f": 5}))
    print("活动选择:", activity_selection([(1, 4), (3, 5), (0, 6), (5, 7), (8, 9)]))
    mst = kruskal_mst(4, [(0, 1, 1), (0, 2, 3), (1, 2, 2), (1, 3, 4), (2, 3, 5)])
    print("Kruskal MST:", mst)

    graph = {0: [(1, 4), (2, 1)], 1: [(3, 1)], 2: [(1, 2), (3, 5)], 3: []}
    shortest = dijkstra(graph, 0)
    print("Dijkstra 距离:", shortest.distances)
    print("0 到 3 路径:", reconstruct_path(shortest.previous, 3))

    print("最近点对:", closest_pair([(0, 0), (2, 2), (3, 4), (2.1, 2.1)]))
    print("FFT 多项式乘法:", polynomial_multiply([1, 2], [3, 4]))
    print("Strassen:", strassen_multiply([[1, 2], [3, 4]], [[5, 6], [7, 8]]))

    dist = [
        [0, 10, 15, 20],
        [10, 0, 35, 25],
        [15, 35, 0, 30],
        [20, 25, 30, 0],
    ]
    print("TSP Held-Karp:", tsp_held_karp(dist))
    formula = [[1, -2, 3], [-1, 2, 3], [1, 2, -3]]
    print("是 3-SAT:", is_3sat_formula(formula))
    print("SAT 暴力解:", brute_force_sat(formula))
    print("TSP 路线验证:", verify_tsp_tour(dist, [0, 1, 3, 2], 80))
    print("蒙特卡洛估计 pi:", round(monte_carlo_pi(20_000), 4))


if __name__ == "__main__":
    main()

