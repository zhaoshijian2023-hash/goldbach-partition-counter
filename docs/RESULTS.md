# 结果数据与检验 / Results and Validation

[中文](#中文) | [English](#english)

---

## 中文

### 1. 数据文件一览

| # | S0 | S2 | 偶数范围 | 偶数个数 | 文件名 | 大小 | 存放 | 日志 |
|---|---|---|---|---|---|---|---|---|
| 1 | 0 | 50,000,000 | 2 – 10⁸ | 50,000,000 | `goldbach_partition_counts_0_50000000.npy` | 400 MB | Release v2.0 附件 | `run1_1e8_to_1e11.log` |
| 2 | 499,900,000 | 500,000,000 | 999,800,002 – 10⁹ | 100,000 | `goldbach_partition_counts_499900000_500000000.npy` | 800 KB | `results/` | 同上 |
| 3 | 4,999,900,000 | 5,000,000,000 | 9,999,800,002 – 10¹⁰ | 100,000 | `goldbach_partition_counts_4999900000_5000000000.npy` | 800 KB | `results/` | 同上 |
| 4 | 49,999,900,000 | 50,000,000,000 | 99,999,800,002 – 10¹¹ | 100,000 | `goldbach_partition_counts_49999900000_50000000000.npy` | 800 KB | `results/` | 同上 |
| 5 | 4,999,999,900,000 | 5,000,000,000,000 | 9,999,999,800,002 – 10¹³ | 100,000 | `goldbach_partition_counts_4999999900000_5000000000000.npy` | 800 KB | `results/` | `run2_1e13_100000.log` |
| 6 | 49,999,999,990,000 | 50,000,000,000,000 | 99,999,999,980,002 – 10¹⁴ | 10,000 | `goldbach_partition_counts_49999999990000_50000000000000.npy` | 80 KB | `results/` | `run3_1e14_10000.log` |

所有文件 dtype 均为 `int64`。文件 1 超过 GitHub 100 MB 限制，作为 [Releases](../../releases) 页面 v2.0 的附件提供，SHA-256: `(will be added after upload)`

### 2. 文件格式与读取

一维数组，`r[i]` 对应偶数 `N = 2·(S0 + 1 + i)`。

```python
import numpy as np

S0 = 4_999_999_900_000
r = np.load("results/goldbach_partition_counts_4999999900000_5000000000000.npy")

i = 1000
print(f"N = {2*(S0+1+i)}, r(N) = {r[i]}")

print("count:", r.size)
print("sum  :", int(r.sum()))
print("min  :", r.min(), "at N =", 2*(S0+1+int(r.argmin())))
print("max  :", r.max(), "at N =", 2*(S0+1+int(r.argmax())))
```

### 3. 各区间统计量（摘自日志）

| # | 偶数范围 | Σr(N) | 平均值 | 最小值 | 最大值 | max/min |
|---|---|---|---|---|---|---|
| 1 | 2 – 100,000,000 | 8,804,091,976,100 | 176,081.84 | 0（仅 N=2） | 931,793 | — |
| 2 | 999,800,002 – 1,000,000,000 | 258,061,302,293 | 2,580,613.02 | 1,700,413 | 6,945,267 | 4.08 |
| 3 | 9,999,800,002 – 10,000,000,000 | 2,067,765,005,068 | 20,677,650.05 | 13,642,231 | 59,206,649 | 4.34 |
| 4 | 99,999,800,002 – 100,000,000,000 | 16,938,711,667,770 | 169,387,116.68 | 111,800,676 | 473,687,623 | 4.24 |
| 5 | 9,999,999,800,002 – 10,000,000,000,000 | 1,196,643,430,857,110 | 11,966,434,308.57 | 7,899,589,779 | 32,977,156,851 | 4.17 |
| 6 | 99,999,999,980,002 – 100,000,000,000,000 | 1,026,454,633,774,816 | 102,645,463,377.48 | 67,762,050,004 | 273,105,181,124 | 4.03 |

区间 2–5 各含 100,000 个连续偶数（宽 199,998），区间 6 含 10,000 个（宽 19,998），均以 10ᵏ 为末端。

### 4. 一致性检验

#### 4.1 哥德巴赫猜想已验证范围

区间 1 中"有分拆的偶数"为 49,999,999 / 50,000,000，唯一例外是 N = 2（1 不是素数）。所有 N ≥ 4 均有 r(N) ≥ 1，与猜想在 4×10¹⁸ 以内已被验证的事实一致。

#### 4.2 与 OEIS A045917 比对

[A045917](https://oeis.org/A045917)（2n 的无序素数对分拆数）首项为 0, 1, 1, 1, 2, 1, 2, 2, 2, 2, 3, …。区间 1 的 `r[n−1]` 即 a(n)，n = 1 … 5×10⁷。OEIS 提供前 10,000 项的 b-file，可用下面脚本直接比对：

```python
import numpy as np, urllib.request

r = np.load("goldbach_partition_counts_0_50000000.npy")
txt = urllib.request.urlopen("https://oeis.org/A045917/b045917.txt").read().decode()
oeis = {int(a): int(b) for a, b in (ln.split() for ln in txt.splitlines() if ln and not ln.startswith("#"))}
print(all(r[n-1] == v for n, v in oeis.items()), len(oeis), "terms compared")
```

本仓库发布前已运行该脚本并输出 `True`。
# 输出示例：True 10000 terms compared

#### 4.3 与 Hardy–Littlewood 渐近量级的一致性

Hardy–Littlewood 猜想给出（无序计数）

> r(N) ~ C₂ · ∏_{p|N, p>2} (p−1)/(p−2) · N / ln²N，　C₂ ≈ 0.660

修正项 ∏(p−1)/(p−2) 在偶数上的平均值恰为 1/C₂，因此**窄窗口内 r(N) 的均值应接近 N/ln²N**，且由于存在正的低阶项，比值应略大于 1 并随 N 增大趋近 1。实测：

| 区间 | N | N/ln²N | 均值 | 均值 ÷ (N/ln²N) |
|---|---|---|---|---|
| 2 | 10⁹ | 2.329×10⁶ | 2.581×10⁶ | 1.108 |
| 3 | 10¹⁰ | 1.886×10⁷ | 2.068×10⁷ | 1.096 |
| 4 | 10¹¹ | 1.559×10⁸ | 1.694×10⁸ | 1.087 |
| 5 | 10¹³ | 1.116×10¹⁰ | 1.197×10¹⁰ | 1.072 |
| 6 | 10¹⁴ | 9.623×10¹⁰ | 1.026×10¹¹ | 1.067 |

比值单调下降、趋近 1，与预期一致。

**最大/最小比值**：窄窗口内，N = 2×素数型的偶数修正项 ≈ 1；N 为 30030 = 2·3·5·7·11·13 的倍数时修正项 = 2 × 4/3 × 6/5 × 10/9 × 12/11 ≈ 3.88，再含因子 17 则 ≈ 4.14。宽 2×10⁵ 的窗口必含 30030 的倍数；10¹⁴ 窗口（宽 2×10⁴）也含 99,999,999,999,900 = 30030 × 3,330,003,330。因此预期 max/min 在 4 附近，实测 4.03–4.34，一致。

以上只是数量级检验，不涉及任何拟合。

#### 4.4 耗时与 Σr(N) 成正比

见 [ALGORITHM.md §6](ALGORITHM.md)：四次独立运行的计数吞吐量均为 1.3–1.45×10¹⁰ 对/秒。若存在遗漏或重复计数，不同规模的运行之间不会得到一致的吞吐量。

### 5. 运行日志

`docs/logs/` 中三份日志为控制台原始输出：

| 文件 | 内容 | 参数 |
|---|---|---|
| `run1_1e8_to_1e11.log` | 区间 1–4 连续运行 | BLOCK_SIZE 2.5×10¹⁰，NUM_EXTRACT_THREADS 4 |
| `run2_1e13_100000.log` | 区间 5，100 块 | 同上 |
| `run3_1e14_10000.log` | 区间 6，1000 块 | NUM_EXTRACT_THREADS 30 |

说明：

- 日志由 `goldbach_partition_counter_1.py` 产生（与仓库中 `goldbach_partition_counter.py` 完全相同）；
- `run1` 中部分"本块进度 / ETA"行与其他输出交错（如出现 "ETA: 45小时47分"），是进度刷新线程与主线程打印交错所致，与计算无关；
- `run2`、`run3` 中间块（第 12–97 块、第 11–979 块）的重复行已省略，用 "……" 标出；每块耗时见"平均块用时 / 最快块 / 最慢块"。

### 6. 硬件与耗时

| 项目 | 取值 |
|---|---|
| CPU | Intel i9-14900K（5 GHz 级） |
| 内存 | 64 GB |
| 操作系统 | Windows |
| Python 发行版 | Anaconda |
| BLOCK_SIZE | 25,000,000,000 |
| 两块常驻内存 / 计数阶段 / 峰值 | ≈ 30 GB / ≈ 42 GB / ≈ 57 GB（筛法时） |

| 区间 | 块数 | 单块筛法 | 单块平均用时 | 最快 / 最慢块 | 总用时 |
|---|---|---|---|---|---|
| 1 | 1 | 1.4 s（截短） | 10 分 46 秒 | — | 10 分 48 秒 |
| 2 | 1 | 0.2 s（截短） | 18 秒 | — | 19 秒 |
| 3 | 1 | 1.6 s（截短） | 2 分 26 秒 | — | 2 分 26 秒 |
| 4 | 1 | 16 s | 20 分 13 秒 | — | 20 分 14 秒 |
| 5 | 100 | 16 s + 16 s | 14 分 58 秒 | 14 分 19 秒 / 26 分 54 秒 | 24 小时 57 分 |
| 6 | 1000 | 10 s + 11 s | 1 分 38 秒 | 1 分 30 秒 / 4 分 40 秒 | 27 小时 31 分 |

六个区间合计约 53 小时。

### 7. 数据使用声明

所有数值均为精确值，欢迎用于独立研究、核验或作为估算方法的基准。若在出版物中使用，请按 README 中的格式引用本仓库。

---

## English

### 1. Data files

| # | S0 | S2 | Even integers | Count | File | Size | Location | Log file |
|---|---|---|---|---|---|---|---|---|
| 1 | 0 | 50,000,000 | 2 – 10⁸ | 50,000,000 | `goldbach_partition_counts_0_50000000.npy` | 400 MB | Release v2.0 | `run1_1e8_to_1e11.log` |
| 2 | 499,900,000 | 500,000,000 | 999,800,002 – 10⁹ | 100,000 | `goldbach_partition_counts_499900000_500000000.npy` | 800 KB | `results/` | same |
| 3 | 4,999,900,000 | 5,000,000,000 | 9,999,800,002 – 10¹⁰ | 100,000 | `goldbach_partition_counts_4999900000_5000000000.npy` | 800 KB | `results/` | same |
| 4 | 49,999,900,000 | 50,000,000,000 | 99,999,800,002 – 10¹¹ | 100,000 | `goldbach_partition_counts_49999900000_50000000000.npy` | 800 KB | `results/` | same |
| 5 | 4,999,999,900,000 | 5,000,000,000,000 | 9,999,999,800,002 – 10¹³ | 100,000 | `goldbach_partition_counts_4999999900000_5000000000000.npy` | 800 KB | `results/` | `run2_1e13_100000.log` |
| 6 | 49,999,999,990,000 | 50,000,000,000,000 | 99,999,999,980,002 – 10¹⁴ | 10,000 | `goldbach_partition_counts_49999999990000_50000000000000.npy` | 80 KB | `results/` | `run3_1e14_10000.log` |

All files are `int64`. File 1 exceeds GitHub's 100 MB limit and is attached to Release v2.0; SHA-256: `(will be added after upload)`
### 2. Format and loading

One-dimensional array; `r[i]` is r(N) for `N = 2·(S0 + 1 + i)`. See the Python snippet in the Chinese section (identical code).

### 3. Statistics (from logs)

| # | Even integers N | Σr(N) | Mean | Min | Max | Max/Min |
|---|---|---|---|---|---|---|
| 1 | 2 – 100,000,000 | 8,804,091,976,100 | 176,081.84 | 0 (N=2 only) | 931,793 | — |
| 2 | 999,800,002 – 1,000,000,000 | 258,061,302,293 | 2,580,613.02 | 1,700,413 | 6,945,267 | 4.08 |
| 3 | 9,999,800,002 – 10,000,000,000 | 2,067,765,005,068 | 20,677,650.05 | 13,642,231 | 59,206,649 | 4.34 |
| 4 | 99,999,800,002 – 100,000,000,000 | 16,938,711,667,770 | 169,387,116.68 | 111,800,676 | 473,687,623 | 4.24 |
| 5 | 9,999,999,800,002 – 10,000,000,000,000 | 1,196,643,430,857,110 | 11,966,434,308.57 | 7,899,589,779 | 32,977,156,851 | 4.17 |
| 6 | 99,999,999,980,002 – 100,000,000,000,000 | 1,026,454,633,774,816 | 102,645,463,377.48 | 67,762,050,004 | 273,105,181,124 | 4.03 |

Intervals 2–5 each contain 100,000 consecutive even integers (width 199,998), interval 6 contains 10,000 (width 19,998); all end exactly at 10ᵏ.

### 4. Consistency checks

**4.1 Goldbach.** In interval 1, 49,999,999 of 50,000,000 even integers have r(N) ≥ 1; the sole exception is N = 2.

#### 4.2 Comparison with OEIS A045917

[A045917](https://oeis.org/A045917) (number of unordered prime-pair partitions of 2n) begins 0, 1, 1, 1, 2, 1, 2, 2, 2, 2, 3, … Interval 1's `r[n−1]` equals a(n) for n = 1 … 5×10⁷. OEIS provides a b-file of the first 10,000 terms; the following script compares them directly:

```python
import numpy as np, urllib.request

r = np.load("goldbach_partition_counts_0_50000000.npy")
txt = urllib.request.urlopen("https://oeis.org/A045917/b045917.txt").read().decode()
oeis = {int(a): int(b) for a, b in (ln.split() for ln in txt.splitlines() if ln and not ln.startswith("#"))}
print(all(r[n-1] == v for n, v in oeis.items()), len(oeis), "terms compared")
# Output example: True 10000 terms compared

**4.3 Hardy–Littlewood order of magnitude.** With the unordered convention r(N) ~ C₂ ∏_{p|N,p>2}(p−1)/(p−2) · N/ln²N and the average of the product over even N equal to 1/C₂, the window mean should be close to N/ln²N, slightly above it, and approach it as N grows. Measured ratios mean ÷ (N/ln²N): 1.108 (10⁹), 1.096 (10¹⁰), 1.087 (10¹¹), 1.072 (10¹³), 1.067 (10¹⁴) — monotone towards 1.

Max/min: the factor is ≈ 1 for N = 2·prime and ≈ 3.88 for multiples of 30030 (≈ 4.14 with 17 as well). Every window contains a multiple of 30030 (the 10¹⁴ window contains 99,999,999,999,900 = 30030 × 3,330,003,330), so a ratio near 4 is expected; measured 4.03–4.34. Order-of-magnitude check only; no fitting.

**4.4 Run time ∝ Σr(N).** Counting throughput is 1.3–1.45×10¹⁰ pairs/s in all four independent runs (ALGORITHM.md §6); missed or duplicated pairs would break this consistency.

### 5. Run logs

Three unedited console logs in docs/logs/:

File	Content	Parameters
run1_1e8_to_1e11.log	Intervals 1–4 (continuous run)	BLOCK_SIZE 2.5×10¹⁰, NUM_EXTRACT_THREADS 4
run2_1e13_100000.log	Interval 5, 100 blocks	same
run3_1e14_10000.log	Interval 6, 1000 blocks	NUM_EXTRACT_THREADS 30
Notes:

The logs were produced by goldbach_partition_counter_1.py (identical to goldbach_partition_counter.py in the repository).
In run1, some "block progress / ETA" lines are interleaved with other output (e.g., "ETA: 45小时47分") due to concurrent printing by the progress-refresh thread and the main thread; this does not affect computation.
In run2 and run3, repetitive middle blocks (blocks 12–97 and 11–979, respectively) are elided with "……"; per-block timing is shown in "average / fastest / slowest block" statistics.

### 6. Hardware and timing

Intel i9-14900K (5 GHz class), 64 GB RAM, Windows, Anaconda Python; BLOCK_SIZE 25,000,000,000; | Two resident blocks / counting / peak | ≈ 30 GB / ≈ 42 GB / ≈ 57 GB (sieving) |

| Interval | Blocks | Sieve per block | Mean block time | Fastest / slowest | Total |
|---|---|---|---|---|---|
| 1 | 1 | 1.4 s (truncated) | 10 min 46 s | — | 10 min 48 s |
| 2 | 1 | 0.2 s | 18 s | — | 19 s |
| 3 | 1 | 1.6 s | 2 min 26 s | — | 2 min 26 s |
| 4 | 1 | 16 s | 20 min 13 s | — | 20 min 14 s |
| 5 | 100 | 16 s + 16 s | 14 min 58 s | 14 min 19 s / 26 min 54 s | 24 h 57 min |
| 6 | 1000 | 10 s + 11 s | 1 min 38 s | 1 min 30 s / 4 min 40 s | 27 h 31 min |

About 53 hours in total.

### 7. Data use

All values are exact and may be used freely for research, verification or benchmarking; please cite the repository in publications.