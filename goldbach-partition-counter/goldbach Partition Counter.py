"""
Goldbach Partition Counter - 哥德巴赫分拆数精确计算器
Goldbach Partition Counter - Precise Calculator for Goldbach Partition Numbers
============================================================

计算哥德巴赫分拆数 g(2n) 的精确值：
Calculate the exact value of Goldbach partition number g(2n):
g(2n) = 偶数 2n 表示为两个素数之和的方案数
g(2n) = number of ways to express even number 2n as sum of two primes

核心算法 | Core Algorithm:
  1. 实时素数筛选（埃拉托斯特尼筛法）
     Real-time prime sieving (Sieve of Eratosthenes)
  2. 流式块配对（分块处理，内存友好）
     Streaming block pairing (memory-efficient chunking)
  3. 双索引优化（利用单调性避免重复搜索）
     Dual-index optimization (leveraging monotonicity)

性能特点 | Performance Features:
  - 16GB 内存可计算到 10^12 | 16GB RAM can compute up to 10^12
  - 64GB 内存可计算到 10^14 | 64GB RAM can compute up to 10^14
  - 多线程并行加速 | Multi-threaded parallel acceleration
  - 自适应块大小优化 | Adaptive block size optimization

作者 | Author: 赵时建
版本 | Version: 2.0
日期 | Date: 2026-08-28

============================================================
计算规模指导说明 | Calculation Scale Guidelines
============================================================

一、核心概念说明 | Core Concept Explanation
------------------------------------------------------------

索引范围 | Index range: n ∈ (s0, s2]
对应偶数 | Corresponding even numbers: 2n = 2*n
偶数范围 | Even number range: 2n ∈ [2*s0+2, 2*s2]
计算个数 | Number of calculations: s2 - s0

示例 | Example:
calculation_ranges = [(0, 50000000)]
  → 索引范围 | Index range: n ∈ (0, 50000000]
  → 偶数范围 | Even range: 2n ∈ [2, 100000000]
  → 计算个数 | Calculation count: 50000000 - 0 = 5000万 | 50M

------------------------------------------------------------
二、硬件配置与计算规模对照表
Hardware Configuration and Calculation Scale Reference
------------------------------------------------------------

1. 标准配置（16GB 内存，8-16核CPU）
   Standard Configuration (16GB RAM, 8-16 cores)
   
   适合计算范围 | Suitable calculation range:
   - 偶数最大值 2*s2 ≤ 10^12（1万亿 | 1 trillion）
   - 即索引上限 s2 ≤ 5×10^11（5000亿 | 500 billion）
   
   分拆数个数建议 | Recommended partition count (s2-s0):
   - 小数范围（2*s2 < 10^10）: 不超过 50,000,000（5000万 | 50M）
   - 大数范围（2*s2 ≥ 10^10）: 建议 10,000 ~ 1,000,000（1万-100万 | 10K-1M）
   
   示例配置 | Example configurations:
   
   # 小数范围示例 | Small number example:
   calculation_ranges = [(0, 50000000)]
   Config.BLOCK_SIZE = 2_500_000_000
   Config.BATCH_SIZE = 100_000
   
   # 大数范围示例 | Large number example:
   calculation_ranges = [(499999000000, 500000000000)]  # 100万个 | 1M
   Config.BLOCK_SIZE = 2_500_000_000
   Config.BATCH_SIZE = 100_000
   
   峰值内存占用 | Peak memory usage:
   - BLOCK_SIZE = 2_500_000_000（25亿奇数 / 2.5B odds）
   - 素数表二块: ~3 GB | Two prime blocks: ~3 GB
   - 筛选峰值: ~1 GB | Sieving peak: ~1 GB
   - 其他开销: ~10 GB | Other overhead: ~10 GB
   - 峰值总计: ~15 GB < 16 GB ✓ | Total peak: ~15 GB < 16 GB ✓

2. 服务器级配置（64GB 内存，32核+CPU）
   Server-grade Configuration (64GB RAM, 32+ cores)
   
   适合计算范围 | Suitable calculation range:
   - 偶数最大值 2*s2 ≤ 10^14（100万亿 | 100 trillion）
   - 即索引上限 s2 ≤ 5×10^13（50万亿 | 50 trillion）
   
   分拆数个数建议 | Recommended partition count (s2-s0):
   - 小数范围（2*s2 < 10^10）: 不超过 50,000,000（5000万 | 50M）
   - 大数范围（2*s2 ≥ 10^10）: 建议 10,000 ~ 100,000（1万-10万 | 10K-100K）
     * 注：10^14 规模计算 100,000 个约需 11.5 天 | Note: ~11.5 days for 100K at 10^14
   
   示例配置 | Example configurations:
   
   # 小数范围示例 | Small number example:
   calculation_ranges = [(0, 50000000)]
   Config.BLOCK_SIZE = 25_000_000_000
   Config.BATCH_SIZE = 100_000
   
   # 大数范围示例 | Large number example:
   calculation_ranges = [(49999999990000, 50000000000000)]  # 1万个 | 10K
   Config.BLOCK_SIZE = 25_000_000_000
   Config.BATCH_SIZE = 100_000
   
   峰值内存占用 | Peak memory usage:
   - BLOCK_SIZE = 25_000_000_000（250亿奇数 / 25B odds）
   - 素数表二块: ~30 GB | Two prime blocks: ~30 GB
   - 筛选峰值: ~15 GB | Sieving peak: ~15 GB
   - 其他开销: ~12 GB | Other overhead: ~12 GB
   - 峰值总计: ~57 GB < 64 GB ✓ | Total peak: ~57 GB < 64 GB ✓

------------------------------------------------------------
三、性能估算 | Performance Estimation
------------------------------------------------------------

基于实际测试日志（64GB 内存，16核CPU，峰值45GB）
Based on actual test logs (64GB RAM, 16 cores, peak 45GB usage)

计算时间统计（每 10,000 个偶数）| Time per 10,000 evens:

| 偶数规模 | 10,000 个耗时 | 配置 |
| Even scale | Time for 10K | Config |
|-----------|--------------|--------|
| 10^8（1亿 / 100M） | ~1.3秒 / ~1.3s | BLOCK_SIZE = 2.5×10^9 |
| 10^9（10亿 / 1B） | ~1.9秒 / ~1.9s | BLOCK_SIZE = 2.5×10^9 |
| 10^10（100亿 / 10B） | ~15秒 / ~15s | BLOCK_SIZE = 2.5×10^9 |
| 10^11（1000亿 / 100B） | ~2分 / ~2min | BLOCK_SIZE = 2.5×10^9 |
| 10^12（1万亿 / 1T） | ~2.5小时 / ~2.5hrs | BLOCK_SIZE = 2.5×10^10 |
| 10^14（100万亿 / 100T） | ~27.5小时 / ~27.5hrs | BLOCK_SIZE = 2.5×10^10 |
注：100,000 个耗时约为 10,000 个的 10 倍
Note: 100,000 evens take approximately 10× the time of 10,000 evens

内存占用 | Memory usage:
- BLOCK_SIZE = 2.5×10^9: 峰值 ~3.5 GB
- BLOCK_SIZE = 2.5×10^10: 峰值 ~35 GB

------------------------------------------------------------
四、分段计算策略 | Segmented Calculation Strategy
------------------------------------------------------------

对于超大规模计算，建议分段执行：
For ultra-large calculations, segmented execution is recommended:

策略1：小数范围连续计算 | Continuous calculation for small numbers
calculation_ranges = [
    (0, 50000000),        # 2 到 10^8
]

策略2：大数范围目标区间 | Target intervals for large numbers
calculation_ranges = [
    (499900000, 500000000),                 # 10^9 附近 100,000 个
    (4999900000, 5000000000),               # 10^10 附近 100,000 个
    (49999900000, 50000000000),             # 10^11 附近 100,000 个
    (4999999900000, 5000000000000),         # 10^12 附近 100,000 个
    (49999999990000, 50000000000000),       # 10^14 附近 10,000 个
]

策略3：多机并行分段 | Multi-machine parallel segmentation
# 机器 A | Machine A
calculation_ranges = [(0, 50000000), (50000000, 100000000)]
# 机器 B | Machine B
calculation_ranges = [(100000000, 150000000), (150000000, 200000000)]

分段优势 | Advantages:
- 可随时中断，已完成部分不丢失 | Interruptible without data loss
- 便于多机并行计算 | Easy multi-machine parallelization
- 降低单次运行风险 | Reduced single-run risk
- 灵活调整计算目标 | Flexible calculation targets

============================================================
"""
import numpy as np
import time
import gc
import threading
from numba import njit, prange
import os

