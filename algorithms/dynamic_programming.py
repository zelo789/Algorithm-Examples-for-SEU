"""动态规划类算法。

动态规划的共同套路：
1. 定义状态：dp[i] 或 dp[i][j] 表示什么。
2. 写状态转移：当前状态如何由更小问题得到。
3. 确定初始值和遍历顺序。
4. 如需具体方案，额外记录选择路径。
"""

from __future__ import annotations

from dataclasses import dataclass
from math import inf


@dataclass(frozen=True)
class KnapsackResult:
    max_value: int
    selected_items: list[int]


def knapsack_01(weights: list[int], values: list[int], capacity: int) -> KnapsackResult:
    """0/1 背包：每件物品只能选或不选一次。

    dp[i][c] 表示只考虑前 i 件物品、容量为 c 时的最大价值。
    转移：
    - 不选第 i 件：dp[i - 1][c]
    - 选第 i 件：dp[i - 1][c - weight] + value
    时间 O(nC)，空间 O(nC)，其中 C 是背包容量。
    """
    if len(weights) != len(values):
        raise ValueError("weights 和 values 长度必须一致")
    if capacity < 0:
        raise ValueError("capacity 不能为负")

    n = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        weight = weights[i - 1]
        value = values[i - 1]
        for c in range(capacity + 1):
            dp[i][c] = dp[i - 1][c]
            if c >= weight:
                dp[i][c] = max(dp[i][c], dp[i - 1][c - weight] + value)

    selected: list[int] = []
    c = capacity
    for i in range(n, 0, -1):
        if dp[i][c] == dp[i - 1][c]:
            continue
        selected.append(i - 1)
        c -= weights[i - 1]

    selected.reverse()
    return KnapsackResult(dp[n][capacity], selected)


@dataclass(frozen=True)
class LCSResult:
    length: int
    sequence: str


