# 修复 YouTube 视频链接说明

## 问题说明

`post2.html` 页面中的 YouTube 视频链接显示为空，这是因为原始备份文件中的 iframe src 属性也是空的。WordPress 可能使用了 JavaScript 动态加载视频，导致备份文件中没有包含实际的视频 ID。

## 解决方案

您需要从原始 WordPress 网站获取实际的 YouTube 视频 ID，然后手动更新 `post2.html` 文件。

### 方法 1：从浏览器获取（推荐）

1. **访问原始网站**：在可以访问原始服务器的网络环境下，打开原始 WordPress 网站
2. **打开 post2 页面**：找到对应的页面（"市大同106學年度音樂科-楊欣瑜老師【高二學生EDM混音軟體Launch pad發表】"）
3. **查看页面源代码**：
   - 在浏览器中按 `F12` 或右键选择"检查"
   - 切换到"网络"（Network）标签
   - 刷新页面
   - 搜索 "youtube.com/embed/" 或查看 iframe 元素
4. **提取视频 ID**：
   - 找到类似 `https://www.youtube.com/embed/VIDEO_ID` 的链接
   - 复制每个视频的 ID（VIDEO_ID 部分）

### 方法 2：从视频直接获取

1. **在原始网站上播放视频**
2. **右键点击视频**，选择"复制视频地址"或"复制嵌入代码"
3. **提取视频 ID**：
   - 如果得到 `https://www.youtube.com/watch?v=VIDEO_ID`，VIDEO_ID 就是视频 ID
   - 如果得到 `https://youtu.be/VIDEO_ID`，VIDEO_ID 就是视频 ID
   - 如果得到嵌入代码 `<iframe src="https://www.youtube.com/embed/VIDEO_ID">`，VIDEO_ID 就是视频 ID

### 方法 3：使用提供的脚本

运行 `extract_youtube_ids.py` 脚本（需要连接到原始服务器）：

```bash
python3 extract_youtube_ids.py
```

然后按照提示输入原始网站的 URL。

## 更新 post2.html

获取到所有视频 ID 后，按照以下格式更新 `post2.html`：

```html
<iframe src="https://www.youtube.com/embed/VIDEO_ID" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
<a href="https://www.youtube.com/watch?v=VIDEO_ID" target="_blank" class="youtube-link">到以下平台觀看: YouTube</a>
```

### 需要更新的视频列表

根据 `post2.html`，需要找到以下 6 个视频的 ID：

1. **208 陳英瀚組 hiphop+即興舞蹈**
2. **209 吳光宇組 trance**
3. **202 林智雅組 funk**
4. **206 沈妍組**
5. **206 周宥言組 trance**
6. **205 郭律伶組 Hip Hop**

## 示例

假设您找到了第一个视频的 ID 是 `abc123xyz`，那么更新后的代码应该是：

```html
<div class="video-entry">
    <h3>208 陳英瀚組 hiphop+即興舞蹈</h3>
    <div class="video-wrapper">
        <iframe src="https://www.youtube.com/embed/abc123xyz" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
    </div>
    <a href="https://www.youtube.com/watch?v=abc123xyz" target="_blank" class="youtube-link">到以下平台觀看: YouTube</a>
</div>
```

## 注意事项

- 确保所有视频 ID 都是正确的，否则视频将无法播放
- 如果某些视频已被删除或设为私有，您可能需要联系视频所有者或使用替代视频
- 更新后，请在浏览器中测试所有视频是否都能正常播放