# ============================================================================
# 全局配置参数 | Global Configuration Parameters
# ============================================================================

class Config:
    """
    全局配置类 - 统一管理所有可调参数
    Global Configuration - Centralized parameter management
    """

    # ========== 并行计算参数 | Parallel Computing Parameters ==========
    NUM_GROUPS = 30  # 分拆计算的线程组数 | Thread groups for partition calculation
    NUM_EXTRACT_THREADS = 30  # 素数提取的线程数 | Threads for prime extraction

    # ========== 内存与分块参数 | Memory and Chunking Parameters ==========
    BLOCK_SIZE = 25_000_000_000  # L2层块大小（前半区）| L2 block size (frontend)
    BATCH_SIZE = 100_000  # 分拆计算批次大小 | Batch size for partition calculation

    # ========== 素数筛选参数 | Prime Sieving Parameters ==========
    BASE_PRIMES_LIMIT = 10_000_000  # L1层基础素数上限 | L1 base primes limit

    # 自适应分块大小（根据索引范围动态调整）
    # Adaptive chunk size (dynamically adjusted based on index range)
    SIEVE_CHUNK_SIZE_SMALL = 2_000_000  # 小范围分块 | Small-range chunks
    SIEVE_CHUNK_SIZE_LARGE = 2_500_000  # 大范围分块 | Large-range chunks
    SIEVE_THRESHOLD = 1_875_000_000_000_000  # 切换阈值 | Switching threshold

    # ========== 进度监控参数 | Progress Monitoring Parameters ==========
    PROGRESS_UPDATE_INTERVAL = 5  # 块级进度更新间隔（秒）| Block-level update interval (sec)
    BATCH_PROGRESS_INTERVAL = 1  # 批次级进度更新间隔（秒）| Batch-level update interval (sec)
    BATCH_REPORT_FREQUENCY = 5000  # 批次内报告频率（每N个元素）| In-batch report frequency (every N elements)

    # ========== ETA计算参数 | ETA Calculation Parameters ==========
    ETA_STABLE_THRESHOLD = 60  # 启用稳定ETA算法的最小时间（秒）| Min time for stable ETA (sec)

    # ========== 输出参数 | Output Parameters ==========
    DEFAULT_OUTPUT_DIR = 'results'  # 默认输出目录 | Default output directory
    OUTPUT_FILE_PREFIX = 'goldbach_partition_counts'  # 输出文件前缀 | Output file prefix


# 提取 Config 常量供 JIT 函数使用
# Extract Config constants for JIT functions
NUM_GROUPS = Config.NUM_GROUPS
NUM_EXTRACT_THREADS = Config.NUM_EXTRACT_THREADS
SIEVE_CHUNK_SIZE_SMALL = Config.SIEVE_CHUNK_SIZE_SMALL
SIEVE_CHUNK_SIZE_LARGE = Config.SIEVE_CHUNK_SIZE_LARGE
SIEVE_THRESHOLD = Config.SIEVE_THRESHOLD
BATCH_REPORT_FREQUENCY = Config.BATCH_REPORT_FREQUENCY


# ============================================================================
# 语言配置 | Language Configuration
# ============================================================================

LANGUAGE = "zh"  # 可选 | Options: "zh" (中文), "en" (English)

