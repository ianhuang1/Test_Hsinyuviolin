#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复 post2.html 中的 YouTube 视频链接
"""

import re
import urllib.request
import urllib.parse

def extract_youtube_id_from_url(url):
    """从各种 YouTube URL 格式中提取视频 ID"""
    patterns = [
        r'youtube\.com/watch\?v=([^&]+)',
        r'youtube\.com/embed/([^?&]+)',
        r'youtu\.be/([^?&]+)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def fix_post2_html(video_ids):
    """
    修复 post2.html 文件
    video_ids: 字典，键是视频标题，值是视频 ID
    """
    html_file = 'post2.html'
    
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 视频标题到视频 ID 的映射
        title_to_id = {
            '208 陳英瀚組 hiphop+即興舞蹈': video_ids.get('208', ''),
            '209 吳光宇組 trance': video_ids.get('209', ''),
            '202 林智雅組 funk': video_ids.get('202', ''),
            '206 沈妍組': video_ids.get('206_shen', ''),
            '206 周宥言組 trance': video_ids.get('206_zhou', ''),
            '205 郭律伶組 Hip Hop': video_ids.get('205', ''),
        }
        
        # 替换每个视频的 iframe 和链接
        for title, video_id in title_to_id.items():
            if not video_id:
                continue
            
            # 替换 iframe src
            old_iframe_pattern = rf'(<h3>{re.escape(title)}</h3>\s*<div class="video-wrapper">\s*<iframe src=")https://www\.youtube\.com/embed/(")'
            new_iframe = rf'\1https://www.youtube.com/embed/{video_id}\2'
            content = re.sub(old_iframe_pattern, new_iframe, content)
            
            # 替换链接
            old_link_pattern = rf'(<h3>{re.escape(title)}</h3>.*?<a href=")#(" target="_blank" class="youtube-link">到以下平台觀看: YouTube</a>)'
            new_link = rf'\1https://www.youtube.com/watch?v={video_id}\2'
            content = re.sub(old_link_pattern, new_link, content, flags=re.DOTALL)
        
        # 写回文件
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✓ 已更新 {html_file}")
        return True
        
    except Exception as e:
        print(f"✗ 错误: {e}")
        return False

def main():
    print("=" * 60)
    print("修复 post2.html 中的 YouTube 视频链接")
    print("=" * 60)
    print("\n请提供以下 6 个视频的 YouTube 视频 ID 或完整链接：\n")
    
    videos = [
        ('208', '208 陳英瀚組 hiphop+即興舞蹈'),
        ('209', '209 吳光宇組 trance'),
        ('202', '202 林智雅組 funk'),
        ('206_shen', '206 沈妍組'),
        ('206_zhou', '206 周宥言組 trance'),
        ('205', '205 郭律伶組 Hip Hop'),
    ]
    
    video_ids = {}
    
    for key, title in videos:
        print(f"{title}:")
        user_input = input("  请输入视频 ID 或完整 YouTube 链接（按 Enter 跳过）: ").strip()
        
        if user_input:
            # 如果是完整链接，提取 ID
            if 'youtube.com' in user_input or 'youtu.be' in user_input:
                video_id = extract_youtube_id_from_url(user_input)
                if video_id:
                    video_ids[key] = video_id
                    print(f"  ✓ 提取到视频 ID: {video_id}\n")
                else:
                    print(f"  ✗ 无法从链接中提取视频 ID\n")
            else:
                # 假设直接输入的是视频 ID
                video_ids[key] = user_input
                print(f"  ✓ 使用视频 ID: {user_input}\n")
        else:
            print(f"  - 跳过\n")
    
    if video_ids:
        print("\n开始修复 post2.html...")
        if fix_post2_html(video_ids):
            print("\n✓ 修复完成！")
            print("\n请检查 post2.html 文件，确认所有视频链接都已正确更新。")
        else:
            print("\n✗ 修复失败，请检查错误信息。")
    else:
        print("\n未提供任何视频 ID，退出。")

if __name__ == "__main__":
    main()

