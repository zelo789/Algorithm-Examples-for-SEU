"""理论类问题的小规模可运行示例。

注意：NP 完全问题的重点通常不是“写一个很快的程序”，而是理解：
1. 解可以在多项式时间内验证，属于 NP。
2. 许多问题可以互相多项式归约。
3. 若任意 NP 完全问题有多项式时间解，则所有 NP 问题都有多项式时间解。
"""

from __future__ import annotations

from itertools import product

Clause = list[int]
Formula = list[Clause]


def is_satisfied(formula: Formula, assignment: dict[int, bool]) -> bool:
    """检查 SAT 公式是否被某个赋值满足。

    公式使用 CNF 表示：
    - 正整数 x 表示变量 x 为 True。
    - 负整数 -x 表示变量 x 为 False。
    - 子句 clause 是若干文字的“或”。
    - formula 是若干子句的“与”。
    验证一个给定解的时间为 O(文字总数)，这正是 SAT 属于 NP 的原因之一。
    """
    for clause in formula:
        clause_ok = False
        for literal in clause:
            value = assignment[abs(literal)]
            if literal < 0:
                value = not value
            clause_ok = clause_ok or value
        if not clause_ok:
            return False
    return True


def brute_force_sat(formula: Formula) -> dict[int, bool] | None:
    """暴力求解 SAT。

    这不是高效 SAT Solver，只用于理解指数复杂度。
    若变量数为 n，需要最多检查 2^n 个赋值。
    """
    variables = sorted({abs(literal) for clause in formula for literal in clause})

    for values in product([False, True], repeat=len(variables)):
        assignment = dict(zip(variables, values))
        if is_satisfied(formula, assignment):
            return assignment
    return None


def is_3sat_formula(formula: Formula) -> bool:
    """判断一个 CNF 公式是否是 3-SAT 形式：每个子句恰好 3 个文字。"""
    return all(len(clause) == 3 for clause in formula)


def verify_tsp_tour(dist: list[list[float]], tour: list[int], limit: float) -> bool:
    """验证 TSP 证书：给定路线是否访问所有城市一次且总长度不超过 limit。

    这说明 TSP 的判定版属于 NP：只要有人给出一条路线，我们能在 O(n)
    时间内检查它是否合法并计算长度。
    """
    n = len(dist)
    if len(tour) != n or set(tour) != set(range(n)):
        return False

    total = 0.0
    for i in range(n):
        total += dist[tour[i]][tour[(i + 1) % n]]
    return total <= limit


NP_COMPLETE_NOTES = """
NP 完全问题复习要点：

P：能在多项式时间内求解的问题。
NP：给一个候选答案，能在多项式时间内验证的问题。
NP-hard：至少和 NP 中所有问题一样难的问题。
NP-complete：既属于 NP，又是 NP-hard 的问题。

SAT 是第一个被证明的 NP 完全问题（Cook-Levin 定理）。
3-SAT 是 SAT 的受限形式，但仍然是 NP 完全问题。
TSP 的判定版：“是否存在一条长度不超过 K 的旅行路线？” 是 NP 完全问题。
TSP 的优化版：“最短路线是多少？” 通常称为 NP-hard。
"""

