"""排序、查找、选择类算法。"""

from __future__ import annotations

import heapq
import random
from typing import Iterable, TypeVar

T = TypeVar("T")


def quick_sort(items: list[T]) -> list[T]:
    """快速排序：平均 O(n log n)，最坏 O(n^2)，额外空间平均 O(log n)。

    思想：
    1. 选一个基准 pivot。
    2. 把数组分成小于、等于、大于 pivot 的三段。
    3. 递归排序左右两段。

    这里返回新列表，便于学习；工程中也常写原地版本以节省空间。
    """
    if len(items) <= 1:
        return items.copy()

    pivot = items[len(items) // 2]
    less = [x for x in items if x < pivot]
    equal = [x for x in items if x == pivot]
    greater = [x for x in items if x > pivot]
    return quick_sort(less) + equal + quick_sort(greater)


def randomized_quick_sort(items: list[T]) -> list[T]:
    """随机化快速排序。

    随机选 pivot 可以降低被特殊输入卡成 O(n^2) 的概率。
    期望时间复杂度 O(n log n)，最坏仍是 O(n^2)。
    """
    if len(items) <= 1:
        return items.copy()

    pivot = random.choice(items)
    less = [x for x in items if x < pivot]
    equal = [x for x in items if x == pivot]
    greater = [x for x in items if x > pivot]
    return randomized_quick_sort(less) + equal + randomized_quick_sort(greater)


def merge_sort(items: list[T]) -> list[T]:
    """归并排序：稳定排序，时间 O(n log n)，额外空间 O(n)。

    思想：先递归把左右两半排好，再用双指针合并两个有序数组。
    """
    if len(items) <= 1:
        return items.copy()

    mid = len(items) // 2
    left = merge_sort(items[:mid])
    right = merge_sort(items[mid:])
    return _merge(left, right)


def _merge(left: list[T], right: list[T]) -> list[T]:
    result: list[T] = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
            continue
        result.append(right[j])
        j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result


def heap_sort(items: Iterable[T]) -> list[T]:
    """堆排序：时间 O(n log n)，额外空间这里为 O(n)。

    Python 的 heapq 是小根堆。把所有元素建堆后，不断弹出堆顶即可得到升序。
    原地堆排序可做到 O(1) 额外空间，但代码会更绕。
    """
    heap = list(items)
    heapq.heapify(heap)
    return [heapq.heappop(heap) for _ in range(len(heap))]


def binary_search(items: list[T], target: T) -> int:
    """二分查找：要求数组已经升序，时间 O(log n)，空间 O(1)。

    返回 target 的下标；如果不存在，返回 -1。
    """
    left, right = 0, len(items) - 1

    while left <= right:
        mid = left + (right - left) // 2
        if items[mid] == target:
            return mid
        if items[mid] < target:
            left = mid + 1
            continue
        right = mid - 1

    return -1


def quick_select(items: list[T], k: int) -> T:
    """第 k 小元素，k 从 1 开始。

    这是随机化选择算法，期望 O(n)，最坏 O(n^2)。
    若考试强调“线性选择”，可看 deterministic_select，它保证最坏 O(n)。
    """
    if not 1 <= k <= len(items):
        raise ValueError("k 必须在 1 到 len(items) 之间")

    pivot = random.choice(items)
    less = [x for x in items if x < pivot]
    equal = [x for x in items if x == pivot]
    greater = [x for x in items if x > pivot]

    if k <= len(less):
        return quick_select(less, k)
    if k <= len(less) + len(equal):
        return pivot
    return quick_select(greater, k - len(less) - len(equal))


def deterministic_select(items: list[T], k: int) -> T:
    """线性选择：Median of Medians，最坏时间 O(n)。

    思想：
    1. 每 5 个元素分组，各组排序取中位数。
    2. 递归求这些中位数的中位数，作为较好的 pivot。
    3. 用 pivot 划分后只递归进入包含第 k 小元素的一边。
    """
    if not 1 <= k <= len(items):
        raise ValueError("k 必须在 1 到 len(items) 之间")
    if len(items) <= 5:
        return sorted(items)[k - 1]

    groups = [items[i : i + 5] for i in range(0, len(items), 5)]
    medians = [sorted(group)[len(group) // 2] for group in groups]
    pivot = deterministic_select(medians, (len(medians) + 1) // 2)

    less = [x for x in items if x < pivot]
    equal = [x for x in items if x == pivot]
    greater = [x for x in items if x > pivot]

    if k <= len(less):
        return deterministic_select(less, k)
    if k <= len(less) + len(equal):
        return pivot
    return deterministic_select(greater, k - len(less) - len(equal))


def monte_carlo_pi(samples: int = 100_000) -> float:
    """随机算法示例：用蒙特卡洛方法估计圆周率。

    在单位正方形中随机撒点，落入 1/4 圆内的比例约等于 pi / 4。
    样本越多越准；时间 O(samples)，空间 O(1)。
    """
    if samples <= 0:
        raise ValueError("samples 必须为正数")

    inside = 0
    for _ in range(samples):
        x = random.random()
        y = random.random()
        if x * x + y * y <= 1:
            inside += 1
    return 4 * inside / samples

