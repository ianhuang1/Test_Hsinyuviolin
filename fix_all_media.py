#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
强力修复所有媒体文件链接
"""

import os
import re

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

def fix_file(filepath):
    """修复单个文件"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        
        # 修复所有重复的 media 路径
        while 'media/media' in content or 'mediamedia' in content:
            content = re.sub(r'media/media+', 'media', content)
            content = re.sub(r'mediamediamedia+', 'media', content)
        
        # 替换所有服务器 URL
        content = re.sub(
            r'http://203\.72\.57\.15/blog_music/wp-content/uploads/([^"\'>\s]+)',
            r'media/wp-content/uploads/\1',
            content
        )
        
        # 替换相对路径
        content = re.sub(
            r'/blog_music/wp-content/uploads/([^"\'>\s]+)',
            r'media/wp-content/uploads/\1',
            content
        )
        
        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
    except Exception as e:
        print(f"错误 {filepath}: {e}")
        return False

def main():
    print("修复所有媒体链接...")
    fixed = 0
    for f in HTML_FILES:
        if os.path.exists(f):
            if fix_file(f):
                print(f"✓ {f}")
                fixed += 1
            else:
                print(f"- {f} (无需修复)")
        else:
            print(f"✗ {f} (不存在)")
    
    print(f"\n完成！修复了 {fixed} 个文件")

if __name__ == '__main__':
    main()

