"""回溯与搜索类算法。"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TypeVar

T = TypeVar("T")


@dataclass(frozen=True)
class NQueensResult:
    solution_count: int
    first_solution: list[int] | None


def solve_n_queens(n: int) -> NQueensResult:
    """N 皇后：在 n*n 棋盘上放置 n 个皇后，使其互不攻击。"""
    if n <= 0:
        raise ValueError("n 必须为正整数")

    cols: set[int] = set()
    diag1: set[int] = set()
    diag2: set[int] = set()
    placement: list[int] = []
    first_solution: list[int] | None = None
    solution_count = 0

    def backtrack(row: int) -> None:
        nonlocal first_solution, solution_count
        if row == n:
            solution_count += 1
            if first_solution is None:
                first_solution = placement.copy()
            return

        for col in range(n):
            if col in cols or row - col in diag1 or row + col in diag2:
                continue
            cols.add(col)
            diag1.add(row - col)
            diag2.add(row + col)
            placement.append(col)

            backtrack(row + 1)

            placement.pop()
            diag2.remove(row + col)
            diag1.remove(row - col)
            cols.remove(col)

    backtrack(0)
    return NQueensResult(solution_count=solution_count, first_solution=first_solution)


@dataclass(frozen=True)
class SubsetSumResult:
    exists: bool
    subset: list[int]


def subset_sum_exists(numbers: list[int], target: int) -> SubsetSumResult:
    """子集和：是否存在一个子集，使其元素和恰好为 target。"""
    if target < 0:
        raise ValueError("target 不能为负")
    if any(number < 0 for number in numbers):
        raise ValueError("numbers 不能包含负数")

    path: list[int] = []
    answer: list[int] | None = None

    def search(index: int, remain: int) -> bool:
        nonlocal answer
        if remain == 0:
            answer = path.copy()
            return True
        if index == len(numbers) or remain < 0:
            return False

        path.append(numbers[index])
        if search(index + 1, remain - numbers[index]):
            return True
        path.pop()

        return search(index + 1, remain)

    exists = search(0, target)
    return SubsetSumResult(exists=exists, subset=answer or [])


def generate_permutations(items: list[T]) -> list[list[T]]:
    """生成 items 的所有排列。"""
    if not items:
        return [[]]

    used = [False] * len(items)
    current: list[T] = []
    permutations: list[list[T]] = []

    def backtrack() -> None:
        if len(current) == len(items):
            permutations.append(current.copy())
            return

        for index, item in enumerate(items):
            if used[index]:
                continue
            used[index] = True
            current.append(item)
            backtrack()
            current.pop()
            used[index] = False

    backtrack()
    return permutations