# 多语言文本字典 | Multilingual text dictionary
MESSAGES = {
    "zh": {
        "generate_base_primes": "🔢 生成基础素数到",
        "base_primes_complete": "  ✅ 生成 {} 个基础素数",
        "sieve_start": "\n开始筛选...",
        "start_calculation": "🚀 开始计算哥德巴赫分拆数",
        "step1": "📊 步骤1: 生成基础素数...",
        "step1_complete": "  ✅ 基础素数生成完成，用时: {}",
        "step2": "\n📊 步骤2: 计算全局参数...",
        "target_range": "  目标偶数范围: {} 个 ({} 到 {})",
        "frontend_max": "  前半区最大索引 ii_max: {}",
        "backend_min": "  后半区最小索引 jj_min: {}",
        "step3": "\n🎯 步骤3: 计算处理范围...",
        "block_estimate": "  预计需要处理前半区块: 1 到 {}",
        "init_array": "  ✅ 初始化分拆数数组: {} 个偶数",
        "block_frontend_sieve": "\n🔍 块{} 前半区筛选，计算中...",
        "frontend_complete": "✅ 筛选完成！耗时: {:.3f} 秒，前半区索引：{}——{}",
        "block_backend_sieve": "🔍 块{} 后半区筛选，计算中...",
        "backend_complete": "✅ 筛选完成！耗时: {:.3f} 秒，后半区索引：{}——{}",
        "block_complete": "    ✅ 块{}完成，用时: {}",
        "no_primes": " ⚠️ 无素数，跳过",
        "save_result": "\n💾 结果已保存到: {}",
        "save_failed": "\n⚠️ 保存失败: {}",
        "calculation_complete": "\n🎉 计算完成!",
        "final_stats": "📊 最终统计:",
        "processed_evens": "  处理偶数数量: {}",
        "total_partitions": "  分拆数总和: {}",
        "nonzero_evens": "  有分拆的偶数: {}",
        "avg_partitions": "  平均分拆数: {:.2f}",
        "min_partitions": "  最小分拆数: {}",
        "max_partitions": "  最大分拆数: {}",
        "total_time": "  总用时: {}",
        "time_analysis": "\n⏱️  时间详细分析:",
        "blocks_processed": "  处理块数: {}",
        "avg_block_time": "  平均块用时: {}",
        "fastest_block": "  最快块: {}",
        "slowest_block": "  最慢块: {}",
        "block_efficiency": "  块处理效率: {:.2f} 块/小时",
        "avg_nonzero": "  有分拆偶数的平均分拆数: {:.2f}",
        "progress_batch": "\r      🔄 本块进度: {:.1f}% | 批次: {}/{} ({:.1f}%) | 已用时: {} | ETA: {}",
        "progress_block": "\r📊 总体进度: {:.1f}% ({}/{}) | 块{}运行中：已用时 {}，预计还需 {}",
        "calculating": "计算中...",
        "plan_ranges": "📊 计划计算 {} 个区间:",
        "range_info": "  区间 {}: S0={} → S2={}",
        "actual_range": "         实际偶数范围: {} 到 {} (共 {} 个)",
        "current_config": "⚙️  当前参数配置:",
        "start_range": "\n🚀 开始计算区间 {}/{}",
        "current_params": "📊 当前参数:",
        "s0_param": "  起始索引 S0 = {}",
        "s2_param": "  结束索引 S2 = {}",
        "actual_even_range": "  实际偶数范围: {} 到 {}",
        "calculation_count": "  计算数量: {} 个连续偶数",
        "range_success": "\n✅ 区间 {} 计算成功!",
        "range_failed": "\n❌ 区间 {} 计算失败: {}",
        "continue_next": "⚠️  继续执行下一个区间...",
        "all_complete": "\n🎉 所有区间计算完成!",
    },
    "en": {
        "generate_base_primes": "🔢 Generating base primes up to",
        "base_primes_complete": "  ✅ Generated {} base primes",
        "sieve_start": "\nSieving started...",
        "start_calculation": "🚀 Starting Goldbach partition number calculation",
        "step1": "📊 Step 1: Generate base primes...",
        "step1_complete": "  ✅ Base primes generation complete, time: {}",
        "step2": "\n📊 Step 2: Calculate global parameters...",
        "target_range": "  Target even number range: {} numbers ({} to {})",
        "frontend_max": "  Frontend max index ii_max: {}",
        "backend_min": "  Backend min index jj_min: {}",
        "step3": "\n🎯 Step 3: Calculate processing range...",
        "block_estimate": "  Estimated frontend blocks to process: 1 to {}",
        "init_array": "  ✅ Initialized partition array: {} even numbers",
        "block_frontend_sieve": "\n🔍 Block {} frontend sieving in progress...",
        "frontend_complete": "✅ Sieving complete! Time: {:.3f} sec, frontend index: {}—{}",
        "block_backend_sieve": "🔍 Block {} backend sieving in progress...",
        "backend_complete": "✅ Sieving complete! Time: {:.3f} sec, backend index: {}—{}",
        "block_complete": "    ✅ Block {} complete, time: {}",
        "no_primes": " ⚠️ No primes, skipping",
        "save_result": "\n💾 Results saved to: {}",
        "save_failed": "\n⚠️ Save failed: {}",
        "calculation_complete": "\n🎉 Calculation complete!",
        "final_stats": "📊 Final Statistics:",
        "processed_evens": "  Processed even numbers: {}",
        "total_partitions": "  Total partitions: {}",
        "nonzero_evens": "  Even numbers with partitions: {}",
        "avg_partitions": "  Average partitions: {:.2f}",
        "min_partitions": "  Minimum partitions: {}",
        "max_partitions": "  Maximum partitions: {}",
        "total_time": "  Total time: {}",
        "time_analysis": "\n⏱️  Detailed Time Analysis:",
        "blocks_processed": "  Blocks processed: {}",
        "avg_block_time": "  Average block time: {}",
        "fastest_block": "  Fastest block: {}",
        "slowest_block": "  Slowest block: {}",
        "block_efficiency": "  Block efficiency: {:.2f} blocks/hour",
        "avg_nonzero": "  Average partitions (nonzero): {:.2f}",
        "progress_batch": "\r      🔄 Block progress: {:.1f}% | Batch: {}/{} ({:.1f}%) | Elapsed: {} | ETA: {}",
        "progress_block": "\r📊 Overall progress: {:.1f}% ({}/{}) | Block {} running: Elapsed {}, ETA {}",
        "calculating": "Calculating...",
        "plan_ranges": "📊 Planning to calculate {} ranges:",
        "range_info": "  Range {}: S0={} → S2={}",
        "actual_range": "         Actual even range: {} to {} (total {})",
        "current_config": "⚙️  Current Configuration:",
        "start_range": "\n🚀 Starting calculation for range {}/{}",
        "current_params": "📊 Current Parameters:",
        "s0_param": "  Start index S0 = {}",
        "s2_param": "  End index S2 = {}",
        "actual_even_range": "  Actual even range: {} to {}",
        "calculation_count": "  Calculation count: {} consecutive even numbers",
        "range_success": "\n✅ Range {} calculation successful!",
        "range_failed": "\n❌ Range {} calculation failed: {}",
        "continue_next": "⚠️  Continuing to next range...",
        "all_complete": "\n🎉 All ranges calculation complete!",
    }
}


def msg(key, *args):
    """
    获取当前语言的消息
    Get message in current language
    
    Args:
        key: 消息键 | Message key
        *args: 格式化参数 | Formatting arguments
    
    Returns:
        格式化的消息字符串 | Formatted message string
    """
    text = MESSAGES[LANGUAGE].get(key, key)
    if args:
        return text.format(*args)
    return text


# ============================================================================
# 辅助工具函数 | Utility Functions
# ============================================================================

def format_time(seconds):
    """
    格式化时间显示
    Format time display

    Args:
        seconds: 秒数 | Seconds

    Returns:
        格式化的时间字符串（如 "1小时23分45秒"）
        Formatted time string (e.g., "1 hour 23 min 45 sec")
    """
    if seconds < 60:
        return f"{seconds:.0f}秒" if LANGUAGE == "zh" else f"{seconds:.0f} sec"
    elif seconds < 3600:
        minutes = seconds // 60
        secs = seconds % 60
        if LANGUAGE == "zh":
            return f"{minutes:.0f}分{secs:.0f}秒"
        else:
            return f"{minutes:.0f} min {secs:.0f} sec"
    else:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        if LANGUAGE == "zh":
            return f"{hours:.0f}小时{minutes:.0f}分"
        else:
            return f"{hours:.0f} hour {minutes:.0f} min"


