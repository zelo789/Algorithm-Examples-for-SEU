"""算法样例回归测试。

运行方式：
python -m unittest
"""

from __future__ import annotations

import math
import unittest

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
    DisjointSetUnion,
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
from algorithms.theory import brute_force_sat, is_satisfied, verify_tsp_tour


class SortingSearchTests(unittest.TestCase):
    def test_sorting_algorithms(self) -> None:
        nums = [7, 3, 9, 1, 5, 3]
        expected = [1, 3, 3, 5, 7, 9]

        self.assertEqual(quick_sort(nums), expected)
        self.assertEqual(merge_sort(nums), expected)
        self.assertEqual(heap_sort(nums), expected)

    def test_binary_search_and_select(self) -> None:
        nums = [1, 3, 3, 5, 7, 9]

        self.assertEqual(binary_search(nums, 5), 3)
        self.assertEqual(binary_search(nums, 8), -1)
        self.assertEqual(deterministic_select(nums, 4), 5)


class DynamicProgrammingTests(unittest.TestCase):
    def test_knapsack_and_lcs(self) -> None:
        bag = knapsack_01([2, 2, 6, 5, 4], [6, 3, 5, 4, 6], 10)
        lcs = longest_common_subsequence("ABCBDAB", "BDCABA")

        self.assertEqual(bag.max_value, 15)
        self.assertEqual(bag.selected_items, [0, 1, 4])
        self.assertEqual(lcs.length, 4)
        self.assertTrue(is_satisfied([[1], [-2]], {1: True, 2: False}))

    def test_matrix_chain_rod_probability_and_tsp(self) -> None:
        chain = matrix_chain_order([30, 35, 15, 5, 10, 20, 25])
        rod = rod_cutting([1, 5, 8, 9, 10, 17, 17, 20], 8)
        dist = [
            [0, 10, 15, 20],
            [10, 0, 35, 25],
            [15, 35, 0, 30],
            [20, 25, 30, 0],
        ]

        self.assertEqual(chain.min_cost, 15125)
        self.assertEqual(rod.max_revenue, 22)
        self.assertAlmostEqual(series_win_probability(0.55, 4), 0.608287796875)
        self.assertEqual(tsp_held_karp(dist), 80)


class GreedyGraphTests(unittest.TestCase):
    def test_greedy_algorithms(self) -> None:
        codes = huffman_codes({"a": 45, "b": 13, "c": 12, "d": 16, "e": 9, "f": 5})
        selected = activity_selection([(1, 4), (3, 5), (0, 6), (5, 7), (8, 9)])

        self.assertEqual(codes["a"], "0")
        self.assertEqual(selected, [(1, 4), (5, 7), (8, 9)])

    def test_graph_algorithms(self) -> None:
        dsu = DisjointSetUnion(3)
        self.assertTrue(dsu.union(0, 1))
        self.assertFalse(dsu.union(0, 1))

        mst = kruskal_mst(4, [(0, 1, 1), (0, 2, 3), (1, 2, 2), (1, 3, 4), (2, 3, 5)])
        graph = {0: [(1, 4), (2, 1)], 1: [(3, 1)], 2: [(1, 2), (3, 5)], 3: []}
        shortest = dijkstra(graph, 0)

        self.assertEqual(mst.total_weight, 7)
        self.assertEqual(shortest.distances[3], 4)
        self.assertEqual(reconstruct_path(shortest.previous, 3), [0, 2, 1, 3])


class DivideConquerTheoryTests(unittest.TestCase):
    def test_divide_conquer_algorithms(self) -> None:
        distance, pair = closest_pair([(0, 0), (2, 2), (3, 4), (2.1, 2.1)])

        self.assertTrue(math.isclose(distance, math.sqrt(0.02)))
        self.assertEqual(set(pair or []), {(2, 2), (2.1, 2.1)})
        self.assertEqual(polynomial_multiply([1, 2], [3, 4]), [3.0, 10.0, 8.0])
        self.assertEqual(strassen_multiply([[1, 2], [3, 4]], [[5, 6], [7, 8]]), [[19, 22], [43, 50]])

    def test_theory_helpers(self) -> None:
        dist = [
            [0, 10, 15, 20],
            [10, 0, 35, 25],
            [15, 35, 0, 30],
            [20, 25, 30, 0],
        ]
        formula = [[1, -2, 3], [-1, 2, 3], [1, 2, -3]]

        self.assertIsNotNone(brute_force_sat(formula))
        self.assertTrue(verify_tsp_tour(dist, [0, 1, 3, 2], 80))


if __name__ == "__main__":
    unittest.main()

