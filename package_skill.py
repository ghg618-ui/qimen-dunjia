#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
奇门遁甲技能打包脚本
将技能文件夹打包成 .skill 文件（实际上是 zip 文件）
"""

import os
import sys
import zipfile
from pathlib import Path


def package_skill(skill_dir, output_dir=None):
    """
    打包技能文件夹
    """
    skill_path = Path(skill_dir)
    
    if not skill_path.exists():
        print(f"错误：技能目录不存在：{skill_dir}")
        return False
    
    if not skill_path.is_dir():
        print(f"错误：不是一个目录：{skill_dir}")
        return False
    
    # 检查 SKILL.md 是否存在
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        print(f"错误：找不到 SKILL.md 文件")
        return False
    
    # 确定输出目录
    if output_dir is None:
        output_dir = skill_path.parent
    else:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
    
    # 技能名称
    skill_name = skill_path.name
    output_file = output_dir / f"{skill_name}.skill"
    
    print(f"正在打包技能：{skill_name}")
    print(f"源目录：{skill_path}")
    print(f"输出文件：{output_file}")
    
    # 创建 zip 文件
    try:
        with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # 遍历技能目录下的所有文件
            for root, dirs, files in os.walk(skill_path):
                for file in files:
                    file_path = Path(root) / file
                    # 计算相对路径
                    arcname = file_path.relative_to(skill_path.parent)
                    print(f"  添加：{arcname}")
                    zipf.write(file_path, arcname)
        
        print(f"\n✓ 打包成功！")
        print(f"输出文件：{output_file}")
        print(f"文件大小：{output_file.stat().st_size / 1024:.2f} KB")
        return True
        
    except Exception as e:
        print(f"\n✗ 打包失败：{e}")
        return False


def main():
    if len(sys.argv) < 2:
        print("用法：python3 package_skill.py <技能目录> [输出目录]")
        print("示例：python3 package_skill.py ./qimen-dunjia")
        print("示例：python3 package_skill.py ./qimen-dunjia ./dist")
        sys.exit(1)
    
    skill_dir = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None
    
    success = package_skill(skill_dir, output_dir)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