@njit(inline='always')
def binary_search_right(arr, target):
    """
    二分查找：返回 arr 中 <= target 的元素个数
    Binary search: return count of elements <= target in arr

    Args:
        arr: 已排序的数组 | Sorted array
        target: 目标值 | Target value

    Returns:
        arr 中 <= target 的元素个数
        Count of elements <= target in arr

    Example:
        >>> arr = np.array([3, 5, 7, 11, 13])
        >>> binary_search_right(arr, 10)
        3  # [3, 5, 7] 三个元素 <= 10 | three elements <= 10
    """
    left, right = 0, len(arr)
    while left < right:
        mid = (left + right) // 2
        if arr[mid] <= target:
            left = mid + 1
        else:
            right = mid
    return left


# ============================================================================
# L1 层：基础素数生成 | L1 Layer: Base Prime Generation
# ============================================================================

def generate_base_primes(limit=None):
    """
    生成 L1 层基础素数（埃拉托斯特尼筛法）
    Generate L1 base primes (Sieve of Eratosthenes)

    Args:
        limit: 生成素数的上限（默认使用配置中的值）
               Prime generation limit (default: use Config value)

    Returns:
        基础奇素数数组（不含2）
        Base odd primes array (excluding 2)

    Note:
        基础素数用于 L2 层的素数筛选
        Base primes are used for L2 prime sieving
    """
    if limit is None:
        limit = Config.BASE_PRIMES_LIMIT

    print(f"{msg('generate_base_primes')} {limit:,}...")

    # 埃拉托斯特尼筛法 | Sieve of Eratosthenes
    is_prime = np.ones(limit + 1, dtype=bool)
    is_prime[0] = is_prime[1] = False

    for i in range(2, int(limit ** 0.5) + 1):
        if is_prime[i]:
            is_prime[i * i::i] = False

    primes = np.where(is_prime)[0]
    odd_primes = primes[primes > 2]  # 排除2，只保留奇素数 | Exclude 2, keep odd primes only

    print(msg('base_primes_complete', len(odd_primes)))
    return odd_primes


# ============================================================================
# L2 层：分块并行素数筛选 | L2 Layer: Parallel Block Prime Sieving
# ============================================================================

@njit(parallel=True, fastmath=True, nogil=True, cache=True)
def sieve_block(start_idx, end_idx, base_primes):
    """
    分块筛选素数（核心算法 - JIT编译加速）
    Block prime sieving (core algorithm - JIT compiled)

    Args:
        start_idx: 起始索引（奇数索引）| Start index (odd index)
        end_idx: 结束索引（奇数索引）| End index (odd index)
        base_primes: L1层基础素数数组 | L1 base primes array

    Returns:
        该块内的素数索引数组
        Prime index array in this block

    Algorithm:
        1. 将索引范围分成若干小块（chunk）
           Divide index range into small chunks
        2. 并行处理每个小块：用基础素数筛除合数
           Process each chunk in parallel: sieve composites using base primes
        3. 提取素数索引
           Extract prime indices
    """
    array_len = end_idx - start_idx + 1
    is_composite = np.zeros(array_len, dtype=np.bool_)  # False=素数 | prime，True=合数 | composite

    # 自适应分块大小（使用全局常量）
    # Adaptive chunk size (using global constants)
    if start_idx < SIEVE_THRESHOLD:
        chunk_size = SIEVE_CHUNK_SIZE_SMALL
    else:
        chunk_size = SIEVE_CHUNK_SIZE_LARGE

    num_chunks = (array_len + chunk_size - 1) // chunk_size

    # 并行筛选每个小块 | Sieve each chunk in parallel
    for chunk_id in prange(num_chunks):
        chunk_start = chunk_id * chunk_size
        chunk_end = min(chunk_start + chunk_size, array_len)

        abs_start_idx = start_idx + chunk_start
        start_odd = 2 * abs_start_idx + 3
        end_odd = 2 * (start_idx + chunk_end - 1) + 3

        sqrt_end = int(np.sqrt(float(end_odd)))
        num_base_primes = binary_search_right(base_primes, sqrt_end)

        # 用基础素数筛除合数 | Sieve composites using base primes
        for i in range(num_base_primes):
            p = base_primes[i]
            p_squared = p * p

            # 计算第一个需要筛除的奇数
            # Calculate first odd number to sieve
            if p_squared >= start_odd:
                first_odd = p_squared
            else:
                quotient = (start_odd + p - 1) // p
                if quotient % 2 == 0:
                    quotient += 1
                first_odd = quotient * p

            if first_odd > end_odd:
                continue

            first_idx = (first_odd - start_odd) // 2 + chunk_start

            if first_idx >= chunk_end:
                continue

            # 标记合数 | Mark composites
            for idx in range(first_idx, chunk_end, p):
                is_composite[idx] = True

    # ========== 提取素数索引 | Extract prime indices ==========
    num_threads = NUM_EXTRACT_THREADS
    chunk_size_extract = (array_len + num_threads - 1) // num_threads
    counts = np.zeros(num_threads, dtype=np.int64)

    # 统计每个线程块的素数个数
    # Count primes in each thread chunk
    for t in prange(num_threads):
        chunk_start = t * chunk_size_extract
        chunk_end = min((t + 1) * chunk_size_extract, array_len)
        count = 0
        for i in range(chunk_start, chunk_end):
            if not is_composite[i]:
                count += 1
        counts[t] = count

    total_primes = np.sum(counts)

    # 计算每个线程的写入偏移
    # Calculate write offset for each thread
    offsets = np.zeros(num_threads, dtype=np.int64)
    for t in range(1, num_threads):
        offsets[t] = offsets[t - 1] + counts[t - 1]

    prime_indices = np.empty(total_primes, dtype=np.int64)

    # 并行提取素数索引 | Extract prime indices in parallel
    for t in prange(num_threads):
        chunk_start = t * chunk_size_extract
        chunk_end = min((t + 1) * chunk_size_extract, array_len)
        write_idx = offsets[t]

        for i in range(chunk_start, chunk_end):
            if not is_composite[i]:
                prime_indices[write_idx] = start_idx + i
                write_idx += 1

    return prime_indices


def sieve_prime_indices(start_idx, end_idx, base_primes):
    """
    筛选指定索引范围内的素数（高层API）
    Sieve primes in specified index range (high-level API)

    Args:
        start_idx: 起始索引 | Start index
        end_idx: 结束索引 | End index
        base_primes: 基础素数数组 | Base primes array

    Returns:
        素数索引数组 | Prime index array
    """
    if end_idx < start_idx:
        return np.array([], dtype=np.int64)

    print(msg('sieve_start'), end='', flush=True)
    prime_indices = sieve_block(start_idx, end_idx, base_primes)

    return prime_indices


