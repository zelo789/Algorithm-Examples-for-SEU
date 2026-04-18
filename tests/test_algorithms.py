"""算法样例回归测试。

运行方式：
python -m unittest
"""

from __future__ import annotations

import math
import unittest
from http.client import HTTPConnection
from http.server import ThreadingHTTPServer
from io import StringIO
from threading import Thread
from unittest.mock import patch

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
from algorithms.showcase import TOPICS, build_topic_examples
from algorithms.sorting_search import (
    binary_search,
    deterministic_select,
    heap_sort,
    merge_sort,
    quick_sort,
)
from algorithms.theory import brute_force_sat, is_satisfied, verify_tsp_tour
from algorithms.visualization import VISUALIZER_BUILDERS, build_visualizer_algorithm, build_visualizer_payload
from cli import main as cli_main
from visualize import VisualizerHandler


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

    def test_knapsack_rejects_negative_weight(self) -> None:
        with self.assertRaisesRegex(ValueError, "weight"):
            knapsack_01([-1], [5], 3)

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


class BacktrackingSearchTests(unittest.TestCase):
    def test_n_queens_subset_sum_and_permutations(self) -> None:
        queens = solve_n_queens(4)
        subset = subset_sum_exists([3, 34, 4, 12, 5, 2], 9)
        permutations = generate_permutations([1, 2, 3])

        self.assertEqual(queens.solution_count, 2)
        self.assertEqual(queens.first_solution, [1, 3, 0, 2])
        self.assertTrue(subset.exists)
        self.assertEqual(sum(subset.subset), 9)
        self.assertEqual(len(permutations), 6)
        self.assertIn([1, 2, 3], permutations)
        self.assertIn([3, 2, 1], permutations)

    def test_backtracking_rejects_invalid_inputs(self) -> None:
        with self.assertRaisesRegex(ValueError, "n"):
            solve_n_queens(0)
        with self.assertRaisesRegex(ValueError, "target"):
            subset_sum_exists([1, 2, 3], -1)


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


class ShowcaseAndVisualizationTests(unittest.TestCase):
    def test_showcase_registry_includes_backtracking_topic(self) -> None:
        self.assertIn("backtracking", TOPICS)
        examples = build_topic_examples("backtracking")

        self.assertEqual(TOPICS["backtracking"].title, "回溯与搜索")
        self.assertGreaterEqual(len(examples), 3)

    def test_visualizer_payload_contains_animation_steps(self) -> None:
        payload = build_visualizer_payload()
        algorithms = {item["id"]: item for item in payload["algorithms"]}

        self.assertEqual(payload["title"], "Algorithm Visualizer")
        self.assertIn("n-queens", algorithms)
        self.assertIn("subset-sum", algorithms)
        self.assertIn("permutations", algorithms)
        self.assertGreater(len(algorithms["n-queens"]["steps"]), 0)
        self.assertIn("message", algorithms["subset-sum"]["steps"][0])

    def test_visualizer_payload_keeps_static_inputs_in_meta(self) -> None:
        payload = build_visualizer_payload()
        algorithms = {item["id"]: item for item in payload["algorithms"]}
        subset_sum = algorithms["subset-sum"]
        permutations = algorithms["permutations"]

        self.assertEqual(subset_sum["meta"]["numbers"], [3, 34, 4, 12, 5, 2])
        self.assertIn("selected_indexes", subset_sum["steps"][0])
        self.assertNotIn("numbers", subset_sum["steps"][0])
        self.assertNotIn("target", subset_sum["steps"][0])

        self.assertEqual(permutations["meta"]["items"], [1, 2, 3])
        self.assertNotIn("items", permutations["steps"][0])

    def test_visualizer_exposes_builder_registry_and_custom_inputs(self) -> None:
        self.assertEqual(set(VISUALIZER_BUILDERS), {"n-queens", "subset-sum", "permutations"})

        queens = build_visualizer_algorithm("n-queens", {"n": 5})
        subset_sum = build_visualizer_algorithm("subset-sum", {"numbers": [2, 2, 5], "target": 4})
        permutations = build_visualizer_algorithm("permutations", {"items": [1, 1, 2]})

        self.assertEqual(queens["meta"]["size"], 5)
        self.assertEqual(queens["meta"]["solutionCount"], 10)
        self.assertEqual(subset_sum["meta"]["solution"], [2, 2])
        self.assertEqual(permutations["meta"]["items"], [1, 1, 2])

    def test_visualizer_rejects_invalid_custom_inputs(self) -> None:
        with self.assertRaisesRegex(ValueError, "algorithm"):
            build_visualizer_algorithm("unknown", {})
        with self.assertRaisesRegex(ValueError, "n"):
            build_visualizer_algorithm("n-queens", {"n": 0})
        with self.assertRaisesRegex(ValueError, "target"):
            build_visualizer_algorithm("subset-sum", {"numbers": [1, 2], "target": -1})

    def test_cli_list_shows_backtracking_topic(self) -> None:
        stdout = StringIO()

        with patch("sys.stdout", stdout):
            cli_main(["--list"])

        self.assertIn("backtracking", stdout.getvalue())

    def test_visualizer_http_routes_serve_index_and_api(self) -> None:
        server = ThreadingHTTPServer(("127.0.0.1", 0), VisualizerHandler)
        thread = Thread(target=server.serve_forever, daemon=True)
        thread.start()

        try:
            port = server.server_address[1]
            connection = HTTPConnection("127.0.0.1", port, timeout=5)

            connection.request("GET", "/")
            index_response = connection.getresponse()
            self.assertEqual(index_response.status, 200)
            index_response.read()

            connection.request("HEAD", "/api/data")
            api_response = connection.getresponse()
            self.assertEqual(api_response.status, 200)
            api_response.read()

            connection.request("GET", "/api/algorithm?algorithm=n-queens&n=5")
            custom_response = connection.getresponse()
            self.assertEqual(custom_response.status, 200)
            self.assertIn('"solutionCount": 10', custom_response.read().decode("utf-8"))

            connection.request("GET", "/api/algorithm?algorithm=n-queens&n=0")
            invalid_response = connection.getresponse()
            self.assertEqual(invalid_response.status, 400)
            self.assertIn("n", invalid_response.read().decode("utf-8"))
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=5)


if __name__ == "__main__":
    unittest.main()