def longest_common_subsequence(a: str, b: str) -> LCSResult:
    """最长公共子序列 LCS。

    子序列不要求连续，只要求相对顺序不变。
    dp[i][j] 表示 a 的前 i 个字符与 b 的前 j 个字符的 LCS 长度。
    时间 O(mn)，空间 O(mn)。
    """
    m, n = len(a), len(b)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
                continue
            dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    chars: list[str] = []
    i, j = m, n
    while i > 0 and j > 0:
        if a[i - 1] == b[j - 1]:
            chars.append(a[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] >= dp[i][j - 1]:
            i -= 1
        else:
            j -= 1

    chars.reverse()
    return LCSResult(dp[m][n], "".join(chars))


@dataclass(frozen=True)
class MatrixChainResult:
    min_cost: int
    parenthesization: str


def matrix_chain_order(dimensions: list[int]) -> MatrixChainResult:
    """矩阵连乘：求最少标量乘法次数。

    若有矩阵 A1...An，dimensions 长度为 n+1：
    Ai 的维度是 dimensions[i-1] x dimensions[i]。

    dp[i][j] 表示从 Ai 乘到 Aj 的最小代价。
    split[i][j] 记录最佳断点，方便还原括号。
    时间 O(n^3)，空间 O(n^2)。
    """
    if len(dimensions) < 2:
        raise ValueError("至少需要一个矩阵维度")

    n = len(dimensions) - 1
    dp = [[0] * n for _ in range(n)]
    split = [[0] * n for _ in range(n)]

    for length in range(2, n + 1):
        for i in range(0, n - length + 1):
            j = i + length - 1
            dp[i][j] = inf
            for k in range(i, j):
                cost = (
                    dp[i][k]
                    + dp[k + 1][j]
                    + dimensions[i] * dimensions[k + 1] * dimensions[j + 1]
                )
                if cost < dp[i][j]:
                    dp[i][j] = cost
                    split[i][j] = k

    def build(i: int, j: int) -> str:
        if i == j:
            return f"A{i + 1}"
        k = split[i][j]
        return f"({build(i, k)} x {build(k + 1, j)})"

    return MatrixChainResult(int(dp[0][n - 1]), build(0, n - 1))


@dataclass(frozen=True)
class RodCutResult:
    max_revenue: int
    cuts: list[int]


def rod_cutting(prices: list[int], length: int) -> RodCutResult:
    """钢条切割：长度为 length 的钢条怎样切收益最大。

    prices[i] 表示长度 i+1 的钢条价格。
    dp[l] 表示长度 l 的最大收益。
    时间 O(n^2)，空间 O(n)。
    """
    if length < 0:
        raise ValueError("length 不能为负")
    if length > len(prices):
        raise ValueError("prices 至少要给到目标长度")

    dp = [0] * (length + 1)
    first_cut = [0] * (length + 1)

    for l in range(1, length + 1):
        best = -inf
        for cut in range(1, l + 1):
            revenue = prices[cut - 1] + dp[l - cut]
            if revenue > best:
                best = revenue
                first_cut[l] = cut
        dp[l] = int(best)

    cuts: list[int] = []
    remain = length
    while remain > 0:
        cut = first_cut[remain]
        cuts.append(cut)
        remain -= cut

    return RodCutResult(dp[length], cuts)


@dataclass(frozen=True)
class OptimalBSTResult:
    min_expected_cost: float
    root_table: list[list[int]]


def optimal_bst(success_prob: list[float], fail_prob: list[float]) -> OptimalBSTResult:
    """最优二叉搜索树。

    success_prob[1..n] 是真实关键字被查到的概率，这里输入用 0 下标。
    fail_prob[0..n] 是落在关键字间隙的失败查找概率。

    e[i][j] 表示包含关键字 Ki...Kj 的最小期望代价。
    w[i][j] 表示该子树所有成功/失败概率之和。
    时间 O(n^3)，空间 O(n^2)。
    """
    n = len(success_prob)
    if len(fail_prob) != n + 1:
        raise ValueError("fail_prob 长度必须比 success_prob 多 1")

    e = [[0.0] * (n + 2) for _ in range(n + 2)]
    w = [[0.0] * (n + 2) for _ in range(n + 2)]
    root = [[0] * (n + 1) for _ in range(n + 1)]

    for i in range(1, n + 2):
        e[i][i - 1] = fail_prob[i - 1]
        w[i][i - 1] = fail_prob[i - 1]

    for length in range(1, n + 1):
        for i in range(1, n - length + 2):
            j = i + length - 1
            e[i][j] = inf
            w[i][j] = w[i][j - 1] + success_prob[j - 1] + fail_prob[j]
            for r in range(i, j + 1):
                cost = e[i][r - 1] + e[r + 1][j] + w[i][j]
                if cost < e[i][j]:
                    e[i][j] = cost
                    root[i][j] = r

    return OptimalBSTResult(e[1][n], root)


def series_win_probability(p: float, need_wins: int) -> float:
    """概率 DP：七局四胜等系列赛的获胜概率。

    p 表示单场获胜概率，need_wins 表示先赢几场拿下系列赛。
    dp[i][j] 表示我方已赢 i 场、对方已赢 j 场时，最终我方夺冠概率。
    时间 O(k^2)，空间 O(k^2)。
    """
    if not 0 <= p <= 1:
        raise ValueError("p 必须在 [0, 1] 内")
    if need_wins <= 0:
        raise ValueError("need_wins 必须为正")

    dp = [[0.0] * (need_wins + 1) for _ in range(need_wins + 1)]

    for j in range(need_wins + 1):
        dp[need_wins][j] = 1.0
    for i in range(need_wins):
        dp[i][need_wins] = 0.0

    for i in range(need_wins - 1, -1, -1):
        for j in range(need_wins - 1, -1, -1):
            dp[i][j] = p * dp[i + 1][j] + (1 - p) * dp[i][j + 1]

    return dp[0][0]


def tsp_held_karp(dist: list[list[float]]) -> float:
    """TSP 旅行商问题的动态规划解法 Held-Karp。

    目标：从 0 号城市出发，访问每个城市一次后回到 0，求最短路程。
    dp[(mask, j)] 表示从 0 出发，访问集合 mask，最后停在 j 的最小代价。
    时间 O(n^2 2^n)，空间 O(n 2^n)。这比暴力 O(n!) 好，但仍是指数级。
    """
    n = len(dist)
    if n == 0:
        return 0.0
    if any(len(row) != n for row in dist):
        raise ValueError("dist 必须是方阵")

    dp: dict[tuple[int, int], float] = {(1, 0): 0.0}

    for mask in range(1, 1 << n):
        if not mask & 1:
            continue
        for j in range(n):
            if not mask & (1 << j) or (mask, j) not in dp:
                continue
            for nxt in range(n):
                if mask & (1 << nxt):
                    continue
                new_mask = mask | (1 << nxt)
                new_cost = dp[(mask, j)] + dist[j][nxt]
                old_cost = dp.get((new_mask, nxt), inf)
                if new_cost < old_cost:
                    dp[(new_mask, nxt)] = new_cost

    if n == 1:
        return 0.0

    full = (1 << n) - 1
    return min(dp[(full, j)] + dist[j][0] for j in range(1, n))
