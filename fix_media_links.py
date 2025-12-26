#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复媒体文件链接脚本
将所有 HTML 文件中的媒体链接更新为正确的本地路径
"""

import os
import re
from pathlib import Path

# 配置
MEDIA_DIR = "media"
HTML_FILES = [
    "post1.html",
    "post2.html", 
    "post3.html",
    "post4.html",
    "post5.html",
    "post6.html",
    "post7.html",
    "about.html",
    "index.html"
]

def fix_media_links(html_file):
    """修复 HTML 文件中的媒体链接"""
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        changes = 0
        
        # 修复重复的 media 路径（多次替换确保全部修复）
        for _ in range(5):  # 最多修复5次嵌套
            content = re.sub(r'media/media/', 'media/', content)
            content = re.sub(r'mediamediamedia/', 'media/', content)
            content = re.sub(r'media/media/media/', 'media/', content)
        
        # 替换所有服务器 URL 为本地路径
        patterns = [
            # 完整 URL
            (r'http://203\.72\.57\.15/blog_music/wp-content/uploads/([^"\'>\s]+)', r'media/wp-content/uploads/\1'),
            (r'http://203\.72\.57\.15/blog_music/wp-content/uploads/([^"\'>\s]+)', r'media/wp-content/uploads/\1'),
            # 相对路径（带 /blog_music）
            (r'/blog_music/wp-content/uploads/([^"\'>\s]+)', r'media/wp-content/uploads/\1'),
            # 相对路径（不带前缀）
            (r'wp-content/uploads/([^"\'>\s]+)', r'media/wp-content/uploads/\1'),
        ]
        
        for pattern, replacement in patterns:
            new_content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
            if new_content != content:
                changes += 1
                content = new_content
        
        # 确保所有 media/ 路径都是正确的
        # 修复可能的双斜杠
        content = re.sub(r'media//', 'media/', content)
        
        if content != original_content:
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ 已修复: {html_file} ({changes} 处更改)")
            return True
        else:
            print(f"- 无需修复: {html_file}")
            return False
    except Exception as e:
        print(f"✗ 修复失败 {html_file}: {str(e)}")
        return False

def main():
    """主函数"""
    print("=" * 60)
    print("修复媒体文件链接")
    print("=" * 60)
    
    fixed = 0
    for html_file in HTML_FILES:
        if not os.path.exists(html_file):
            print(f"警告: 文件不存在 {html_file}")
            continue
        
        if fix_media_links(html_file):
            fixed += 1
    
    print("\n" + "=" * 60)
    print(f"完成！已修复 {fixed} 个文件")
    print("=" * 60)

if __name__ == '__main__':
    main()