# ============================================================================
# 分拆数计算核心 | Core Partition Number Calculation
# ============================================================================

@njit(parallel=True)
def compute_partition_parallel(s0, s2, nxx_i_batch, nxx_j_batch, ijs_offset, progress_array):
    """
    并行计算哥德巴赫分拆数（核心算法 - JIT编译优化）
    Parallel Goldbach partition number calculation (core algorithm - JIT optimized)

    参数说明 | Parameter Description
    --------
    s0 : int
        起始索引（不包含）| Start index (exclusive)
        实际起始偶数 = 2×(s0+1) | Actual starting even = 2×(s0+1)

    s2 : int
        结束索引（包含）| End index (inclusive)
        实际结束偶数 = 2×s2 | Actual ending even = 2×s2

    nxx_i_batch : ndarray
        前半区奇素数的索引数组 | Frontend odd prime indices
        素数计算公式 | Prime formula: p = 2×nxx_i_batch[k] + 3
        示例 | Example: [0,1,2,3,...] 对应素数 | corresponds to primes [3,5,7,9,...]

    nxx_j_batch : ndarray
        后半区奇素数的索引数组 | Backend odd prime indices
        素数计算公式 | Prime formula: q = 2×nxx_j_batch[k] + 3

    ijs_offset : int
        前后半区分界偏移量 | Frontend-backend boundary offset

        作用 | Purpose: 确保配对 (p,q) 满足 p ≤ q，避免重复计数
                        Ensure pairs (p,q) satisfy p ≤ q to avoid double counting

        原理 | Principle:
        - 对于偶数 2n = p + q，要求 p ≤ q | For even 2n = p + q, require p ≤ q
        - 等价于 p ≤ n ≤ q | Equivalent to p ≤ n ≤ q
        - ijs_offset 标记满足 p ≈ n 的索引位置 | marks index position where p ≈ n
        - 当 nxx_i_batch[i] > ijs_offset 时，对应的 p > n
          When nxx_i_batch[i] > ijs_offset, corresponding p > n
          此时必有 q < n < p，应跳过以避免重复
          Then q < n < p, should skip to avoid duplication

        示例 | Example:
        计算 g(100) = 偶数100的分拆数 | Calculate g(100) = partitions of 100
        - 配对 | Pair (3,97): p=3 < 50, q=97 > 50  ✅ 计数 | count
        - 配对 | Pair (47,53): p=47 < 50, q=53 > 50  ✅ 计数 | count
        - 配对 | Pair (53,47): p=53 > 50, q=47 < 50  ❌ 跳过（重复）| skip (duplicate)

    progress_array : ndarray
        进度监控数组，用于实时显示计算进度
        Progress monitoring array for real-time display

    返回值 | Returns
    ------
    partitions : ndarray
        分拆数数组，长度为 s2-s0 | Partition array, length = s2-s0
        partitions[k] = g(2×(s0+1+k))

        索引映射 | Index mapping:
        - partitions[0] → g(2×(s0+1))
        - partitions[i] → g(2×(s0+1+i))
        - partitions[s2-s0-1] → g(2×s2)

    算法原理 | Algorithm Principle
    --------
    双指针流式配对算法 | Two-pointer streaming pairing algorithm:

    目标 | Goal: 对每个偶数 2n，计算 | For each even 2n, compute
          g(2n) = |{(p,q): p≤q, p+q=2n, p,q是素数}|
                  |{(p,q): p≤q, p+q=2n, p,q are primes}|

    步骤 | Steps:
    1. 并行处理 | Parallel processing: 将前半区素数分成多个批次，每个线程处理一部分
                                      Divide frontend primes into batches, each thread processes a portion

    2. 配对搜索 | Pair search: 对前半区素数 p = 2i+3，在后半区找 q = 2j+3，满足
                               For frontend prime p = 2i+3, find q = 2j+3 in backend, satisfying:
       p + q = 2n 且 | and p ≤ q
       即 | i.e.: (2i+3) + (2j+3) = 2n
       简化 | Simplify: i + j = n - 3

    3. 去重机制 | Deduplication:
       - 仅计数 p ≤ q 的配对 | Only count pairs where p ≤ q
       - 通过 ijs_offset 判断何时停止搜索 | Use ijs_offset to determine when to stop
       - 保证每对素数只被计数一次 | Ensure each pair is counted once

    4. 单调性优化 | Monotonicity optimization:
       - 固定 n 时，i↑ 则 j↓（双指针技巧）| For fixed n, i↑ then j↓ (two-pointer trick)
       - 扫描所有 n 时，总复杂度 O(π(2n)) | Scanning all n, total complexity O(π(2n))

    5. 特殊处理 | Special handling:
       - 素数 2 的配对单独处理（检查 2n-2 是否为素数）
         Pairs with prime 2 handled separately (check if 2n-2 is prime)

    时间复杂度 | Time complexity: O(π(2s2) / num_threads)
    空间复杂度 | Space complexity: O(s2 - s0)
    """
    w = (s2 - 3) // 2
    ki_end = np.int64(np.searchsorted(nxx_i_batch, w, side='right') - 1)

    num_groups = NUM_GROUPS  # 使用全局常量 | Use global constant
    group_size = (ki_end + 1 + num_groups - 1) // num_groups

    # 每组维护自己的搜索起点（利用单调性）
    # Each group maintains its own search start position (leveraging monotonicity)
    group_kj_start = np.zeros(num_groups, dtype=np.int64)
    group_kj_end = np.zeros(num_groups, dtype=np.int64)

    shape = s2 - s0
    group_counts = np.zeros((num_groups, shape), dtype=np.int64)

    # 并行处理每组 | Process each group in parallel
    for group_id in prange(num_groups):
        start_i = group_id * group_size
        end_i = min(start_i + group_size, ki_end + 1)

        for i in range(start_i, end_i):
            # 计算当前i对应的搜索范围
            # Calculate search range for current i
            w_min = s0 + 1 - nxx_i_batch[i] - 3

            # 确定后半区搜索起点（利用单调性）
            # Determine backend search start (leveraging monotonicity)
            if w_min < nxx_i_batch[i]:
                kj_start = i - ijs_offset
            else:
                if i == start_i:
                    kj_start = np.searchsorted(nxx_j_batch, w_min, side='right') - 1
                    if kj_start < len(nxx_j_batch) and nxx_j_batch[kj_start] < w_min:
                        kj_start += 1
                else:
                    current_kj_start = group_kj_start[group_id]
                    while current_kj_start > 0 and nxx_j_batch[current_kj_start - 1] >= w_min:
                        current_kj_start -= 1
                    kj_start = current_kj_start

            # 确定后半区搜索终点
            # Determine backend search end
            w_max = s2 - nxx_i_batch[i] - 3
            if i == start_i:
                kj_end = np.int64(np.searchsorted(nxx_j_batch, w_max, side='right') - 1)
            else:
                current_kj_end = group_kj_end[group_id]
                while current_kj_end >= 0 and nxx_j_batch[current_kj_end] > w_max:
                    current_kj_end -= 1
                kj_end = current_kj_end

            # 更新组内搜索位置 | Update in-group search position
            group_kj_start[group_id] = kj_start
            group_kj_end[group_id] = kj_end

            # 统计配对数 | Count pairs
            if kj_end >= kj_start:
                nxx_i_val = nxx_i_batch[i] + 3 - (s0 + 1)

                for kj in range(kj_start, kj_end + 1):
                    idx = nxx_i_val + nxx_j_batch[kj]

                    if 0 <= idx < shape:
                        group_counts[group_id][idx] += 1

            # 定期更新进度（使用全局常量）
            # Periodically update progress (using global constant)
            if (i - start_i) % BATCH_REPORT_FREQUENCY == 0:
                progress_array[group_id] = i - start_i

    return np.sum(group_counts, axis=0)


