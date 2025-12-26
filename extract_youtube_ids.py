#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从原始 WordPress 网站提取 YouTube 视频 ID
"""

import urllib.request
import urllib.parse
import re
from html.parser import HTMLParser

BASE_URL = "http://203.72.57.15/blog_music"

class YouTubeExtractor(HTMLParser):
    """提取 YouTube 视频 ID"""
    def __init__(self):
        super().__init__()
        self.video_ids = []
        self.current_title = ""
        
    def handle_starttag(self, tag, attrs):
        if tag == 'iframe':
            for attr, value in attrs:
                if attr == 'src' and value and 'youtube.com/embed/' in value:
                    # 提取视频 ID
                    match = re.search(r'youtube\.com/embed/([^?&#"\']+)', value)
                    if match:
                        video_id = match.group(1)
                        if video_id and video_id not in self.video_ids:
                            self.video_ids.append(video_id)
        elif tag == 'a':
            href = None
            for attr, value in attrs:
                if attr == 'href':
                    href = value
            if href and ('youtube.com/watch' in href or 'youtu.be/' in href):
                # 提取视频 ID
                match = re.search(r'(?:youtube\.com/watch\?v=|youtu\.be/)([^?&#"\']+)', href)
                if match:
                    video_id = match.group(1)
                    if video_id and video_id not in self.video_ids:
                        self.video_ids.append(video_id)

def extract_from_url(url):
    """从 URL 提取 YouTube 视频 ID"""
    try:
        print(f"正在访问: {url}")
        req = urllib.request.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        
        with urllib.request.urlopen(req, timeout=30) as response:
            html = response.read().decode('utf-8', errors='ignore')
            
        # 使用正则表达式提取所有 YouTube 链接
        youtube_patterns = [
            r'youtube\.com/embed/([^?&#"\']+)',
            r'youtube\.com/watch\?v=([^?&#"\']+)',
            r'youtu\.be/([^?&#"\']+)',
        ]
        
        video_ids = []
        for pattern in youtube_patterns:
            matches = re.findall(pattern, html)
            for match in matches:
                if match and match not in video_ids:
                    video_ids.append(match)
        
        return video_ids
    except Exception as e:
        print(f"错误: {e}")
        return []

def main():
    """主函数"""
    print("=" * 60)
    print("从原始网站提取 YouTube 视频 ID")
    print("=" * 60)
    
    # 尝试访问 post2 的原始页面
    # 需要根据实际的 WordPress URL 结构调整
    post_urls = [
        f"{BASE_URL}/?p=62",  # 可能是 post2 的 ID
        f"{BASE_URL}/?p=61",
        f"{BASE_URL}/?p=60",
    ]
    
    # 或者尝试直接访问已知的页面
    # 根据 WordPress 的 URL 结构，可能需要不同的格式
    
    print("\n请提供原始网站的完整 URL，或者")
    print("我可以尝试从以下可能的 URL 提取：")
    for url in post_urls:
        print(f"  - {url}")
    
    # 让用户输入实际的 URL
    user_url = input("\n请输入 post2 页面的完整 URL（或按 Enter 跳过）: ").strip()
    
    if user_url:
        video_ids = extract_from_url(user_url)
        if video_ids:
            print(f"\n找到 {len(video_ids)} 个 YouTube 视频 ID:")
            for i, vid_id in enumerate(video_ids, 1):
                print(f"  {i}. {vid_id}")
                print(f"     Embed: https://www.youtube.com/embed/{vid_id}")
                print(f"     Watch: https://www.youtube.com/watch?v={vid_id}")
        else:
            print("\n未找到 YouTube 视频 ID")
            print("\n提示：")
            print("1. 请确保您已连接到可以访问原始服务器的网络")
            print("2. 在浏览器中打开原始网站，查看页面源代码")
            print("3. 搜索 'youtube.com/embed/' 或 'youtu.be/' 找到视频 ID")
            print("4. 或者右键点击视频，选择'复制视频地址'")

if __name__ == "__main__":
    main()

