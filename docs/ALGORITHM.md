# 算法原理 / Algorithm

[中文](#中文) | [English](#english)

---

## 中文

本文档说明 `goldbach_partition_counter.py` 的计算方法，与代码的步骤一一对应。性能数字均取自 `docs/logs/` 中的实际运行日志。

### 1. 问题定义

给定索引 start < end，目标偶数为 N = 2n，n = start+1, …, end，共 end − start 个。对每个 N 计算

> r(N) = #{ (p, q) : p ≤ q，p + q = N，p、q 为素数 }，

等价于满足"p 与 N − p 都是素数"的 p ∈ [2, N/2] 的个数。

### 2. 直接方法为何不可行

最直接的做法是筛出 [2, N_max] 内全部素数，再对每个 N 检查 p 与 N − p。N_max = 10¹⁴ 时：

- 按每个奇数 1 bit 存筛表：5×10¹³ bit ≈ 6 TB；
- 按 int64 存素数本身：π(10¹⁴) ≈ 3.2×10¹² 个 × 8 B ≈ 26 TB。

单机无法常驻，磁盘随机访问又慢到不可接受。因此筛素数和配对计数都必须限制在内存能容纳的块上进行。

### 3. 分块配对（"前半区 / 后半区"）

**核心观察**：对目标区间 [A, B] 中任意 N，若 p 落在块 [x, x+L)，则 q = N − p 必落在镜像块 (A − x − L, B − x]。

程序据此组织计算：

1. 把 p 的取值范围 [2, B/2]（代码中称"前半区"）切成若干块，每块含 `BLOCK_SIZE` 个奇数；
2. 对每个前半区块，筛出其中的素数，同时筛出对应的镜像块（"后半区"）中的素数；
3. 对前半区的每个素数 p 和后半区的每个素数 q，若 p + q ∈ [A, B]，则 r(p+q) 加 1；
4. 处理完全部块后 r(N) 即为精确值。

任何时刻内存中只有一对块，这就是"两块常驻内存"的含义。镜像块长度为 L + (B − A)，目标区间远小于块时两块大小相同。

块数 = ⌈(B/2) / L⌉。日志中 L = 5×10¹⁰（2.5×10¹⁰ 个奇数）：

| 目标区间末端 | 块数 |
|---|---|
| ≤ 10¹¹ | 1（自动截短） |
| 10¹³ | 100 |
| 10¹⁴ | 1,000 |

### 4. 分段筛法

- 只处理奇数：每块 2.5×10¹⁰ 个奇数位置；
- 基础素数：√(10¹⁴) = 10⁷ 以内共 664,578 个，程序启动时一次生成（< 1 秒），常驻内存可忽略；
- 对每个基础素数，定位其在块内第一个奇倍数，按步长 2p 标记；
- 筛完后用 `NUM_EXTRACT_THREADS` 个线程并行把块内素数提取为 int64 数组，供计数使用。

**实测筛法耗时**（单个满块，含提取）：`NUM_EXTRACT_THREADS = 4` 时约 16 秒，`= 30` 时约 10 秒。

**内存**：L = 5×10¹⁰（各 250 亿奇数）时：
- 提取出的素数数组（两块）：约 30 GB
- 筛法阶段临时筛表：额外 15 GB
- 其他开销：约 12 GB
- **峰值**（筛法阶段，持续约 10–16 秒）：约 **57 GB**
- **稳定值**（分拆计数阶段）：约 **42 GB**
- 需要 **64 GB** 内存

将 `BLOCK_SIZE` 改为 2,500,000,000 后内存占用约为十分之一，16 GB 机器可运行。

### 5. 计数阶段

计数是耗时主体。实现要点：

- 配对循环用 Numba `@njit` 编译，按 `NUM_GROUPS` 个分组并行；
- 目标偶数按 `BATCH_SIZE` 个一批处理（区间 1 的 5×10⁷ 个偶数即 500 批）；
- 两个素数数组均已有序，对每个 p 只需扫描 q ∈ [A − p, B − p] 这一小段；
- 累加数组 r 为 int64，长度 S2 − S0，常驻但远小于素数块。10¹⁴ 处 r(N) 已达 2.7×10¹¹，超过 uint32 上限 4.29×10⁹，因此必须用 64 位。

### 6. 复杂度与实测性能

- **筛法**：每块 O(L log log B)，与块位置基本无关——日志中各块筛法耗时稳定在 16 s（或 10 s）；
- **计数**：与区间内分拆数之和 Σr(N) 成正比。四次独立运行的吞吐量：

| 运行 | Σr(N) | 计数耗时（总耗时减筛法） | 吞吐量（对/秒） |
|---|---|---|---|
| 区间 1（2–10⁸） | 8.80×10¹² | ≈ 646 s | 1.36×10¹⁰ |
| 区间 4（10¹¹） | 1.69×10¹³ | ≈ 1,180 s | 1.44×10¹⁰ |
| 区间 5（10¹³，100 块） | 1.20×10¹⁵ | ≈ 24.0 h | 1.38×10¹⁰ |
| 区间 6（10¹⁴，1000 块） | 1.03×10¹⁵ | ≈ 21.7 h | 1.31×10¹⁰ |

吞吐量稳定在 1.3–1.45×10¹⁰ 素数对/秒，说明实现没有随规模退化。

- **耗时估算公式**（默认配置）：

  > T ≈ Σr(N) / 1.3×10¹⁰ 秒 + 块数 × 20 秒
  >
  > 其中 Σr(N) ≈ 偶数个数 × N/ln²N × 1.07（10¹³–10¹⁴ 处）

  例：10¹⁴ 末端 10,000 个偶数：1.03×10¹⁵ / 1.3×10¹⁰ ≈ 22 h，加 1000 × 20 s ≈ 5.6 h，合计约 27.5 h，与实测 27 h 31 min 相符。

### 7. 参数选择

| 参数 | 影响 | 建议 |
|---|---|---|
| `BLOCK_SIZE` | 决定内存；越大则块数越少、固定开销越低 | 64 GB 机器 25,000,000,000；16 GB 机器 2,500,000,000 |
| `S2 − S0`（区间宽度） | 决定计数耗时与结果文件大小 | 按可接受时间选择；10¹⁴ 处每 10,000 个偶数约 22 h 计数 |
| `NUM_GROUPS` | 计数并行度 | 取 CPU 逻辑线程数附近 |
| `NUM_EXTRACT_THREADS` | 提取并行度 | 取 CPU 逻辑线程数附近（30 比 4 快约 40%） |
| `BATCH_SIZE` | 每批偶数数 | 100,000 即可，无需调整 |

### 8. 正确性保障

1. 筛法与配对均为穷举，无近似；
2. 分块只是计算顺序的重排，块大小不影响结果；
3. int64 累加器排除溢出；
4. 外部一致性检验见 [RESULTS.md](RESULTS.md)。

---

## English

This document describes the method implemented in `goldbach_partition_counter.py`. Performance figures are taken from the logs in `docs/logs/`.

### 1. Problem

Given indices start < end, the target even integers are N = 2n, n = start+1, …, end (end − start of them). For each, compute

> r(N) = #{ (p, q) : p ≤ q, p + q = N, p, q prime },

equivalently the number of p ∈ [2, N/2] with both p and N − p prime.

### 2. Why the direct approach fails

Sieving all primes up to N_max = 10¹⁴ would need ≈ 6 TB at one bit per odd integer, or ≈ 26 TB to store the π(10¹⁴) ≈ 3.2×10¹² primes as int64. Neither fits in memory, and disk random access is far too slow. Both sieving and counting must therefore be confined to memory-sized blocks.

### 3. Block pairing ("lower half / upper half")

**Key observation**: for any N ∈ [A, B], if p ∈ [x, x+L) then q = N − p lies in the mirror block (A − x − L, B − x].

1. Split the p-range [2, B/2] (the "lower half") into blocks of `BLOCK_SIZE` odd integers.
2. For each lower block, sieve its primes and those of the mirror block (the "upper half").
3. For every p in the lower block and q in the upper block with p + q ∈ [A, B], increment r(p + q).
4. After all blocks, r(N) is exact.

Only one pair of blocks is resident at any time. Number of blocks = ⌈(B/2)/L⌉: 1 (truncated) for B ≤ 10¹¹, 100 for 10¹³, 1,000 for 10¹⁴ with L = 5×10¹⁰.

### 4. Segmented sieve

- Odd integers only: 2.5×10¹⁰ positions per block.
- Base primes below √(10¹⁴) = 10⁷: 664,578 of them, generated once in < 1 s.
- Standard marking with stride 2p from the first odd multiple inside the block.
- Primes are extracted into an int64 array by `NUM_EXTRACT_THREADS` threads.

Measured: ≈ 16 s per full block with 4 extraction threads, ≈ 10 s with 30.

**Memory usage** with L = 5×10¹⁰ (25 billion odd integers per block):
- Extracted prime arrays (two blocks): ≈ 30 GB
- Temporary sieve tables during sieving: additional 15 GB
- Other overhead: ≈ 12 GB
- **Peak** (during sieving, lasting ≈ 10–16 s): ≈ **57 GB**
- **Stable** (during partition counting): ≈ **42 GB**
- **64 GB** required

With `BLOCK_SIZE = 2_500_000_000` memory usage is about one tenth, so 16 GB suffices.

### 5. Counting

- Numba `@njit` pairing loop, parallel over `NUM_GROUPS` groups.
- Targets processed in batches of `BATCH_SIZE` even integers (500 batches for the 5×10⁷ of interval 1).
- Both prime arrays are sorted; for each p only q ∈ [A − p, B − p] is scanned.
- Accumulator r is int64 of length S2 − S0. Since r(N) reaches 2.7×10¹¹ near 10¹⁴, exceeding the uint32 limit 4.29×10⁹, 64-bit is mandatory.

### 6. Complexity and measured performance

Sieving is O(L log log B) per block and position-independent (16 s or 10 s per block throughout the logs). Counting is proportional to Σr(N):

| Run | Σr(N) | Counting time | Throughput (pairs/s) |
|---|---|---|---|
| Interval 1 (2–10⁸) | 8.80×10¹² | ≈ 646 s | 1.36×10¹⁰ |
| Interval 4 (10¹¹) | 1.69×10¹³ | ≈ 1,180 s | 1.44×10¹⁰ |
| Interval 5 (10¹³, 100 blocks) | 1.20×10¹⁵ | ≈ 24.0 h | 1.38×10¹⁰ |
| Interval 6 (10¹⁴, 1000 blocks) | 1.03×10¹⁵ | ≈ 21.7 h | 1.31×10¹⁰ |

**Run-time estimate** (default configuration):

> T ≈ Σr(N) / 1.3×10¹⁰ s + (number of blocks) × 20 s, with Σr(N) ≈ count × N/ln²N × 1.07 at 10¹³–10¹⁴.

For 10,000 even integers below 10¹⁴: 22 h + 5.6 h ≈ 27.5 h, matching the logged 27 h 31 min.

### 7. Parameters

| Parameter | Effect | Recommendation |
|---|---|---|
| `BLOCK_SIZE` | memory; larger → fewer blocks | 25,000,000,000 on 64 GB; 2,500,000,000 on 16 GB |
| `S2 − S0` | counting time and file size | ≈ 22 h per 10,000 even integers at 10¹⁴ |
| `NUM_GROUPS` | counting parallelism | ≈ number of logical CPU threads |
| `NUM_EXTRACT_THREADS` | extraction parallelism | ≈ number of logical threads (30 is ~40 % faster than 4) |
| `BATCH_SIZE` | targets per batch | 100,000; no tuning needed |

### 8. Correctness

Exhaustive sieve and pairing with no approximation; blocking only reorders the work; int64 excludes overflow. External checks: see [RESULTS.md](RESULTS.md).