<div align="center">

# Algorithm Examples for SEU

Python 算法样例与中文复习笔记

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB)
![Tests](https://img.shields.io/badge/tests-unittest-brightgreen)
![Language](https://img.shields.io/badge/docs-%E4%B8%AD%E6%96%87-red)

面向算法课程考试、面试复习和代码理解的轻量项目。  
每个算法都尽量写清楚：解决什么问题、核心思想是什么、Python 怎么实现、复杂度如何分析。

</div>

## 目录

- [快速开始](#快速开始)
- [项目亮点](#项目亮点)
- [算法地图](#算法地图)
- [建议学习路线](#建议学习路线)
- [项目结构](#项目结构)
- [考试答题模板](#考试答题模板)
- [测试与验证](#测试与验证)

## 快速开始

克隆仓库后进入项目目录：

```bash
git clone git@github.com:zelo789/Algorithm-Examples-for-SEU.git
cd Algorithm-Examples-for-SEU
```

运行全部示例：

```bash
python demo.py
```

按主题运行：

```bash
python cli.py --list
python cli.py sorting
python cli.py dp
python cli.py graph
python cli.py divide
python cli.py theory
```

运行测试：

```bash
python -m unittest
```

## 项目亮点

| 内容 | 说明 |
| --- | --- |
| 中文注释 | 代码中保留关键思路说明，适合边读边复习。 |
| 可运行示例 | `demo.py` 和 `cli.py` 提供完整输入输出。 |
| 考试导向 | README 和 `docs/exam_quick_review.md` 按考点整理目的、原理和复杂度。 |
| 覆盖全面 | 包含排序、查找、动态规划、贪心、图算法、分治、FFT、NP 完全问题。 |
| 有测试保护 | `tests/` 中提供基础回归测试，方便修改后验证。 |

## 算法地图

### 第一优先：考试与面试核心

| 算法 | 解决的问题 | 核心思想 | 时间复杂度 | 空间复杂度 | 代码位置 |
| --- | --- | --- | --- | --- | --- |
| 快速排序 | 高效排序 | 选 pivot，将数组划分为小于、等于、大于三段 | 平均 O(n log n)，最坏 O(n^2) | 示例版 O(n) | `sorting_search.py` |
| 归并排序 | 稳定排序 | 递归分半，再合并两个有序数组 | O(n log n) | O(n) | `sorting_search.py` |
| 二分查找 | 有序数组查找 | 每次排除一半搜索区间 | O(log n) | O(1) | `sorting_search.py` |
| 0/1 背包 | 容量限制下价值最大 | `dp[i][c]` 表示前 i 件、容量 c 的最优价值 | O(nC) | O(nC) | `dynamic_programming.py` |
| LCS | 最长公共子序列 | 相等取左上 +1，不等取上方和左方最大值 | O(mn) | O(mn) | `dynamic_programming.py` |
| 矩阵连乘 | 最少标量乘法次数 | 枚举最后一次断点 k | O(n^3) | O(n^2) | `dynamic_programming.py` |
| 哈夫曼编码 | 最优前缀编码 | 每次合并频率最小的两棵树 | O(n log n) | O(n) | `greedy_graph.py` |
| 活动选择 | 最多不冲突活动 | 总是选择结束最早的兼容活动 | O(n log n) | O(n) | `greedy_graph.py` |
| Kruskal | 最小生成树 | 按边权升序加边，用并查集避环 | O(E log E) | O(V) | `greedy_graph.py` |
| Dijkstra | 非负权单源最短路 | 每次确定当前距离最小的点 | O((V+E) log V) | O(V+E) | `greedy_graph.py` |

### 第二优先：进阶题型

| 算法 | 解决的问题 | 核心思想 | 时间复杂度 | 空间复杂度 | 代码位置 |
| --- | --- | --- | --- | --- | --- |
| 钢条切割 | 切分钢条收益最大 | `dp[l]` 枚举第一刀长度 | O(n^2) | O(n) | `dynamic_programming.py` |
| 最优 BST | 最小化搜索期望代价 | 枚举每段关键字的根 | O(n^3) | O(n^2) | `dynamic_programming.py` |
| 最近点对 | 平面最近两点 | 分治后只检查中线附近条带 | O(n log n) | O(n) | `divide_conquer.py` |
| 第 k 小元素 | 顺序统计量 | Median of Medians 保证较好的 pivot | O(n) | O(n) | `sorting_search.py` |
| 堆排序 | 基于堆的排序 | 建堆后不断弹出堆顶 | O(n log n) | 示例版 O(n) | `sorting_search.py` |
| 并查集 | 动态连通性 | 路径压缩 + 按秩合并 | 近似 O(1) | O(n) | `greedy_graph.py` |

### 第三优先：理解型算法

| 算法 | 解决的问题 | 核心思想 | 时间复杂度 | 空间复杂度 | 代码位置 |
| --- | --- | --- | --- | --- | --- |
| FFT | 快速多项式乘法 | 奇偶拆分，在单位根上分治求值 | O(n log n) | O(n) | `divide_conquer.py` |
| Strassen | 更快矩阵乘法 | 用 7 次子矩阵乘法替代普通 8 次 | O(n^2.807) | O(n^2) | `divide_conquer.py` |
| 概率 DP | 系列赛获胜概率 | `dp[i][j]` 表示当前比分下最终胜率 | O(k^2) | O(k^2) | `dynamic_programming.py` |
| 随机算法 | 随机选择或概率估计 | 随机 pivot、蒙特卡洛采样 | 视算法而定 | 视算法而定 | `sorting_search.py` |

### 理论类：考试大题

| 主题 | 必须说清楚的点 | 代码位置 |
| --- | --- | --- |
| NP 完全问题 | P、NP、NP-hard、NP-complete 的区别 | `theory.py` |
| SAT | CNF 公式是否存在满足赋值；SAT 是第一个 NP 完全问题 | `theory.py` |
| 3-SAT | 每个子句恰好 3 个文字；仍然是 NP 完全问题 | `theory.py` |
| TSP | 判定版是 NP 完全；优化版通常称为 NP-hard | `theory.py`、`dynamic_programming.py` |

## 建议学习路线

1. 先跑 `python cli.py --list`，了解有哪些主题。
2. 按优先级学习：先 `sorting`、`dp`、`graph`，再看 `divide` 和 `theory`。
3. 每学一个算法，按“目的、原理、实现、复杂度”四步复述一遍。
4. 打开源码看中文注释，重点理解状态定义、贪心选择、分治合并和图算法的不变量。
5. 考前读 [docs/exam_quick_review.md](docs/exam_quick_review.md)，把模板写熟。

推荐顺序：

```text
排序与查找
  -> 动态规划
  -> 贪心与图算法
  -> 分治进阶
  -> NP 完全理论
```

## 项目结构

```text
.
├── algorithms/
│   ├── sorting_search.py       # 排序、查找、选择、随机算法
│   ├── dynamic_programming.py  # 背包、LCS、矩阵连乘、TSP 等
│   ├── greedy_graph.py         # 贪心、并查集、MST、最短路
│   ├── divide_conquer.py       # 最近点对、FFT、Strassen
│   └── theory.py               # SAT、3-SAT、NP 完全、TSP 验证
├── docs/
│   └── exam_quick_review.md    # 考前速记
├── tests/
│   └── test_algorithms.py      # 回归测试
├── cli.py                      # 按主题运行示例
├── demo.py                     # 一次性运行所有典型示例
└── README.md
```

## 考试答题模板

### 动态规划

1. 定义状态：例如 `dp[i][c]` 表示前 i 件物品、容量 c 的最大价值。
2. 写状态转移：说明当前状态如何从更小状态得到。
3. 写初始化：说明空序列、容量为 0、单个矩阵等边界情况。
4. 写遍历顺序：保证依赖的状态已经计算过。
5. 写答案位置：例如 `dp[n][capacity]`。
6. 分析复杂度：状态数量乘每个状态的转移代价。

### 贪心算法

1. 写贪心选择：例如活动选择总选结束最早的活动。
2. 证明不会吃亏：常用交换论证或归纳证明。
3. 写算法步骤：排序、扫描、选择。
4. 分析复杂度：通常包括排序复杂度和线性扫描复杂度。

### 图算法

- Kruskal 解决最小生成树问题，适合边列表，用并查集判断是否成环。
- Dijkstra 解决非负权单源最短路问题，适合邻接表和优先队列。
- 最小生成树关注“连通所有点的总边权最小”。
- 最短路关注“从源点到某个点的路径最短”。

## 测试与验证

运行回归测试：

```bash
python -m unittest
```

运行语法编译检查：

```bash
python -m compileall .
```

运行全部示例：

```bash
python cli.py all
```

当前测试覆盖了排序、查找、动态规划、图算法、分治算法和理论辅助函数。它不是完整算法竞赛评测集，但足够作为学习项目的基础保护网。

