#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试检索系统是否能被 agent 正常使用
"""

import subprocess
import sys
from pathlib import Path

def test_improved_hybrid_search():
    """测试 improved_hybrid_search.py"""
    print("=" * 80)
    print("测试 1: improved_hybrid_search.py (男频)")
    print("=" * 80)

    try:
        result = subprocess.run(
            ["python3", "scripts/improved_hybrid_search.py", "重生 复仇 豪门", "male"],
            capture_output=True,
            text=True,
            timeout=120,
            cwd=Path(__file__).resolve().parent.parent
        )

        if result.returncode == 0:
            print("✅ improved_hybrid_search.py 执行成功")

            # 检查是否有文件列表输出
            if "检索到的文件列表:" in result.stdout:
                print("✅ 输出包含文件列表")

                # 提取文件列表
                lines = result.stdout.split('\n')
                file_list = []
                in_file_list = False
                for line in lines:
                    if "检索到的文件列表:" in line:
                        in_file_list = True
                        continue
                    if in_file_list and line.strip() and line[0].isdigit():
                        # 提取文件名（去掉序号和[男频]/[女频]标记）
                        filename = line.split('. ', 1)[1] if '. ' in line else line
                        # 去掉 [男频] 或 [女频] 标记
                        filename = filename.replace('[男频] ', '').replace('[女频] ', '').strip()
                        file_list.append(filename)

                print(f"✅ 检索到 {len(file_list)} 个文件:")
                for i, f in enumerate(file_list, 1):
                    print(f"   {i}. {f}")

                # 验证文件是否存在
                print("\n验证文件是否存在:")
                base_path = Path(__file__).resolve().parent.parent / "knowledge/hit-scripts-md"
                for filename in file_list:
                    file_path = base_path / filename
                    if file_path.exists():
                        print(f"   ✅ {filename}")
                    else:
                        print(f"   ❌ {filename} (文件不存在)")

                return True, file_list
            else:
                print("❌ 输出不包含文件列表")
                return False, []
        else:
            print(f"❌ improved_hybrid_search.py 执行失败 (退出码: {result.returncode})")
            print(f"错误信息: {result.stderr}")
            return False, []

    except subprocess.TimeoutExpired:
        print("❌ improved_hybrid_search.py 执行超时")
        return False, []
    except Exception as e:
        print(f"❌ 执行出错: {e}")
        return False, []

def test_quick_search():
    """测试 quick_search.py"""
    print("\n" + "=" * 80)
    print("测试 2: quick_search.py (备选方案)")
    print("=" * 80)

    try:
        result = subprocess.run(
            ["python3", "scripts/quick_search.py", "重生 复仇 豪门"],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=Path(__file__).resolve().parent.parent
        )

        if result.returncode == 0:
            print("✅ quick_search.py 执行成功")

            # 检查是否有结果
            if "找到" in result.stdout and "个相关剧本" in result.stdout:
                print("✅ 成功检索到相关剧本")

                # 提取文件列表
                lines = result.stdout.split('\n')
                file_list = []
                for line in lines:
                    if line.strip() and line[0].isdigit() and '. ' in line:
                        # 提取文件名
                        parts = line.split('\n')[0]
                        if '. ' in parts:
                            filename = parts.split('. ', 1)[1].strip()
                            if filename:
                                file_list.append(filename)

                print(f"✅ 检索到 {len(file_list)} 个文件")

                return True, file_list
            else:
                print("❌ 未找到相关剧本")
                return False, []
        else:
            print(f"❌ quick_search.py 执行失败 (退出码: {result.returncode})")
            return False, []

    except Exception as e:
        print(f"❌ 执行出错: {e}")
        return False, []

def test_file_reading(file_list):
    """测试是否能读取检索到的文件"""
    print("\n" + "=" * 80)
    print("测试 3: 读取检索到的文件")
    print("=" * 80)

    base_path = Path(__file__).resolve().parent.parent / "knowledge/hit-scripts-md"

    success_count = 0
    for filename in file_list[:3]:  # 只测试前3个
        file_path = base_path / filename
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                print(f"✅ 成功读取: {filename} ({len(content)} 字符)")
                success_count += 1
        except Exception as e:
            print(f"❌ 读取失败: {filename} - {e}")

    return success_count == len(file_list[:3])

def main():
    print("\n" + "=" * 80)
    print("检索系统测试")
    print("=" * 80 + "\n")

    # 测试 improved_hybrid_search
    improved_success, improved_files = test_improved_hybrid_search()

    # 测试 quick_search
    quick_success, quick_files = test_quick_search()

    # 测试文件读取
    if improved_files:
        file_read_success = test_file_reading(improved_files)
    elif quick_files:
        file_read_success = test_file_reading(quick_files)
    else:
        file_read_success = False
        print("\n❌ 没有文件可供测试读取")

    # 总结
    print("\n" + "=" * 80)
    print("测试总结")
    print("=" * 80)
    print(f"improved_hybrid_search.py: {'✅ 通过' if improved_success else '❌ 失败'}")
    print(f"quick_search.py: {'✅ 通过' if quick_success else '❌ 失败'}")
    print(f"文件读取: {'✅ 通过' if file_read_success else '❌ 失败'}")

    if improved_success or quick_success:
        print("\n✅ 检索系统可以正常使用")
        print("建议: agent 可以使用以下命令检索参考剧本:")
        if improved_success:
            print('  python3 scripts/improved_hybrid_search.py "关键词1 关键词2 关键词3" [male|female|all]')
        if quick_success:
            print('  python3 scripts/quick_search.py "关键词1 关键词2 关键词3"')
        return 0
    else:
        print("\n❌ 检索系统存在问题，需要修复")
        return 1

if __name__ == "__main__":
    sys.exit(main())
