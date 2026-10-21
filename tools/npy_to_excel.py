"""
Goldbach Partition Excel Exporter - 哥德巴赫分拆数据 Excel 导出工具
======================================================================

功能：将计算好的分拆数据导出到格式化的 Excel 表格

特点：
  - 双语支持（中文/English）
  - 自动创建新工作簿
  - 美观的表格样式
  - 批量设置格式（超快速！）
  - 自动列宽调整
  - 智能命名保存
  - 支持超大数据集（优化内存使用）

作者：赵时建（极速优化版）
版本：3.2
日期：2026-10-16
======================================================================
"""

import numpy as np
import time
from datetime import datetime
import xlwings as xw
from pathlib import Path
import os


# ========================================================================
# 语言配置：修改此变量切换语言
# Language Configuration: Change this variable to switch language
# ========================================================================
LANGUAGE = 'english'  # 'chinese' 或 'english'


# ========================================================================
# 双语文本配置
# Bilingual Text Configuration
# ========================================================================
TEXT = {
    'chinese': {
        'title': '📊 哥德巴赫分拆数据 Excel 导出工具',
        'version': 'v3.2 (极速版)',
        'step1': '📂 步骤1: 加载数据文件...',
        'loading': '   正在加载',
        'load_success': '   ✅ 加载成功！数据长度',
        'file_not_found': '❌ 错误：文件',
        'not_exist': '不存在！',
        'step2': '🔄 步骤2: 构建二维数据表...',
        'data_range': '   数据范围',
        'total_data': '   总数据量',
        'table_layout': '   表格布局',
        'rows': '行',
        'cols': '列',
        'even_number': '个偶数',
        'table_build_done': '   ✅ 数据表构建完成，用时',
        'step3': '📝 步骤3: 创建 Excel 工作簿...',
        'excel_created': '   ✅ Excel 工作簿创建成功',
        'create_failed': '   ❌ 创建失败',
        'step4': '✍️  步骤4: 写入数据到 Excel...',
        'writing_rows': '   正在写入',
        'rows_data': '行数据...',
        'write_done': '   ✅ 数据写入完成，用时',
        'step5': '🎨 步骤5: 美化表格样式（批量优化）...',
        'setting_title': '   [1/6] 设置标题格式...',
        'setting_header': '   [2/6] 设置表头格式...',
        'setting_first_col': '   [3/6] 设置第一列格式...',
        'setting_data_area': '   [4/6] 设置数据区域格式...',
        'setting_col_width': '   [5/6] 批量调整列宽...',
        'freezing_panes': '   [6/6] 冻结窗格...',
        'format_done': '   ✅ 表格美化完成，用时',
        'format_partial_fail': '   ⚠️  格式设置部分失败',
        'step6': '💾 步骤6: 保存文件...',
        'file_saved': '   ✅ 文件已保存',
        'save_failed': '   ❌ 保存失败',
        'export_done': '🎉 导出完成!',
        'statistics': '📊 统计信息:',
        'data_count': '   数据量',
        'table_size': '   表格大小',
        'total_time': '   总用时',
        'data_loading': '     - 数据加载',
        'excel_writing': '     - Excel写入',
        'excel_formatting': '     - 格式美化',
        'save_location': '   保存位置',
        'batch_mode': '🚀 批量导出模式',
        'files_to_export': '共',
        'files': '个文件待导出',
        'processing': '正在处理第',
        'wait': '⏸️  等待 3 秒后继续...',
        'batch_done': '🎊 批量导出完成!',
        'export_results': '导出结果:',
        'success': '✅ 成功',
        'failed': '❌ 失败',
        'file': '      文件',
        'single_mode': '📌 单文件导出模式',
        'batch_export_mode': '📌 批量导出模式',
        'files_count': '   待处理文件数',
        'program_done': '✨ 程序执行完毕！',
        'sheet_name': '分拆数数据',
        'table_title': '哥德巴赫分拆数据表',
        'range_label': '数据范围: 偶数',
        'to': '到',
        'gen_time': '生成时间',
        'even_start': '偶数起始值',
        'seconds': '秒',
        'minutes': '分',
        'hours': '小时',
    },
    'english': {
        'title': '📊 Goldbach Partition Excel Exporter',
        'version': 'v3.2 (Turbo)',
        'step1': '📂 Step 1: Loading data file...',
        'loading': '   Loading',
        'load_success': '   ✅ Load successful! Data length',
        'file_not_found': '❌ Error: File',
        'not_exist': 'does not exist!',
        'step2': '🔄 Step 2: Building 2D data table...',
        'data_range': '   Data range',
        'total_data': '   Total data',
        'table_layout': '   Table layout',
        'rows': 'rows',
        'cols': 'cols',
        'even_number': 'even numbers',
        'table_build_done': '   ✅ Table built successfully, time used',
        'step3': '📝 Step 3: Creating Excel workbook...',
        'excel_created': '   ✅ Excel workbook created successfully',
        'create_failed': '   ❌ Creation failed',
        'step4': '✍️  Step 4: Writing data to Excel...',
        'writing_rows': '   Writing',
        'rows_data': 'rows of data...',
        'write_done': '   ✅ Data write completed, time used',
        'step5': '🎨 Step 5: Formatting table (Batch optimized)...',
        'setting_title': '   [1/6] Setting title format...',
        'setting_header': '   [2/6] Setting header format...',
        'setting_first_col': '   [3/6] Setting first column format...',
        'setting_data_area': '   [4/6] Setting data area format...',
        'setting_col_width': '   [5/6] Batch adjusting column widths...',
        'freezing_panes': '   [6/6] Freezing panes...',
        'format_done': '   ✅ Formatting completed, time used',
        'format_partial_fail': '   ⚠️  Formatting partially failed',
        'step6': '💾 Step 6: Saving file...',
        'file_saved': '   ✅ File saved',
        'save_failed': '   ❌ Save failed',
        'export_done': '🎉 Export completed!',
        'statistics': '📊 Statistics:',
        'data_count': '   Data count',
        'table_size': '   Table size',
        'total_time': '   Total time',
        'data_loading': '     - Data loading',
        'excel_writing': '     - Excel writing',
        'excel_formatting': '     - Formatting',
        'save_location': '   Save location',
        'batch_mode': '🚀 Batch Export Mode',
        'files_to_export': 'Total',
        'files': 'files to export',
        'processing': 'Processing',
        'wait': '⏸️  Waiting 3 seconds...',
        'batch_done': '🎊 Batch export completed!',
        'export_results': 'Export results:',
        'success': '✅ Success',
        'failed': '❌ Failed',
        'file': '      File',
        'single_mode': '📌 Single File Export Mode',
        'batch_export_mode': '📌 Batch Export Mode',
        'files_count': '   Files to process',
        'program_done': '✨ Program completed!',
        'sheet_name': 'Partition Data',
        'table_title': 'Goldbach Partition Data Table',
        'range_label': 'Data Range: Even numbers',
        'to': 'to',
        'gen_time': 'Generated',
        'even_start': 'Even Start Value',
        'seconds': 'sec',
        'minutes': 'min',
        'hours': 'hrs',
    }
}


