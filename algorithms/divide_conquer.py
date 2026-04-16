"""分治与数值算法：最近点对、FFT、Strassen。"""

from __future__ import annotations

import cmath
from math import dist, inf

Point = tuple[float, float]
Matrix = list[list[int | float]]


def closest_pair(points: list[Point]) -> tuple[float, tuple[Point, Point] | None]:
    """最近点对：二维平面中找距离最近的两个点。

    分治思想：
    1. 按 x 坐标分成左右两半。
    2. 分别求左右内部最近距离 d。
    3. 只检查中线附近宽度 2d 的条带，寻找跨左右两边的更近点。
    时间 O(n log n)，空间 O(n)。
    """
    if len(points) < 2:
        return inf, None

    points_by_x = sorted(points)
    points_by_y = sorted(points, key=lambda p: p[1])

    def solve(px: list[Point], py: list[Point]) -> tuple[float, tuple[Point, Point]]:
        if len(px) <= 3:
            return _brute_force_closest(px)

        mid = len(px) // 2
        mid_x = px[mid][0]
        left_x = px[:mid]
        right_x = px[mid:]
        left_set = set(left_x)
        left_y = [p for p in py if p in left_set]
        right_y = [p for p in py if p not in left_set]

        left_dist, left_pair = solve(left_x, left_y)
        right_dist, right_pair = solve(right_x, right_y)
        best_dist, best_pair = (
            (left_dist, left_pair) if left_dist <= right_dist else (right_dist, right_pair)
        )

        strip = [p for p in py if abs(p[0] - mid_x) < best_dist]
        for i, point in enumerate(strip):
            # 几何性质：条带中每个点最多只需看后面常数个点，常写 7 个。
            for other in strip[i + 1 : i + 8]:
                candidate = dist(point, other)
                if candidate < best_dist:
                    best_dist = candidate
                    best_pair = (point, other)

        return best_dist, best_pair

    return solve(points_by_x, points_by_y)


def _brute_force_closest(points: list[Point]) -> tuple[float, tuple[Point, Point]]:
    best = inf
    pair = (points[0], points[1])
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            candidate = dist(points[i], points[j])
            if candidate < best:
                best = candidate
                pair = (points[i], points[j])
    return best, pair


