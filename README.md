# Goldbach Partition Counter

**哥德巴赫分拆数精确计算程序与数据集（10⁸ – 10¹⁴）**
**Exact Goldbach partition numbers from 10⁸ to 10¹⁴: program and released data**

[中文](#中文) | [English](#english)

---
## 📌 学术认可 / Academic Recognition

### 中文
本项目已获得**整型序列百科全书 (OEIS)** 官方审核与收录。
本项目已作为永久外部参考链接，正式挂载于 **[OEIS A045917](https://oeis.org/A045917)**（哥德巴赫分拆数）官方页面：

> **"Zhao Shijian, Goldbach Partition Counter, 2026"**

### English
This project has been officially reviewed and accepted by the **Online Encyclopedia of Integer Sequences (OEIS)**.
It has been officially listed as a permanent external link on the official page of **[OEIS A045917](https://oeis.org/A045917)** (Goldbach partitions):

> **"Zhao Shijian, Goldbach Partition Counter, 2026"**

### ✉️ OEIS 官方来信 / Correspondence
> *"I have attached a link to your repository to A045917. ... By providing the link, we allow interested people to follow your work."*
> — **Sean A. Irvine**, Executive Editor of the OEIS (on behalf of **Neil J. A. Sloane**, President of the OEIS Foundation)
>
> *“我已将你的仓库链接附在 A045917 页面。……通过提供链接，我们允许感兴趣的人继续关注你的工作。”*
> — **肖恩·A·欧文**，OEIS 执行编辑（代表 OEIS 基金会主席 **尼尔·J·A·斯隆**）

---

## 中文

### 项目简介
对给定区间内的每一个偶数 N，本程序精确计算其哥德巴赫分拆数
> r(N) = #{ (p, q) : p ≤ q，p + q = N，p、q 均为素数 }
即把 N 写成两个素数之和的方法数（不计顺序，p = q 算一种）。这一定义与 OEIS [A045917](https://oeis.org/A045917) 一致。
程序采用**双块配对流式**分段埃氏筛 + Numba 编译配对计数，可在普通PC上处理 10¹⁴ 量级的偶数区间。仓库公开 **6 个区间、共 50,410,000 个偶数**的精确分拆数和完整运行日志。

### 为什么需要精确值
现有公开数据（如 Oliveira e Silva 等人到 4×10¹⁸ 的验证）仅确认分拆**存在**；10¹³–10¹⁴ 区间可直接下载、可复现的 r(N) 精确值目前暂无其他来源。本仓库提供：
- 2 到 10⁸ 的全部 5×10⁷ 个偶数的 r(N)（A045917 的前 5×10⁷ 项）；
- 2～10¹⁰（100亿）区间已完成全量偶数分拆计算；完整数据集因文件体量过大，未上传至仓库；
- 10⁹、10¹⁰、10¹¹、10¹³ 区间末端各 100,000 个偶数，以及 10¹⁴ 区间末端 10,000 个偶数的抽样数据；
- 原始未修改运行日志。

这些数据可作为任何分拆数渐近公式、估算方法或统计研究的真实值基准。

### 功能特点

- **精确**：逐个偶数穷举全部素数对，结果为整数真值，不含任何近似。
- **可扩展**：分段筛法，内存占用只由"素数块大小"决定，与目标区间所在位置无关。
- **可配置内存**：默认配置需 64 GB；块大小缩小 10 倍后 16 GB 机器同样可以运行，结果完全相同。
- **可复现**：每个已公开结果都附原始运行日志（`docs/logs/`）。

### 环境要求

**软件**

| 项目 | 要求 |
|---|---|
| Python | ≥ 3.9（日志使用 Anaconda 发行版） |
| NumPy | ≥ 1.24 |
| Numba | ≥ 0.58 |
| 操作系统 | Windows（日志环境）；Linux 应可运行，未测试 |

```bash
pip install -r requirements.txt
```

**硬件**

| 配置 | `BLOCK_SIZE`（每块奇数个数） | 每块整数跨度 | 两块常驻内存 | 运行峰值 | 所需内存 |
|---|---|---|---|---|---|
| 默认（日志所用） | 25,000,000,000 (2.5×10¹⁰) | 5×10¹⁰ | ≈ 30 GB | ≈ 45 GB | **64 GB** |
| 小内存配置 | 2,500,000,000 (2.5×10⁹) | 5×10⁹ | ≈ 3 GB | ≈ 5 GB（估） | **16 GB** |

- 块大小只影响内存和耗时，**不影响计算结果**。
- 核心循环由 Numba 编译为机器码，对单核主频敏感。建议 Intel i9-14900K 5 GHz 以上或同级 CPU。日志耗时在 Intel 14900K、128 GB 内存、Windows 的机器上测得。
- 块大小调小后块数增加 10 倍，每块固定开销累积，总耗时会有所增加（计数部分不变，筛法部分基本不变）。
- 目标区间很小（如 N ≤ 10⁸）时程序会自动截短块，此时内存需求可忽略，任何机器都能跑。

### 快速开始

1. 打开 `goldbach_partition_counter.py`，在文件开头修改参数：

   | 参数 | 含义 | 日志所用值 |
   |---|---|---|
   | `S0` | 起始索引。首个偶数 N = 2·(S0+1) | 见下表 |
   | `S2` | 结束索引。末个偶数 N = 2·S2；偶数个数 = S2 − S0 | 见下表 |
   | `BLOCK_SIZE` | 每块奇数个数（内存开关） | `25_000_000_000`；16 GB 机器改 `2_500_000_000` |
   | `BATCH_SIZE` | 计数阶段每批处理的偶数个数 | `100_000` |
   | `NUM_GROUPS` | 计数阶段并行分组数 | `30` |
   | `NUM_EXTRACT_THREADS` | 筛后提取素数的线程数 | `4` 或 `30`（30 时单块筛法由 16 s 降至 10 s） |

   例：要计算 10¹⁴ 末端 10,000 个偶数，设 `S0 = 49_999_999_990_000`，`S2 = 50_000_000_000_000`。

2. 运行：

   ```bash
   python goldbach_partition_counter.py
   ```

   控制台打印每块筛法耗时、批次进度、总体进度。结果自动保存为 `goldbach_partition_counts_{S0}_{S2}.npy`。

3. 读取结果：

   ```python
   import numpy as np
   S0 = 49_999_999_990_000
   r = np.load("results/goldbach_partition_counts_49999999990000_50000000000000.npy")
   i = 9999                       # 最后一个元素
   N = 2 * (S0 + 1 + i)           # = 100,000,000,000,000
   print(N, r[i])
   ```

### 输出格式

- 文件类型：NumPy `.npy`，一维数组，dtype `int64`。
- 索引约定：`r[i]` 为偶数 `N = 2·(S0 + 1 + i)` 的分拆数，`i = 0 … S2−S0−1`。
- 文件名中的两个整数即运行时的 `S0`、`S2`。

## 查看数据 

### 用 NumPy 读取

`.npy` 文件索引 i 对应 N = 2·(i₀ + i)，i₀ 为文件名中的起始索引：

```python
import numpy as np
a = np.load('results/goldbach_partition_counts_0_5000000.npy')
print(a[1:21].tolist())
# [0, 1, 1, 1, 2, 1, 2, 2, 2, 2, 3, 3, 3, 2, 3, 2, 4, 4, 2, 3]  ← N = 2, 4, …, 40，与 OEIS A045917 一致

无需编写额外代码，可使用 `tools/npy_to_excel.py` 将数据导出为 Excel 或 CSV。

Excel 单个工作表上限为 1,048,576 行；更大的数据范围请使用 `--start/--end` 参数，或选择 CSV 格式。
`results/sample_2_to_100000.xlsx` 由上面的命令生成，可直接打开，例如 r (4)=1（2+2）、r (6)=1（3+3）、r (10)=2（3+7，5+5）。

### 已完成的计算

| # | 偶数范围 | 偶数个数 | 结果文件 | 大小 | 耗时 | 存放 |
|---|---|---|---|---|---|---|
| 1 | 2 – 10⁸ | 50,000,000 | `goldbach_partition_counts_0_50000000.npy` | 400 MB | 10 分 48 秒 | Release 附件 |
| 2 | 999,800,002 – 10⁹ | 100,000 | `goldbach_partition_counts_499900000_500000000.npy` | 800 KB | 19 秒 | `results/` |
| 3 | 9,999,800,002 – 10¹⁰ | 100,000 | `goldbach_partition_counts_4999900000_5000000000.npy` | 800 KB | 2 分 26 秒 | `results/` |
| 4 | 99,999,800,002 – 10¹¹ | 100,000 | `goldbach_partition_counts_49999900000_50000000000.npy` | 800 KB | 20 分 14 秒 | `results/` |
| 5 | 9,999,999,800,002 – 10¹³ | 100,000 | `goldbach_partition_counts_4999999900000_5000000000000.npy` | 800 KB | 24 小时 57 分 | `results/` |
| 6 | 99,999,999,980,002 – 10¹⁴ | 10,000 | `goldbach_partition_counts_49999999990000_50000000000000.npy` | 80 KB | 27 小时 31 分 | `results/` |

统计量、一致性检验和下载方式见 [docs/RESULTS.md](docs/RESULTS.md)。

### 正确性检验

1. 区间 1 中 r(2) = 0，其余 49,999,999 个偶数均 ≥ 1，与哥德巴赫猜想已验证范围一致；
2. 区间 1 的结果数组逐项对应 OEIS A045917 的 a(1) … a(5×10⁷)，可与其 b-file 直接比对（脚本见 RESULTS.md）；
3. 五个窄区间内 r(N) 的均值与 N/ln²N 之比为 1.108、1.096、1.087、1.072、1.067，随 N 增大单调趋近 1，符合 Hardy–Littlewood 渐近预期；
4. 五个窄区间内 r(N) 的最大/最小比值为 4.08、4.34、4.24、4.17、4.03，与奇素因子修正项 ∏(p−1)/(p−2) 在窗口内的取值幅度一致；
5. 四次独立运行的计数吞吐量均为 1.3–1.45×10¹⁰ 素数对/秒，说明耗时与 Σr(N) 严格成正比，没有遗漏或重复计数的迹象。

详见 [docs/RESULTS.md](docs/RESULTS.md)。

### 仓库结构

```
goldbach_partition_counter.py 主程序（单文件，中英注释）
tools/npy_to_excel.py 辅助程序（单文件，中英注释）
requirements.txt 依赖
results/
├── goldbach_partitions_0_to_50000000.npy 381 MB，见 Releases
├── goldbach_partitions_499900000_50000000.npy
├── goldbach_partitions_4999900000_500000000.npy
├── goldbach_partitions_49999900000_5000000000.npy
├── goldbach_partitions_4999999900000_5000000000000.npy
├── goldbach_partitions_49999999900000_50000000000000.npy
└── samples/
        ├── goldbach_partitions_0_to_5000000.npy 验证样本（NumPy 格式，38.1 MB）
        └── goldbach_partitions_0_to_5000000.xlsx 验证样本（Excel 格式，29.9 MB）
docs/
├── ALGORITHM.md 算法原理与实现说明
├── RESULTS.md 数据统计、一致性检验、硬件与耗时
└── logs/ 3 份原始运行日志（中文），1 份英文版
CITATION.cff 引用信息
LICENSE MIT 许可证
```

### 引用

```bibtex
@software{zhao_goldbach_partition_counter_2026,
  author  = {赵时建 (Zhao, Shijian)},
  title   = {Goldbach Partition Counter: exact Goldbach partition numbers
             from 10^8 to 10^14},
  version = {2.0},
  year    = {2026},
  url     = {https://github.com/zhaoshijian2023-hash/goldbach-partition-counter}
 }
```

### 许可证

[MIT](LICENSE)。`results/` 中的数据可自由用于研究，若在出版物中使用请引用本仓库。

### 作者

赵时建（Zhao Shijian）

---

## English

### Overview
For every even integer N in a user-specified interval, this program computes the exact Goldbach partition number
> r(N) = #{ (p, q) : p ≤ q, p + q = N, p and q prime },
the number of unordered representations of N as a sum of two primes (p = q counted once), the same convention as OEIS [A045917](https://oeis.org/A045917).
A **dual-block paired streaming** segmented sieve of Eratosthenes feeds Numba-compiled pair counting, allowing a consumer PC to work at the 10¹⁴ scale. Exact values for **six intervals, 50,410,000 even integers in total**, are released together with the complete run logs.

### Why exact values
Public data such as the verification to 4×10¹⁸ by Oliveira e Silva et al. establish that partitions *exist*. Downloadable, reproducible exact values of r(N) itself at 10¹³–10¹⁴ are not otherwise available. This repository provides
- all 5×10⁷ values of r(N) for 2 ≤ N ≤ 10⁸ (the first 5×10⁷ terms of A045917);
- full computation of partition counts for all even numbers in the range \(2 \sim 10^{10}\) (10 billion) has been completed; the complete dataset is not uploaded to the repository owing to its large file size;
- 100,000 values each at the top of 10⁹, 10¹⁰, 10¹¹ and 10¹³, and 10,000 values at the top of 10¹⁴;
- the unedited run logs.

### Features

- **Exact** – exhaustive enumeration of prime pairs; integer results, no approximation.
- **Scalable** – segmented sieve; memory is governed by one block-size parameter, independent of where the interval lies.
- **Configurable memory** – 64 GB by default; a 10× smaller block runs on 16 GB with identical results.
- **Reproducible** – every result ships with its log.

### Requirements

**Software**: Python ≥ 3.9, NumPy ≥ 1.24, Numba ≥ 0.58 (`pip install -r requirements.txt`). Logs were produced on Windows (Anaconda); Linux should work but is untested.

**Hardware**

| Configuration | `BLOCK_SIZE` (odd integers per block) | Integer span per block | Two resident blocks | Peak | RAM |
|---|---|---|---|---|---|
| Default (logs) | 25,000,000,000 | 5×10¹⁰ | ≈ 30 GB | ≈ 45 GB | **64 GB** |
| Low-memory | 2,500,000,000 | 5×10⁹ | ≈ 3 GB | ≈ 5 GB (est.) | **16 GB** |

Block size affects only memory and run time, never results. The hot loops are single-core-clock sensitive; an Intel 14900K at ≥ 5 GHz or equivalent is recommended. Logged timings: Intel 14900K, 128 GB, Windows. Small intervals (e.g. N ≤ 10⁸) truncate the blocks automatically and need negligible memory.

### Quick start

1. Edit the parameters at the top of `goldbach_partition_counter.py`:

   | Parameter | Meaning | Logged value |
   |---|---|---|
   | `S0` | start index; first N = 2·(S0+1) | see table below |
   | `S2` | end index; last N = 2·S2; count = S2 − S0 | see table below |
   | `BLOCK_SIZE` | odd integers per block (memory knob) | `25_000_000_000`; use `2_500_000_000` on 16 GB |
   | `BATCH_SIZE` | even integers per counting batch | `100_000` |
   | `NUM_GROUPS` | parallel groups in counting | `30` |
   | `NUM_EXTRACT_THREADS` | threads for prime extraction after sieving | `4` or `30` (30 cuts block sieve time from 16 s to 10 s) |

   Example: the top 10,000 even integers below 10¹⁴ are `S0 = 49_999_999_990_000`, `S2 = 50_000_000_000_000`.

2. `python goldbach_partition_counter.py` — output is saved as `goldbach_partition_counts_{S0}_{S2}.npy`.

3. Load:

   ```python
   import numpy as np
   S0 = 49_999_999_990_000
   r = np.load("results/goldbach_partition_counts_49999999990000_50000000000000.npy")
   i = 9999
   print(2 * (S0 + 1 + i), r[i])     # N = 10^14 and its partition number
   ```

## Viewing the data

`.npy` files are read with NumPy; index i corresponds to N = 2·(i₀ + i), where i₀ is the start index in the file name.

(same code block)

Without
 writing code, export to Excel or CSV with `tools/npy_to_excel.py`:

(same commands)

Excel caps a sheet at 1,048,576
 rows; use `--start/--end` or CSV for larger ranges.
`results/sample_2_to_100000.xlsx` was produced by the first command above and can be opened directly, e.g. r(4)=1 (2+2), r(6)=1 (3+3), r(10)=2 (3+7, 5+5).￼


### Completed computations

| # | Even integers N | Count | File | Size | Run time | Where |
|---|---|---|---|---|---|---|
| 1 | 2 – 10⁸ | 50,000,000 | `goldbach_partition_counts_0_50000000.npy` | 400 MB | 10 min 48 s | Release asset |
| 2 | 999,800,002 – 10⁹ | 100,000 | `goldbach_partition_counts_499900000_500000000.npy` | 800 KB | 19 s | `results/` |
| 3 | 9,999,800,002 – 10¹⁰ | 100,000 | `goldbach_partition_counts_4999900000_5000000000.npy` | 800 KB | 2 min 26 s | `results/` |
| 4 | 99,999,800,002 – 10¹¹ | 100,000 | `goldbach_partition_counts_49999900000_50000000000.npy` | 800 KB | 20 min 14 s | `results/` |
| 5 | 9,999,999,800,002 – 10¹³ | 100,000 | `goldbach_partition_counts_4999999900000_5000000000000.npy` | 800 KB | 24 h 57 min | `results/` |
| 6 | 99,999,999,980,002 – 10¹⁴ | 10,000 | `goldbach_partition_counts_49999999990000_50000000000000.npy` | 80 KB | 27 h 31 min | `results/` |

### Validation

1. In interval 1, r(2) = 0 and all other 49,999,999 even integers have r(N) ≥ 1.
2. Interval 1 is term-by-term OEIS A045917, a(1) … a(5×10⁷); a comparison script is given in RESULTS.md.
3. Mean r(N) divided by N/ln²N over the five narrow windows: 1.108, 1.096, 1.087, 1.072, 1.067 — decreasing monotonically towards 1, as the Hardy–Littlewood asymptotics predict.
4. Max/min ratios of r(N) within the windows: 4.08, 4.34, 4.24, 4.17, 4.03, consistent with the spread of ∏(p−1)/(p−2).
5. Counting throughput is 1.3–1.45×10¹⁰ prime pairs/s across all four independent runs, i.e. run time is strictly proportional to Σr(N).

See [docs/RESULTS.md](docs/RESULTS.md).


### Repository Structure

goldbach_partition_counter.py Main program (single file, bilingual comments)
tools/npy_to_excel.py Auxiliary script (single file, bilingual comments)
requirements.txt Dependencies
results/
├── goldbach_partitions_0_to_50000000.npy 381 MB, see Releases
├── goldbach_partitions_499900000_50000000.npy
├── goldbach_partitions_4999900000_500000000.npy
├── goldbach_partitions_49999900000_5000000000.npy
├── goldbach_partitions_4999999900000_5000000000000.npy
├── goldbach_partitions_49999999900000_50000000000000.npy
└── samples/
       ├── goldbach_partitions_0_to_5000000.npy Verification sample (NumPy format，38.1MB)
       └── goldbach_partitions_0_to_5000000.xlsx Verification sample (Excel format, 29.9 MB)
docs/
├── ALGORITHM.md Algorithm principles and implementation
├── RESULTS.md Data statistics, consistency checks, hardware & runtime
└── logs/ 3 running logs (Chinese), 1 English version
CITATION.cff Citation information
LICENSE MIT License
```

### Citation

```bibtex
@software{zhao_goldbach_partition_counter_2026,
  author  = {Zhao, Shijian},
  title   = {Goldbach Partition Counter: exact Goldbach partition numbers
             from 10^8 to 10^14},
  version = {2.0},
  year    = {2026},
  url     = {https://github.com/zhaoshijian2023-hash/goldbach-partition-counter}
```

### License

MIT. Data in `results/` may be used freely for research; please cite this repository in publications.

### Author

Zhao Shijian
