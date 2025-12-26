#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
下载脚本：从原始服务器下载所有媒体文件并更新网页链接
"""

import os
import re
import urllib.request
import urllib.parse
from pathlib import Path
from html.parser import HTMLParser
import time

# 配置
BASE_URL = "http://203.72.57.15"
MEDIA_DIR = "media"
HTML_FILES = [
    "post1.html",
    "post2.html", 
    "post3.html",
    "post4.html",
    "post5.html",
    "post6.html",
    "post7.html",
    "about.html"
]
ORIGIN_BACKUPS = [
    "origin_backups/p1.html",
    "origin_backups/p2.html",
    "origin_backups/p3.html",
    "origin_backups/p4.html",
    "origin_backups/p5.html",
    "origin_backups/p6.html",
    "origin_backups/p7.html",
    "origin_backups/about.html",
    "origin_backups/main.html",
]

class MediaExtractor(HTMLParser):
    """提取 HTML 中的媒体文件链接"""
    def __init__(self):
        super().__init__()
        self.media_urls = set()
        
    def handle_starttag(self, tag, attrs):
        if tag == 'img':
            for attr, value in attrs:
                if attr == 'src' and value:
                    self.media_urls.add(value)
        elif tag == 'source':
            for attr, value in attrs:
                if attr == 'src' and value:
                    self.media_urls.add(value)
        elif tag == 'audio':
            for attr, value in attrs:
                if attr == 'src' and value:
                    self.media_urls.add(value)
        elif tag == 'video':
            for attr, value in attrs:
                if attr == 'src' and value:
                    self.media_urls.add(value)
        elif tag == 'a':
            for attr, value in attrs:
                if attr == 'href' and value and (value.endswith('.mp3') or value.endswith('.mp4')):
                    self.media_urls.add(value)

def extract_media_urls(html_content):
    """从 HTML 内容中提取所有媒体文件 URL"""
    parser = MediaExtractor()
    parser.feed(html_content)
    
    # 也使用正则表达式查找
    patterns = [
        r'src=["\']([^"\']*\.(?:mp3|mp4|jpg|jpeg|png|gif))["\']',
        r'href=["\']([^"\']*\.(?:mp3|mp4|jpg|jpeg|png|gif))["\']',
        r'<source[^>]*src=["\']([^"\']*\.(?:mp3|mp4))["\']',
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, html_content, re.IGNORECASE)
        parser.media_urls.update(matches)
    
    return parser.media_urls

def normalize_url(url):
    """标准化 URL"""
    # 移除查询参数
    url = url.split('?')[0]
    
    # 处理 data/images/ 路径（about.html 中的图片）
    if url.startswith('data/images/'):
        # 这些图片可能在服务器的 data/images/ 目录下
        return BASE_URL + '/blog_music/' + url
    
    # 如果已经包含 media/，移除它（避免重复）
    if '/media/' in url and not url.startswith('http'):
        url = url.replace('/media/', '/')
        url = url.replace('media/', '')
    
    # 如果是相对路径，添加基础路径
    if url.startswith('/'):
        return BASE_URL + url
    elif url.startswith('http://') or url.startswith('https://'):
        return url
    else:
        # 如果是 wp-content/uploads/ 路径，直接添加
        if url.startswith('wp-content/'):
            return BASE_URL + '/blog_music/' + url
        return BASE_URL + '/blog_music/' + url

def download_file(url, local_path):
    """下载文件"""
    try:
        print(f"正在下载: {url}")
        
        # 创建目录
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        
        # 下载文件（处理中文文件名）
        req = urllib.request.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        
        # 对 URL 进行编码处理
        try:
            encoded_url = urllib.parse.quote(url, safe=':/?#[]@!$&\'()*+,;=')
        except:
            encoded_url = url
        
        with urllib.request.urlopen(req, timeout=30) as response:
            with open(local_path, 'wb') as f:
                f.write(response.read())
        
        print(f"✓ 下载成功: {local_path}")
        return True
    except urllib.error.HTTPError as e:
        if e.code == 404:
            # 尝试不同的路径
            alt_urls = [
                url.replace('/blog_music/media/', '/blog_music/'),
                url.replace('/media/', '/'),
                BASE_URL + '/blog_music/wp-content/uploads/' + url.split('uploads/')[-1] if 'uploads/' in url else None,
            ]
            for alt_url in alt_urls:
                if alt_url and alt_url != url:
                    try:
                        req = urllib.request.Request(alt_url)
                        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
                        with urllib.request.urlopen(req, timeout=30) as response:
                            with open(local_path, 'wb') as f:
                                f.write(response.read())
                        print(f"✓ 下载成功（备用路径）: {local_path}")
                        return True
                    except:
                        continue
        print(f"✗ 下载失败 {url}: HTTP {e.code}")
        return False
    except Exception as e:
        print(f"✗ 下载失败 {url}: {str(e)}")
        return False

def update_html_links(html_file, url_mapping):
    """更新 HTML 文件中的链接"""
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        changes_made = False
        
        # 按 URL 长度排序，先替换长的（避免部分匹配问题）
        sorted_mappings = sorted(url_mapping.items(), key=lambda x: len(x[0]), reverse=True)
        
        for old_url, new_url in sorted_mappings:
            if not old_url or old_url == new_url:
                continue
            
            # 移除查询参数进行匹配
            old_url_clean = old_url.split('?')[0]
            
            # 创建各种可能的模式
            patterns_to_replace = [
                # 完整 URL
                (old_url, new_url),
                (old_url_clean, new_url),
                # 带引号的
                (f'"{old_url}"', f'"{new_url}"'),
                (f"'{old_url}'", f"'{new_url}'"),
                (f'"{old_url_clean}"', f'"{new_url}"'),
                (f"'{old_url_clean}'", f"'{new_url}'"),
                # src 和 href 属性
                (f'src="{old_url}"', f'src="{new_url}"'),
                (f"src='{old_url}'", f"src='{new_url}'"),
                (f'href="{old_url}"', f'href="{new_url}"'),
                (f"href='{old_url}'", f"href='{new_url}'"),
                (f'src="{old_url_clean}"', f'src="{new_url}"'),
                (f"src='{old_url_clean}'", f"src='{new_url}'"),
                (f'href="{old_url_clean}"', f'href="{new_url}"'),
                (f"href='{old_url_clean}'", f"href='{new_url}'"),
            ]
            
            for old_pattern, new_pattern in patterns_to_replace:
                if old_pattern in content:
                    content = content.replace(old_pattern, new_pattern)
                    changes_made = True
        
        if changes_made:
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ 已更新: {html_file}")
            return True
        else:
            print(f"- 无需更新: {html_file}")
            return False
    except Exception as e:
        print(f"✗ 更新失败 {html_file}: {str(e)}")
        return False

def main():
    """主函数"""
    print("=" * 60)
    print("媒体文件下载脚本")
    print("=" * 60)
    
    # 创建媒体目录
    os.makedirs(MEDIA_DIR, exist_ok=True)
    
    # 收集所有需要下载的 URL
    all_media_urls = set()
    
    print("\n步骤 1: 扫描 HTML 文件，提取媒体链接...")
    
    # 先扫描原始备份文件（包含完整的资源链接）
    print("\n扫描原始备份文件...")
    for html_file in ORIGIN_BACKUPS:
        if not os.path.exists(html_file):
            continue
        
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            urls = extract_media_urls(content)
            print(f"  {html_file}: 找到 {len(urls)} 个媒体链接")
            all_media_urls.update(urls)
        except Exception as e:
            print(f"  警告: 无法读取 {html_file}: {e}")
    
    # 再扫描当前 HTML 文件
    print("\n扫描当前 HTML 文件...")
    for html_file in HTML_FILES:
        if not os.path.exists(html_file):
            print(f"警告: 文件不存在 {html_file}")
            continue
        
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            urls = extract_media_urls(content)
            print(f"  {html_file}: 找到 {len(urls)} 个媒体链接")
            all_media_urls.update(urls)
        except Exception as e:
            print(f"  警告: 无法读取 {html_file}: {e}")
    
    print(f"\n总共找到 {len(all_media_urls)} 个唯一的媒体文件")
    
    # 过滤和标准化 URL
    media_files = []
    for url in all_media_urls:
        # 只处理媒体文件
        if not re.search(r'\.(mp3|mp4|jpg|jpeg|png|gif)$', url, re.IGNORECASE):
            continue
        
        normalized = normalize_url(url)
        # 提取文件名和路径
        path_parts = normalized.replace(BASE_URL, '').strip('/').split('/')
        # 移除 'blog_music' 前缀
        if path_parts and path_parts[0] == 'blog_music':
            path_parts = path_parts[1:]
        
        # 移除可能的 media/ 前缀（如果存在）
        if path_parts and path_parts[0] == 'media':
            path_parts = path_parts[1:]
        
        # 处理 data/images/ 路径
        if path_parts and path_parts[0] == 'data':
            # 保持 data/images/ 结构
            pass
        elif not path_parts or not path_parts[-1]:
            continue
        
        local_path = os.path.join(MEDIA_DIR, *path_parts)
        relative_url = '/'.join([MEDIA_DIR] + path_parts)
        
        media_files.append({
            'url': normalized,
            'local_path': local_path,
            'relative_url': relative_url,
            'original_url': url
        })
    
    print(f"\n步骤 2: 下载 {len(media_files)} 个媒体文件...")
    print("-" * 60)
    
    url_mapping = {}
    downloaded = 0
    failed = 0
    
    for i, media in enumerate(media_files, 1):
        print(f"\n[{i}/{len(media_files)}] {os.path.basename(media['local_path'])}")
        
        # 如果文件已存在，跳过
        if os.path.exists(media['local_path']):
            print(f"  文件已存在，跳过")
        elif download_file(media['url'], media['local_path']):
            downloaded += 1
        else:
            failed += 1
            continue
        
        # 添加所有可能的 URL 映射
        url_mapping[media['url']] = media['relative_url']
        url_mapping[media['original_url']] = media['relative_url']
        
        # 处理相对路径
        rel_path = media['url'].replace(BASE_URL, '').strip('/')
        if rel_path:
            url_mapping[rel_path] = media['relative_url']
            url_mapping['/' + rel_path] = media['relative_url']
        
        # 处理带 blog_music 前缀的路径
        if rel_path.startswith('blog_music/'):
            url_mapping[rel_path.replace('blog_music/', '')] = media['relative_url']
            url_mapping['/' + rel_path.replace('blog_music/', '')] = media['relative_url']
        
        # 避免请求过快
        time.sleep(0.5)
    
    print("\n" + "=" * 60)
    print(f"下载完成: 成功 {downloaded} 个, 失败 {failed} 个")
    
    print("\n步骤 3: 更新 HTML 文件中的链接...")
    print("-" * 60)
    
    updated = 0
    for html_file in HTML_FILES:
        if not os.path.exists(html_file):
            continue
        
        if update_html_links(html_file, url_mapping):
            updated += 1
    
    print("\n" + "=" * 60)
    print("完成！")
    print(f"  - 下载文件: {downloaded} 个")
    print(f"  - 更新 HTML: {updated} 个文件")
    print(f"  - 媒体文件保存在: {MEDIA_DIR}/")
    print("=" * 60)

if __name__ == '__main__':
    main()