def get_text(key):
    """获取当前语言的文本"""
    return TEXT[LANGUAGE].get(key, key)


def format_time_duration(seconds):
    """
    格式化时间长度（双语版）
    Format time duration (bilingual)

    Args:
        seconds: 秒数 / seconds

    Returns:
        格式化的时间字符串 / formatted time string
    """
    sec_text = get_text('seconds')
    min_text = get_text('minutes')
    hrs_text = get_text('hours')

    if seconds < 60:
        return f"{seconds:.2f} {sec_text}"
    elif seconds < 3600:
        minutes = seconds // 60
        secs = seconds % 60
        return f"{int(minutes)} {min_text} {secs:.1f} {sec_text}"
    else:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        return f"{int(hours)} {hrs_text} {int(minutes)} {min_text}"


def export_to_excel(s0, s2, npy_filename=None, rows=5000, cols=10000):
    """
    将分拆数据导出到 Excel（极速优化版）
    Export partition data to Excel (Turbo optimized)

    Args:
        s0: 起始索引 / start index
        s2: 结束索引 / end index
        npy_filename: NumPy 数据文件名（默认自动生成） / NumPy data file (auto-generated by default)
        rows: 导出的行数（默认5000行） / number of rows to export (default 5000)
        cols: 每行的列数（默认10000列） / number of columns per row (default 10000)

    Returns:
        保存的文件路径 / saved file path
    """
    print("=" * 70)
    print(get_text('title'))
    print("=" * 70)

    start_time = time.time()

    # ========== 步骤1：加载数据 / Step 1: Load Data ==========
    print(f"\n{get_text('step1')}")

    if npy_filename is None:
        npy_filename = f'../results/goldbach_partition_counts_{s0}_{s2}.npy'

    if not Path(npy_filename).exists():
        print(f"{get_text('file_not_found')} '{npy_filename}' {get_text('not_exist')}")
        return None

    print(f"{get_text('loading')}: {npy_filename}")
    xy = np.load(npy_filename)
    print(f"{get_text('load_success')}: {len(xy):,}")

    # ========== 步骤2：构建二维数据表 / Step 2: Build 2D Table ==========
    print(f"\n{get_text('step2')}")

    total_elements = s2 - s0
    actual_rows = (total_elements + cols - 1) // cols
    rows = min(rows, actual_rows)

    print(f"{get_text('data_range')}: S0={s0:,}, S2={s2:,}")
    print(f"{get_text('total_data')}: {total_elements:,} {get_text('even_number')}")
    print(f"{get_text('table_layout')}: {rows} {get_text('rows')} × {cols} {get_text('cols')}")

    # 创建表头行（列索引）
    header_row = [get_text('even_start')] + [2 * (j + 1) for j in range(cols)]

    # 创建数据表
    data_table = []

    for i in range(rows):
        row_data = [None] * (cols + 1)

        # 第一列：行起始偶数值（修正：减去2）
        # First column: row starting even value (fixed: subtract 2)
        row_start_even = 2 * (s0 + i * cols + 1) - 2
        row_data[0] = row_start_even

        # 后续列：分拆数
        for j in range(cols):
            array_index = i * cols + j
            if array_index < len(xy):
                row_data[j + 1] = int(xy[array_index])
            else:
                break

        data_table.append(row_data)

    del xy

    load_time = time.time() - start_time
    print(f"{get_text('table_build_done')}: {format_time_duration(load_time)}")

    # ========== 步骤3：创建 Excel 工作簿 / Step 3: Create Excel Workbook ==========
    print(f"\n{get_text('step3')}")

    try:
        app = xw.App(visible=True, add_book=True)
        wb = app.books.active
        sheet = wb.sheets[0]
        sheet.name = get_text('sheet_name')

        print(get_text('excel_created'))

    except Exception as e:
        print(f"{get_text('create_failed')}: {e}")
        return None

    # ========== 步骤4：写入数据 / Step 4: Write Data ==========
    print(f"\n{get_text('step4')}")

    write_start = time.time()

    # 写入标题信息
    sheet.range('A1').value = get_text('table_title')
    sheet.range('A2').value = f"{get_text('range_label')} {2*(s0+1):,} {get_text('to')} {2*s2:,}"
    sheet.range('A3').value = f"{get_text('gen_time')}: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

    # 写入表头
    sheet.range('A5').value = header_row

    # 写入数据表
    print(f"{get_text('writing_rows')} {len(data_table)} {get_text('rows_data')}")
    sheet.range('A6').value = data_table

    write_time = time.time() - write_start
    print(f"{get_text('write_done')}: {format_time_duration(write_time)}")

    # ========== 步骤5：设置格式（批量优化版）/ Step 5: Format Table (Batch Optimized) ==========
    print(f"\n{get_text('step5')}")

    format_start = time.time()

    try:
        # 计算区域范围
        data_start_row = 6
        data_end_row = 5 + rows
        last_col = cols + 1
        last_col_letter = xw.utils.col_name(last_col)

        # ========== [1/6] 标题格式 / Title Format ==========
        print(get_text('setting_title'))
        title_range = sheet.range('A1:A3')
        title_range.font.bold = True
        title_range.font.size = 13
        title_range.font.color = (0, 51, 102)

        # ========== [2/6] 表头行（第5行）格式 / Header Row Format ==========
        print(get_text('setting_header'))
        header_range = sheet.range(f'A5:{last_col_letter}5')
        header_range.font.bold = True
        header_range.font.size = 11
        header_range.color = (255, 242, 204)  # 浅橙色背景
        header_range.font.color = (0, 0, 0)

        # ========== [3/6] 第一列（A列）格式 - 一次性设置 / First Column Format - Set Once ==========
        print(get_text('setting_first_col'))
        first_col_range = sheet.range(f'A{data_start_row}:A{data_end_row}')
        first_col_range.number_format = '0'  # 整数格式
        first_col_range.font.bold = True
        first_col_range.font.size = 10
        first_col_range.color = (204, 255, 204)  # 浅绿色背景
        first_col_range.column_width = 21  # ✅ 修改：14 → 21 (1.5倍)

        # ========== [4/6] 数据区域格式 - 整块设置 / Data Area Format - Set as Block ==========
        print(get_text('setting_data_area'))
        data_cols_range = sheet.range(f'B{data_start_row}:{last_col_letter}{data_end_row}')
        data_cols_range.number_format = '0'  # 整数格式
        data_cols_range.font.size = 10

        # ========== [5/6] 批量调整列宽 - 使用API操作 / Batch Adjust Column Widths - API Operation ==========
        print(get_text('setting_col_width'))

        try:
            # 直接通过API批量设置（最快）- 1.5倍宽度
            sheet.api.Columns(f"B:{last_col_letter}").ColumnWidth = 16.2  # ✅ 修改：10.8 → 16.2 (1.5倍)
        except Exception as e:
            print(f"      ⚠️  API设置失败，使用备用方案: {e}")
            # 备用方案：逐列设置（前100列）- 1.5倍宽度
            for col_idx in range(2, min(last_col + 1, 102)):
                col_letter = xw.utils.col_name(col_idx)
                try:
                    sheet.range(f'{col_letter}:{col_letter}').column_width = 16.2  # ✅ 修改：10.8 → 16.2 (1.5倍)
                except:
                    pass

        # ========== [6/6] 去掉边框 + 冻结窗格 / Remove Borders + Freeze Panes ==========
        print(get_text('freezing_panes'))

        # 去掉所有边框
        all_data_range = sheet.range(f'A1:{last_col_letter}{data_end_row}')
        all_data_range.api.Borders.LineStyle = 0  # 0 = 无边框

        # 冻结窗格
        sheet.range('B6').select()
        app.api.ActiveWindow.FreezePanes = True

        format_time = time.time() - format_start
        print(f"{get_text('format_done')}: {format_time_duration(format_time)}")

    except Exception as e:
        format_time = time.time() - format_start
        print(f"{get_text('format_partial_fail')}: {e}")
        import traceback
        traceback.print_exc()

    # ========== 步骤6：保存文件 / Step 6: Save File ==========
    print(f"\n{get_text('step6')}")

    os.makedirs('../results', exist_ok=True)

    # 根据语言设置文件名
    if LANGUAGE == 'chinese':
        filename = f'../results/哥德巴赫分拆数_{s0}_{s2}.xlsx'
    else:
        filename = f'../results/goldbach_partition_counts_{s0}_{s2}.xlsx'

    try:
        wb.save(filename)
        print(f"{get_text('file_saved')}: {filename}")

    except Exception as e:
        print(f"{get_text('save_failed')}: {e}")
        filename = None

    # ========== 最终统计 / Final Statistics ==========
    total_time = time.time() - start_time

    print("\n" + "=" * 70)
    print(get_text('export_done'))
    print("=" * 70)
    print(get_text('statistics'))
    print(f"{get_text('data_range')}: {2*(s0+1):,} {get_text('to')} {2*s2:,}")
    print(f"{get_text('data_count')}: {total_elements:,} {get_text('even_number')}")
    print(f"{get_text('table_size')}: {rows} {get_text('rows')} × {cols} {get_text('cols')}")
    print(f"{get_text('total_time')}: {format_time_duration(total_time)}")
    print(f"{get_text('data_loading')}: {format_time_duration(load_time)}")
    print(f"{get_text('excel_writing')}: {format_time_duration(write_time)}")
    print(f"{get_text('excel_formatting')}: {format_time_duration(format_time)}")
    if filename:
        print(f"{get_text('save_location')}: {Path(filename).absolute()}")
    print("=" * 70)

    return filename