# ============================================================================
# 进度监控 | Progress Monitoring
# ============================================================================

def calculate_stable_eta(total_current_progress, total_elapsed_time, total_block_work):
    """
    计算稳定的剩余时间估算
    Calculate stable ETA (Estimated Time to Arrival)

    Args:
        total_current_progress: 当前总进度 | Current total progress
        total_elapsed_time: 已用总时间 | Total elapsed time
        total_block_work: 总工作量 | Total work

    Returns:
        格式化的剩余时间字符串 | Formatted remaining time string
    """
    if total_current_progress <= 0:
        return msg('calculating')

    progress_rate = total_current_progress / total_elapsed_time
    remaining_work = total_block_work - total_current_progress

    if progress_rate > 0:
        estimated_remaining_time = remaining_work / progress_rate
        return format_time(max(0, estimated_remaining_time))
    else:
        return msg('calculating')


def monitor_batch_progress(progress_array, total_work_per_group, num_groups, start_time,
                           current_batch, total_batches, previous_batches_time):
    """
    批次级进度监控（线程函数）
    Batch-level progress monitoring (thread function)

    Args:
        progress_array: 进度数组 | Progress array
        total_work_per_group: 每组的总工作量 | Total work per group
        num_groups: 组数 | Number of groups
        start_time: 批次开始时间 | Batch start time
        current_batch: 当前批次号 | Current batch number
        total_batches: 总批次数 | Total batches
        previous_batches_time: 前面批次累计时间 | Previous batches cumulative time
    """
    single_batch_work = total_work_per_group * num_groups
    total_block_work = single_batch_work * total_batches

    while True:
        current_time = time.time()
        elapsed_time = current_time - start_time

        # 当前批次进度 | Current batch progress
        current_batch_progress = np.sum(progress_array)
        batch_progress = min(current_batch_progress / single_batch_work * 100, 100)

        # 整个块的总进度 | Total block progress
        completed_batches_work = (current_batch - 1) * single_batch_work
        total_current_progress = completed_batches_work + current_batch_progress
        block_progress = min(total_current_progress / total_block_work * 100, 100)

        # 计算ETA | Calculate ETA
        total_elapsed_time = previous_batches_time + elapsed_time

        if total_elapsed_time >= Config.ETA_STABLE_THRESHOLD:
            eta_str = calculate_stable_eta(total_current_progress, total_elapsed_time, total_block_work)
        else:
            if batch_progress > 1:
                estimated_batch_time = elapsed_time / (batch_progress / 100)
                batch_remaining_time = estimated_batch_time - elapsed_time

                if total_batches > 1:
                    estimated_total_block_time = estimated_batch_time * total_batches
                    already_completed_time = estimated_batch_time * (current_batch - 1)
                    block_remaining_time = estimated_total_block_time - already_completed_time - elapsed_time
                else:
                    block_remaining_time = batch_remaining_time

                eta_str = format_time(max(0, block_remaining_time))
            else:
                eta_str = msg('calculating')

        elapsed_str = format_time(total_elapsed_time)

        print(msg('progress_batch', block_progress, current_batch, total_batches, 
                  batch_progress, elapsed_str, eta_str), end='', flush=True)

        if batch_progress >= 99:
            break

        time.sleep(Config.BATCH_PROGRESS_INTERVAL)


def monitor_block_progress(block_num, block_start_time, block_times, max_block,
                           completed_blocks, stop_event):
    """
    块级进度监控（线程函数）
    Block-level progress monitoring (thread function)

    Args:
        block_num: 当前块号 | Current block number
        block_start_time: 块开始时间 | Block start time
        block_times: 历史块用时列表 | Historical block time list
        max_block: 最大块号 | Maximum block number
        completed_blocks: 已完成块数 | Completed blocks
        stop_event: 停止事件 | Stop event
    """
    while not stop_event.is_set():
        current_time = time.time()
        elapsed_time = current_time - block_start_time

        overall_progress = (completed_blocks / max_block) * 100

        if len(block_times) > 0:
            avg_time = np.mean(block_times)
            remaining_time = max(0, avg_time - elapsed_time)

            elapsed_str = format_time(elapsed_time)
            eta_str = format_time(remaining_time)

            print(msg('progress_block', overall_progress, completed_blocks, max_block,
                      block_num, elapsed_str, eta_str), end='', flush=True)
        else:
            elapsed_str = format_time(elapsed_time)
            print(msg('progress_block', overall_progress, completed_blocks, max_block,
                      block_num, elapsed_str, msg('calculating')), end='', flush=True)

        if stop_event.wait(Config.PROGRESS_UPDATE_INTERVAL):
            break


# ============================================================================
# 分拆数计算管理 | Partition Number Calculation Management
# ============================================================================

