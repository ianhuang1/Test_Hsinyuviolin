#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复所有 HTML 文件中的 YouTube 嵌入代码
使用标准的 YouTube 嵌入格式
"""

import re
import os

def fix_youtube_iframe(content):
    """修复 YouTube iframe 代码"""
    # 匹配所有 YouTube iframe
    pattern = r'(<iframe src="https://www\.youtube\.com/embed/([^?"]+)(\?[^"]*)?")'
    
    def replace_iframe(match):
        full_src = match.group(1)
        video_id = match.group(2)
        existing_params = match.group(3) if match.group(3) else ''
        
        # 构建新的 URL，确保使用正确的参数
        # 使用标准的 YouTube 嵌入格式，不添加额外的参数（除非必要）
        new_src = f'<iframe src="https://www.youtube.com/embed/{video_id}"'
        
        return new_src
    
    # 替换所有匹配的 iframe
    content = re.sub(pattern, replace_iframe, content)
    
    # 确保 iframe 有正确的属性
    # 修复可能缺少的 allowfullscreen 属性
    content = re.sub(
        r'(<iframe[^>]*src="https://www\.youtube\.com/embed/[^"]+"[^>]*)(?<!allowfullscreen)(>)',
        r'\1 allowfullscreen\2',
        content
    )
    
    return content

def fix_html_file(filepath):
    """修复单个 HTML 文件"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        content = fix_youtube_iframe(content)
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ 已修复: {filepath}")
            return True
        else:
            print(f"- 无需修复: {filepath}")
            return False
    except Exception as e:
        print(f"✗ 错误 {filepath}: {e}")
        return False

def main():
    print("=" * 60)
    print("修复所有 HTML 文件中的 YouTube 嵌入代码")
    print("=" * 60)
    
    html_files = [
        'post1.html',
        'post2.html',
        'post3.html',
        'post4.html',
        'post5.html',
        'post6.html',
        'post7.html',
    ]
    
    fixed_count = 0
    for html_file in html_files:
        if os.path.exists(html_file):
            if fix_html_file(html_file):
                fixed_count += 1
    
    print(f"\n完成！修复了 {fixed_count} 个文件")

if __name__ == "__main__":
    main()

