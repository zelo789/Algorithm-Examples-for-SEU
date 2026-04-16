"""贪心算法与图算法。"""

from __future__ import annotations

import heapq
from dataclasses import dataclass, field
from math import inf


@dataclass(order=True)
class _HuffmanNode:
    freq: int
    order: int
    char: str | None = field(compare=False, default=None)
    left: "_HuffmanNode | None" = field(compare=False, default=None)
    right: "_HuffmanNode | None" = field(compare=False, default=None)


def huffman_codes(frequencies: dict[str, int]) -> dict[str, str]:
    """哈夫曼编码：给高频字符更短编码，构造最优前缀码。

    算法每次合并频率最小的两棵树，因此是贪心策略。
    时间 O(n log n)，空间 O(n)。
    """
    if not frequencies:
        return {}
    if any(freq <= 0 for freq in frequencies.values()):
        raise ValueError("频率必须为正数")

    heap: list[_HuffmanNode] = []
    for order, (char, freq) in enumerate(frequencies.items()):
        heapq.heappush(heap, _HuffmanNode(freq=freq, order=order, char=char))

    next_order = len(heap)
    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = _HuffmanNode(
            freq=left.freq + right.freq,
            order=next_order,
            left=left,
            right=right,
        )
        next_order += 1
        heapq.heappush(heap, merged)

    root = heap[0]
    codes: dict[str, str] = {}

    def walk(node: _HuffmanNode, prefix: str) -> None:
        if node.char is not None:
            # 只有一个字符时，用 "0" 作为编码，避免空串编码。
            codes[node.char] = prefix or "0"
            return
        if node.left is not None:
            walk(node.left, prefix + "0")
        if node.right is not None:
            walk(node.right, prefix + "1")

    walk(root, "")
    return codes


def activity_selection(activities: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """活动选择：选出最多个互不重叠活动。

    每个活动为 (start, finish)。贪心原则：总是选结束最早且兼容的活动。
    时间 O(n log n)，主要来自排序；空间 O(n)。
    """
    sorted_activities = sorted(activities, key=lambda item: item[1])
    result: list[tuple[int, int]] = []
    current_finish = -inf

    for start, finish in sorted_activities:
        if start < current_finish:
            continue
        result.append((start, finish))
        current_finish = finish

    return result


class DisjointSetUnion:
    """并查集：维护不相交集合，支持合并与查询连通性。

    路径压缩 + 按秩合并后，单次操作均摊近似 O(1)，严格为 O(alpha(n))。
    """

    def __init__(self, size: int) -> None:
        if size < 0:
            raise ValueError("size 不能为负")
        self.parent = list(range(size))
        self.rank = [0] * size

    def find(self, x: int) -> int:
        """查找 x 所属集合的代表元。"""
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, a: int, b: int) -> bool:
        """合并 a、b 所属集合；若本来已连通，返回 False。"""
        root_a = self.find(a)
        root_b = self.find(b)
        if root_a == root_b:
            return False

        if self.rank[root_a] < self.rank[root_b]:
            root_a, root_b = root_b, root_a

        self.parent[root_b] = root_a
        if self.rank[root_a] == self.rank[root_b]:
            self.rank[root_a] += 1
        return True


@dataclass(frozen=True)
class MSTResult:
    total_weight: float
    edges: list[tuple[int, int, float]]


def kruskal_mst(vertex_count: int, edges: list[tuple[int, int, float]]) -> MSTResult:
    """Kruskal 最小生成树。

    贪心原则：按边权从小到大尝试加入，只要不形成环就保留。
    并查集用于快速判断两个端点是否已连通。
    时间 O(E log E)，空间 O(V)。
    """
    dsu = DisjointSetUnion(vertex_count)
    chosen: list[tuple[int, int, float]] = []
    total = 0.0

    for u, v, weight in sorted(edges, key=lambda edge: edge[2]):
        if not dsu.union(u, v):
            continue
        chosen.append((u, v, weight))
        total += weight
        if len(chosen) == vertex_count - 1:
            break

    if vertex_count > 0 and len(chosen) != vertex_count - 1:
        raise ValueError("图不连通，无法形成生成树")

    return MSTResult(total, chosen)


@dataclass(frozen=True)
class DijkstraResult:
    distances: dict[int, float]
    previous: dict[int, int | None]


def dijkstra(graph: dict[int, list[tuple[int, float]]], source: int) -> DijkstraResult:
    """Dijkstra 单源最短路。

    graph[u] = [(v, weight), ...]，要求所有边权非负。
    使用优先队列后，时间 O((V + E) log V)，空间 O(V + E)。
    """
    for u, neighbors in graph.items():
        for _, weight in neighbors:
            if weight < 0:
                raise ValueError(f"Dijkstra 不支持负边权：节点 {u} 出现 {weight}")

    vertices = set(graph)
    for neighbors in graph.values():
        for v, _ in neighbors:
            vertices.add(v)

    distances = {v: inf for v in vertices}
    previous: dict[int, int | None] = {v: None for v in vertices}
    distances[source] = 0.0

    heap: list[tuple[float, int]] = [(0.0, source)]
    while heap:
        current_dist, u = heapq.heappop(heap)
        if current_dist != distances[u]:
            continue

        for v, weight in graph.get(u, []):
            new_dist = current_dist + weight
            if new_dist >= distances[v]:
                continue
            distances[v] = new_dist
            previous[v] = u
            heapq.heappush(heap, (new_dist, v))

    return DijkstraResult(distances, previous)


def reconstruct_path(previous: dict[int, int | None], target: int) -> list[int]:
    """根据 Dijkstra 的 previous 表还原 source 到 target 的路径。"""
    path: list[int] = []
    current: int | None = target
    while current is not None:
        path.append(current)
        current = previous.get(current)
    path.reverse()
    return path