def calculate_single_batch(s0, s2, nxx_i_batch, nxx_j_batch, ijs_offset,
                           current_batch, total_batches, previous_batches_time):
    """
    计算单个批次的分拆数
    Calculate partition numbers for a single batch

    Args:
        s0: 起始偶数 | Starting even number
        s2: 结束偶数 | Ending even number
        nxx_i_batch: 前半区素数索引 | Frontend prime indices
        nxx_j_batch: 后半区素数索引 | Backend prime indices
        ijs_offset: 重叠跳过偏移量 | Overlap skip offset
        current_batch: 当前批次号 | Current batch number
        total_batches: 总批次数 | Total batches
        previous_batches_time: 前面批次累计时间 | Previous batches cumulative time

    Returns:
        (批次结果数组, 批次用时) | (Batch result array, batch time)
    """
    w = (s2 - 3) // 2
    ki_end = np.searchsorted(nxx_i_batch, w, side='right') - 1
    num_groups = Config.NUM_GROUPS
    total_work_per_group = (ki_end + 1 + num_groups - 1) // num_groups

    progress_array = np.zeros(num_groups, dtype=np.int64)
    start_time = time.time()

    # 启动进度监控线程 | Start progress monitoring thread
    progress_thread = threading.Thread(
        target=monitor_batch_progress,
        args=(progress_array, total_work_per_group, num_groups, start_time,
              current_batch, total_batches, previous_batches_time),
        daemon=True
    )
    progress_thread.start()

    # 执行计算 | Execute calculation
    batch_result = compute_partition_parallel(
        s0, s2, nxx_i_batch, nxx_j_batch, ijs_offset, progress_array
    )

    end_time = time.time()
    batch_time = end_time - start_time

    return batch_result, batch_time


def calculate_block_partitions(total_s0, total_s2, nxx_i, nxx_j, ijs_offset):
    """
    计算整个块的分拆数（分批次处理）
    Calculate partition numbers for entire block (batch processing)

    Args:
        total_s0: 块起始偶数 | Block starting even number
        total_s2: 块结束偶数 | Block ending even number
        nxx_i: 前半区素数索引 | Frontend prime indices
        nxx_j: 后半区素数索引 | Backend prime indices
        ijs_offset: 重叠跳过偏移量 | Overlap skip offset

    Returns:
        块内分拆数数组 | Partition array within block
    """
    total_range = total_s2 - total_s0
    block_result = np.zeros(total_range, dtype=np.int64)

    batch_size = Config.BATCH_SIZE
    num_batches = (total_range + batch_size - 1) // batch_size

    cumulative_batch_time = 0

    for batch_idx in range(num_batches):
        batch_s0 = total_s0 + batch_idx * batch_size
        batch_s2 = min(batch_s0 + batch_size, total_s2)

        try:
            batch_result, batch_time = calculate_single_batch(
                batch_s0, batch_s2, nxx_i, nxx_j, ijs_offset,
                current_batch=batch_idx + 1,
                total_batches=num_batches,
                previous_batches_time=cumulative_batch_time
            )

            cumulative_batch_time += batch_time

            # 合并结果 | Merge results
            global_start_idx = batch_s0 - total_s0
            global_end_idx = global_start_idx + len(batch_result)
            block_result[global_start_idx:global_end_idx] = batch_result

            del batch_result
            gc.collect()

        except Exception as e:
            print(f"\n❌ {msg('range_failed', batch_idx + 1, e)}")
            continue

    return block_result


# ============================================================================
# 主计算函数 | Main Calculation Function
# ============================================================================

def goldbach_partition_count(s0, s2, output_file=None):
    """
    计算哥德巴赫分拆数
    Calculate Goldbach partition numbers

    参数说明 | Parameter Description:
    --------
    s0 : int
        起始索引（不包含）| Start index (exclusive)
        实际起始偶数 = 2×(s0+1) | Actual starting even = 2×(s0+1)

    s2 : int
        结束索引（包含）| End index (inclusive)
        实际结束偶数 = 2×s2 | Actual ending even = 2×s2

    实际计算范围 | Actual calculation range: [2×(s0+1), 2×s2]

    示例 | Examples:
    ----
    goldbach_partition_count(0, 100)
    # 计算偶数 2 到 200 的分拆数
    # Calculate partitions for even numbers 2 to 200
    # 实际范围 | Actual range: [2×(0+1), 2×100] = [2, 200]

    goldbach_partition_count(24999900000, 25000000000)
    # 计算偶数 49999800002 到 50000000000
    # Calculate partitions for even numbers 49999800002 to 50000000000
    # 实际范围 | Actual range: [2×(24999900000+1), 2×25000000000]
    """
    print(msg('start_calculation'))
    print(f"  S0={s0:,}, S2={s2:,}")
    print("=" * 70)

    total_program_start = time.time()
    block_times = []

    # ========== 步骤1：生成基础素数 | Step 1: Generate base primes ==========
    print(msg('step1'))
    stage1_start = time.time()
    base_primes = generate_base_primes()
    stage1_time = time.time() - stage1_start
    print(msg('step1_complete', format_time(stage1_time)))

    # ========== 步骤2：计算全局参数 | Step 2: Calculate global parameters ==========
    print(msg('step2'))
    ii_max = (s2 - 3) // 2
    jj_min = (s0 - 3) // 2

    n_array = np.arange(s0 + 1, s2 + 1, dtype=np.int64)
    if s0 == 0:
        jj_min = 0
        #n_array[0] = 3
        #n_array[1] = 3

    print(msg('target_range', len(n_array), n_array[0], n_array[-1]))
    print(msg('frontend_max', ii_max))
    print(msg('backend_min', jj_min))

    # ========== 步骤3：计算处理范围 | Step 3: Calculate processing range ==========
    print(msg('step3'))
    block_size = Config.BLOCK_SIZE
    effective_range = s2 // 2
    max_block = (effective_range + block_size - 1) // block_size
    print(msg('block_estimate', max_block))

    complete_partition_counts = np.zeros(len(n_array), dtype=np.int64)
    print(msg('init_array', len(complete_partition_counts)))

    completed_blocks = 0

    # ========== 步骤4：逐块处理 | Step 4: Process block by block ==========
    for block_num in range(1, max_block + 1):
        block_start_time = time.time()

        # 计算当前块索引范围 | Calculate current block index range
        i_min = max((block_num - 1) * block_size - 1, 0)
        i_max_raw = block_num * block_size - 2

        is_final_block = (block_num == max_block)
        if is_final_block:
            i_max_raw = ii_max

        # 筛选前半区素数 | Sieve frontend primes
        print(f"\n{msg('block_frontend_sieve', block_num)}", end='', flush=True)
        sieve_start = time.time()
        nxx_i = sieve_prime_indices(i_min, i_max_raw, base_primes)
        sieve_time = time.time() - sieve_start

        if nxx_i is None or len(nxx_i) == 0:
            print(msg('no_primes'))
            continue

        i_min, i_max = nxx_i[0], nxx_i[-1]
        print(msg('frontend_complete', sieve_time, i_min, i_max))

        # 计算后半区范围 | Calculate backend range
        j_min = min(n_array) - i_max - 3
        j_max = max(n_array) - i_min - 3
        if j_min < 0:
            j_min = 0

        if j_min < 0:
            continue

        # 筛选后半区素数 | Sieve backend primes
        print(f"{msg('block_backend_sieve', block_num)}", end='', flush=True)
        sieve_start = time.time()
        nxx_j = sieve_prime_indices(j_min, j_max, base_primes)
        sieve_time = time.time() - sieve_start

        if nxx_j is None or len(nxx_j) == 0:
            print(msg('no_primes'))
            continue

        print(msg('backend_complete', sieve_time, j_min, j_max))

        # 计算重叠跳过数 | Calculate overlap skip offset
        if nxx_j[0] < nxx_i[-1]:
            ijs_offset = len(nxx_i) - np.searchsorted(nxx_j, nxx_i[-1], side='right')
        else:
            ijs_offset = 0

        # 启动块级进度监控 | Start block-level progress monitoring
        stop_event = threading.Event()
        progress_thread = threading.Thread(
            target=monitor_block_progress,
            args=(block_num, block_start_time, block_times, max_block, completed_blocks, stop_event),
            daemon=True
        )
        progress_thread.start()

        # 计算当前块分拆数 | Calculate current block partitions
        block_partition_counts = calculate_block_partitions(s0, s2, nxx_i, nxx_j, ijs_offset)

        # 停止进度监控 | Stop progress monitoring
        stop_event.set()
        progress_thread.join(timeout=1)

        block_end_time = time.time()
        block_time = block_end_time - block_start_time
        block_times.append(block_time)
        completed_blocks += 1

        # 累加结果 | Accumulate results
        complete_partition_counts += block_partition_counts

        print(msg('block_complete', block_num, format_time(block_time)))

        # 清理内存 | Clean up memory
        del nxx_i, nxx_j, block_partition_counts
        gc.collect()

        if is_final_block:
            break

    # ========== 特殊处理 | Special handling ==========
    if s0 == 0:
        complete_partition_counts[1] = 1

    # ========== 保存结果 | Save results ==========
    if output_file is None:
        output_file = f'{Config.DEFAULT_OUTPUT_DIR}/{Config.OUTPUT_FILE_PREFIX}_{s0}_{s2}.npy'

    try:
        # 确保输出目录存在 | Ensure output directory exists
        output_dir = os.path.dirname(output_file)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

        np.save(output_file, complete_partition_counts)
        print(msg('save_result', output_file))
    except Exception as e:
        print(msg('save_failed', e))

    # ========== 最终统计 | Final statistics ==========
    total_partitions = np.sum(complete_partition_counts)
    nonzero_evens = np.count_nonzero(complete_partition_counts)
    total_program_end = time.time()
    total_execution_time = total_program_end - total_program_start

    print(msg('calculation_complete'))
    print("=" * 70)
    print(msg('final_stats'))
    print(msg('processed_evens', len(complete_partition_counts)))
    print(msg('total_partitions', total_partitions))
    print(msg('nonzero_evens', nonzero_evens))
    print(msg('avg_partitions', total_partitions / len(complete_partition_counts)))
    print(msg('min_partitions', np.min(complete_partition_counts)))
    print(msg('max_partitions', np.max(complete_partition_counts)))
    print(msg('total_time', format_time(total_execution_time)))

    if block_times:
        print(msg('time_analysis'))
        print(msg('blocks_processed', len(block_times)))
        print(msg('avg_block_time', format_time(np.mean(block_times))))
        print(msg('fastest_block', format_time(np.min(block_times))))
        print(msg('slowest_block', format_time(np.max(block_times))))
        print(msg('block_efficiency', len(block_times) / (total_execution_time / 3600)))

    if nonzero_evens > 0:
        print(msg('avg_nonzero', total_partitions / nonzero_evens))

    return complete_partition_counts