def fft(values: list[complex], invert: bool = False) -> list[complex]:
    """快速傅里叶变换 FFT。

    用途：把多项式从“系数表示”转换为“点值表示”，从而快速做多项式乘法。
    这里实现 Cooley-Tukey 递归版，要求长度是 2 的幂。
    时间 O(n log n)，空间 O(n)。
    """
    n = len(values)
    if n == 0 or n & (n - 1):
        raise ValueError("FFT 输入长度必须是 2 的幂")
    if n == 1:
        return values.copy()

    even = fft(values[0::2], invert)
    odd = fft(values[1::2], invert)
    angle = 2 * cmath.pi / n * (-1 if invert else 1)
    root = complex(1)
    step = cmath.exp(1j * angle)
    result = [0j] * n

    for k in range(n // 2):
        value = root * odd[k]
        result[k] = even[k] + value
        result[k + n // 2] = even[k] - value
        root *= step

    if invert:
        return [x / 2 for x in result]
    return result


def polynomial_multiply(a: list[int | float], b: list[int | float]) -> list[float]:
    """用 FFT 做多项式乘法。

    若 a=[1,2] 表示 1+2x，b=[3,4] 表示 3+4x，结果为 [3,10,8]。
    时间 O(n log n)，其中 n 是补齐后的 2 的幂长度。
    """
    size = 1
    needed = len(a) + len(b) - 1
    while size < needed:
        size *= 2

    fa = [complex(x) for x in a] + [0j] * (size - len(a))
    fb = [complex(x) for x in b] + [0j] * (size - len(b))
    ya = fft(fa)
    yb = fft(fb)
    yc = [x * y for x, y in zip(ya, yb)]
    coeffs = fft(yc, invert=True)
    return [round(coeff.real, 10) for coeff in coeffs[:needed]]


def strassen_multiply(a: Matrix, b: Matrix) -> Matrix:
    """Strassen 矩阵乘法。

    普通矩阵乘法把 n*n 矩阵分块后需要 8 次子乘法。
    Strassen 用 7 次子乘法加若干加减法换取更低渐进复杂度：
    O(n^log2(7)) 约 O(n^2.807)。

    为了让学习示例好用，这里会把矩阵补成 2 的幂阶方阵，最后再裁剪。
    """
    _validate_matrix_pair(a, b)
    rows, inner, cols = len(a), len(a[0]), len(b[0])
    size = 1
    while size < max(rows, inner, cols):
        size *= 2

    padded_a = _pad_matrix(a, size, size)
    padded_b = _pad_matrix(b, size, size)
    product = _strassen_square(padded_a, padded_b)
    return [row[:cols] for row in product[:rows]]


def _strassen_square(a: Matrix, b: Matrix) -> Matrix:
    n = len(a)
    if n == 1:
        return [[a[0][0] * b[0][0]]]
    if n <= 2:
        return _classic_multiply(a, b)

    a11, a12, a21, a22 = _split(a)
    b11, b12, b21, b22 = _split(b)

    m1 = _strassen_square(_add(a11, a22), _add(b11, b22))
    m2 = _strassen_square(_add(a21, a22), b11)
    m3 = _strassen_square(a11, _sub(b12, b22))
    m4 = _strassen_square(a22, _sub(b21, b11))
    m5 = _strassen_square(_add(a11, a12), b22)
    m6 = _strassen_square(_sub(a21, a11), _add(b11, b12))
    m7 = _strassen_square(_sub(a12, a22), _add(b21, b22))

    c11 = _add(_sub(_add(m1, m4), m5), m7)
    c12 = _add(m3, m5)
    c21 = _add(m2, m4)
    c22 = _add(_sub(_add(m1, m3), m2), m6)
    return _join(c11, c12, c21, c22)


def _classic_multiply(a: Matrix, b: Matrix) -> Matrix:
    rows, inner, cols = len(a), len(a[0]), len(b[0])
    result: Matrix = [[0 for _ in range(cols)] for _ in range(rows)]
    for i in range(rows):
        for k in range(inner):
            for j in range(cols):
                result[i][j] += a[i][k] * b[k][j]
    return result


def _validate_matrix_pair(a: Matrix, b: Matrix) -> None:
    if not a or not b or not a[0] or not b[0]:
        raise ValueError("矩阵不能为空")
    if any(len(row) != len(a[0]) for row in a):
        raise ValueError("矩阵 a 每行长度必须一致")
    if any(len(row) != len(b[0]) for row in b):
        raise ValueError("矩阵 b 每行长度必须一致")
    if len(a[0]) != len(b):
        raise ValueError("a 的列数必须等于 b 的行数")


def _pad_matrix(matrix: Matrix, rows: int, cols: int) -> Matrix:
    padded: Matrix = [[0 for _ in range(cols)] for _ in range(rows)]
    for i, row in enumerate(matrix):
        for j, value in enumerate(row):
            padded[i][j] = value
    return padded


def _split(matrix: Matrix) -> tuple[Matrix, Matrix, Matrix, Matrix]:
    mid = len(matrix) // 2
    top = matrix[:mid]
    bottom = matrix[mid:]
    return (
        [row[:mid] for row in top],
        [row[mid:] for row in top],
        [row[:mid] for row in bottom],
        [row[mid:] for row in bottom],
    )


def _join(c11: Matrix, c12: Matrix, c21: Matrix, c22: Matrix) -> Matrix:
    top = [left + right for left, right in zip(c11, c12)]
    bottom = [left + right for left, right in zip(c21, c22)]
    return top + bottom


def _add(a: Matrix, b: Matrix) -> Matrix:
    return [[x + y for x, y in zip(row_a, row_b)] for row_a, row_b in zip(a, b)]


def _sub(a: Matrix, b: Matrix) -> Matrix:
    return [[x - y for x, y in zip(row_a, row_b)] for row_a, row_b in zip(a, b)]