def export_multiple_files(file_configs):
    """
    批量导出多个文件（双语版）
    Batch export multiple files (bilingual)

    Args:
        file_configs: 配置列表，每项为 (s0, s2, npy_filename) 元组
                      Config list, each item is (s0, s2, npy_filename) tuple
    """
    print(get_text('batch_mode'))
    print(f"{get_text('files_to_export')} {len(file_configs)} {get_text('files')}\n")

    results = []

    for i, config in enumerate(file_configs, 1):
        print(f"\n{'='*70}")
        print(f"{get_text('processing')} {i}/{len(file_configs)}")
        print(f"{'='*70}")

        s0, s2, npy_file = config
        result = export_to_excel(s0, s2, npy_file)
        results.append(result)

        if i < len(file_configs):
            print(f"\n{get_text('wait')}")
            time.sleep(3)

    print("\n" + "="*70)
    print(get_text('batch_done'))
    print("="*70)
    print(get_text('export_results'))
    for i, (config, result) in enumerate(zip(file_configs, results), 1):
        s0, s2, _ = config
        status = get_text('success') if result else get_text('failed')
        print(f"  {i}. S0={s0:,} S2={s2:,} → {status}")
        if result:
            print(f"{get_text('file')}: {result}")


def main():
    """主程序入口 / Main Entry Point"""
    print("\n" + "="*70)
    print(f"{get_text('title')} {get_text('version')}")
    print("="*70 + "\n")

    # ========================================================================
    # 配置区：根据需要修改这里的参数
    # Configuration: Modify parameters here as needed
    # ========================================================================

    mode = 'single'  # 'single' 或 'batch' / 'single' or 'batch'

    if mode == 'single':
        # ===== 单文件导出配置 / Single File Export Configuration =====
        s0 = 0
        s2 = 5000000
        npy_file = None

        rows = 10000
        cols = 5000

        print(get_text('single_mode'))
        print(f"   S0 = {s0:,}")
        print(f"   S2 = {s2:,}")
        print(f"   {get_text('table_layout')}: {rows} {get_text('rows')} × {cols} {get_text('cols')}\n")

        export_to_excel(s0, s2, npy_file, rows, cols)

    else:
        # ===== 批量导出配置 / Batch Export Configuration =====
        file_configs = [
            (0, 1000000, None),
            (1000000, 2000000, None),
            (2000000, 3000000, None),
        ]

        print(get_text('batch_export_mode'))
        print(f"{get_text('files_count')}: {len(file_configs)}\n")

        export_multiple_files(file_configs)

    print(f"\n{get_text('program_done')}")


if __name__ == "__main__":
    main()