# ============================================================================
# 主程序入口 | Main Program Entry
# ============================================================================

if __name__ == "__main__":
    print("🎯 哥德巴赫分拆数计算程序 | Goldbach Partition Counter" if LANGUAGE == "zh" 
          else "🎯 Goldbach Partition Counter")
    print("=" * 70)

    # ========================================================================
    # 计算任务配置区 | Calculation Task Configuration
    # ========================================================================

    # 定义计算区间（根据硬件配置选择合适的规模）
    # Define calculation ranges (choose appropriate scale based on hardware)

    # 示例1：小规模测试（适合所有配置）
    # Example 1: Small-scale testing (suitable for all configurations)
    # calculation_ranges = [(0, 1000000)]  # 计算 2 到 200万 | Calculate 2 to 2 million

    # 示例2：中等规模（适合 8GB+ 内存）
    # Example 2: Medium-scale (suitable for 8GB+ RAM)
    # calculation_ranges = [(0, 5000000)]  # 计算 2 到 1000万 | Calculate 2 to 10 million

    # 示例3：大规模计算（适合 16GB+ 内存）
    # Example 3: Large-scale (suitable for 16GB+ RAM)
    calculation_ranges = [

        (0, 5000000),
        #(499900000,500000000),
        #(4999900000,5000000000),
        #(49999900000,50000000000),
    ]

    # 示例4：分段计算（推荐策略）
    # Example 4: Segmented calculation (recommended strategy)
    # calculation_ranges = [
    #     (0, 1000000000),           # 第1段 | Segment 1
    #     (1000000000, 2000000000),  # 第2段 | Segment 2
    #     (2000000000, 3000000000),  # 第3段 | Segment 3
    # ]

    print(msg('plan_ranges', len(calculation_ranges)))
    for i, (s0, s2) in enumerate(calculation_ranges, 1):
        actual_start = 2 * (s0 + 1)
        actual_end = 2 * s2
        range_size = s2 - s0
        print(msg('range_info', i, s0, s2))
        print(msg('actual_range', actual_start, actual_end, range_size))
    print()

    # 显示当前配置 | Display current configuration
    print(msg('current_config'))
    print(f"  BLOCK_SIZE = {Config.BLOCK_SIZE:,}")
    print(f"  BATCH_SIZE = {Config.BATCH_SIZE:,}")
    print(f"  NUM_GROUPS = {Config.NUM_GROUPS}")
    print(f"  NUM_EXTRACT_THREADS = {Config.NUM_EXTRACT_THREADS}")
    print()

    # 依次执行每个区间 | Execute each range sequentially
    for i, (s0, s2) in enumerate(calculation_ranges, 1):
        print(msg('start_range', i, len(calculation_ranges)))
        print(msg('current_params'))
        print(msg('s0_param', s0))
        print(msg('s2_param', s2))
        print(msg('actual_even_range', 2*(s0+1), 2*s2))
        print(msg('calculation_count', s2 - s0))

        try:
            result = goldbach_partition_count(
                s0=s0,
                s2=s2,
                output_file=f"results/goldbach_partition_counts_{s0}_{s2}.npy"
            )

            print(msg('range_success', i))

        except Exception as e:
            print(msg('range_failed', i, e))
            import traceback
            traceback.print_exc()
            print(msg('continue_next'))
            continue

    print(msg('all_complete'))