# Python 算法样例与复习笔记

运行示例：

```bash
python demo.py
```

按主题运行示例：

```bash
python cli.py --list
python cli.py sorting
python cli.py dp
python cli.py graph
python cli.py divide
python cli.py theory
```

运行回归测试：

```bash
python -m unittest discover -s tests
```

项目结构：

- `algorithms/sorting_search.py`：快速排序、归并排序、堆排序、二分查找、第 k 小元素、随机算法。
- `algorithms/dynamic_programming.py`：0/1 背包、LCS、矩阵连乘、钢条切割、最优 BST、概率 DP、TSP 动态规划。
- `algorithms/greedy_graph.py`：哈夫曼编码、活动选择、并查集、Kruskal、Dijkstra。
- `algorithms/divide_conquer.py`：最近点对、FFT、多项式乘法、Strassen 矩阵乘法。
- `algorithms/theory.py`：SAT、3-SAT、TSP 验证与 NP 完全要点。
- `cli.py`：按主题运行算法示例。
- `tests/test_algorithms.py`：核心算法回归测试。
- `docs/exam_quick_review.md`：考前速记版复习材料。

## 建议学习顺序

1. 先读 `README.md` 的复杂度表，建立整体地图。
2. 再运行 `python cli.py sorting`、`python cli.py dp` 等主题命令，看输入输出。
3. 打开对应源码，重点看中文注释里的状态定义、贪心选择和复杂度。
4. 最后读 `docs/exam_quick_review.md`，练习把算法思路写成考试答案。

## 第一优先：考试/面试核心

| 算法 | 目的 | 核心原理 | 时间复杂度 | 空间复杂度 |
| --- | --- | --- | --- | --- |
| 快速排序 | 高效排序 | 选 pivot，把问题划分为小于/等于/大于三段 | 平均 O(n log n)，最坏 O(n^2) | 平均 O(log n)，示例版 O(n) |
| 归并排序 | 稳定排序 | 递归分半，合并两个有序数组 | O(n log n) | O(n) |
| 二分查找 | 在有序数组中查找 | 每次排除一半搜索区间 | O(log n) | O(1) |
| 0/1 背包 | 容量限制下价值最大 | `dp[i][c]` 表示前 i 件、容量 c 的最优值 | O(nC) | O(nC) |
| LCS | 求两个序列最长公共子序列 | 相等取左上 +1，不等取上/左最大 | O(mn) | O(mn) |
| 矩阵连乘 | 找最省乘法次数的括号化 | 枚举最后一次断点 k | O(n^3) | O(n^2) |
| 哈夫曼编码 | 构造最优前缀码 | 每次合并频率最小的两棵树 | O(n log n) | O(n) |
| 活动选择 | 选最多不冲突活动 | 总选结束最早的兼容活动 | O(n log n) | O(n) |
| Kruskal | 最小生成树 | 按边权升序加边，用并查集避环 | O(E log E) | O(V) |
| Dijkstra | 非负权单源最短路 | 每次扩展当前距离最小的点 | O((V+E) log V) | O(V+E) |

## 第二优先：进阶

| 算法 | 目的 | 核心原理 | 时间复杂度 | 空间复杂度 |
| --- | --- | --- | --- | --- |
| 钢条切割 | 切钢条收益最大 | `dp[l]` 枚举第一刀长度 | O(n^2) | O(n) |
| 最优 BST | 最小化搜索期望代价 | 枚举每段关键字的根 | O(n^3) | O(n^2) |
| 最近点对 | 平面最近两点 | 分治 + 检查中线条带 | O(n log n) | O(n) |
| 第 k 小元素 | 找顺序统计量 | Median of Medians 保证好 pivot | O(n) | O(n) |
| 堆排序 | 原理清晰的选择式排序 | 建堆后不断弹出堆顶 | O(n log n) | 示例版 O(n) |
| 并查集 | 动态连通性 | 路径压缩 + 按秩合并 | 近似 O(1) | O(n) |

## 第三优先：理解型

| 算法 | 目的 | 核心原理 | 时间复杂度 | 空间复杂度 |
| --- | --- | --- | --- | --- |
| FFT | 快速多项式乘法 | 奇偶拆分，在单位根上分治求值 | O(n log n) | O(n) |
| Strassen | 更快矩阵乘法 | 用 7 次子矩阵乘法替代普通 8 次 | O(n^2.807) | O(n^2) |
| 概率 DP | 计算系列赛获胜概率 | `dp[i][j]` 表示当前比分下最终胜率 | O(k^2) | O(k^2) |
| 随机算法 | 用随机性降低坏情况概率或估计结果 | 随机 pivot、蒙特卡洛采样 | 视算法而定 | 视算法而定 |

## 理论类：考试大题

| 主题 | 你需要会说清楚什么 |
| --- | --- |
| NP 完全问题 | P、NP、NP-hard、NP-complete 的区别；“可快速验证”不等于“可快速求解”。 |
| SAT | CNF 公式是否存在满足赋值；SAT 是第一个被证明的 NP 完全问题。 |
| 3-SAT | 每个子句恰好 3 个文字；它是 SAT 的受限形式，但仍是 NP 完全。 |
| TSP | 判定版是 NP 完全；优化版通常称 NP-hard；小规模可用 Held-Karp 动态规划。 |

## 常见答题模板

动态规划题可以按这个顺序写：

1. 定义状态：例如 `dp[i][c]` 表示前 i 件物品、容量 c 的最大价值。
2. 写转移：不选当前物品和选当前物品取最大。
3. 写初始化：容量为 0 或物品数为 0 时答案为 0。
4. 写遍历顺序：通常从小规模到大规模。
5. 分析复杂度：状态数乘每个状态的转移代价。

贪心题可以按这个顺序写：

1. 描述贪心选择：例如活动选择总选结束最早的活动。
2. 说明为什么不会吃亏：交换论证或最优子结构。
3. 给出算法步骤。
4. 分析排序和扫描的复杂度。

图算法题重点：

- Kruskal 适合边集排序，用并查集判环。
- Dijkstra 只能用于非负边权；有负边时考虑 Bellman-Ford。
- 最小生成树处理的是“连通所有点的最小边权总和”，最短路处理的是“从源点到其他点的最短距离”，别混。
