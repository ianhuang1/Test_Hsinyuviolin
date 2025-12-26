# iTalkShow Music Zone

楊欣瑜老師的音樂教室 - 靜態網站

這是一個從 WordPress 轉換而來的靜態網站，可以部署到 GitHub Pages。

## 網站結構

```
Hsinyuviolin/
├── index.html          # 首頁
├── about.html          # 楊欣瑜老師介紹
├── css/
│   └── style.css       # 統一樣式表
└── README.md           # 本文件
```

## 本地預覽

1. 直接在瀏覽器中打開 `index.html` 文件
2. 或使用本地服務器：
   ```bash
   # 使用 Python 3
   python3 -m http.server 8000
   
   # 或使用 Node.js (需要先安裝 http-server)
   npx http-server
   ```
3. 在瀏覽器中訪問 `http://localhost:8000`

## 部署到 GitHub Pages

### 方法一：使用 GitHub 網頁界面

1. 在 GitHub 上創建一個新的 repository（例如：`Hsinyuviolin`）
2. 將所有文件上傳到 repository
3. 進入 repository 的 Settings
4. 在左側選單中找到 "Pages"
5. 在 "Source" 下拉選單中選擇 "main" 分支（或你的主分支）
6. 點擊 "Save"
7. 幾分鐘後，你的網站將在 `https://[你的用戶名].github.io/Hsinyuviolin/` 上線

### 方法二：使用 Git 命令行

```bash
# 初始化 Git repository
git init

# 添加所有文件
git add .

# 提交
git commit -m "Initial commit: Static website for iTalkShow Music Zone"

# 添加 GitHub remote（替換為你的 repository URL）
git remote add origin https://github.com/[你的用戶名]/Hsinyuviolin.git

# 推送到 GitHub
git branch -M main
git push -u origin main
```

然後按照方法一的步驟 3-7 啟用 GitHub Pages。

## 添加新頁面

當你需要添加新的子頁面時：

1. 創建新的 HTML 文件（例如：`newpage.html`）
2. 複製 `about.html` 的結構作為模板
3. 更新導覽列（`nav`）中的連結
4. 更新頁面內容
5. 確保所有頁面都使用 `css/style.css` 樣式表

### 頁面模板結構

```html
<!DOCTYPE html>
<html lang="zh-Hant">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>頁面標題 - iTalkShow Music Zone</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
    <header>
        <h1>iTalkShow Music Zone</h1>
        <p>楊欣瑜老師的音樂教室</p>
    </header>

    <nav>
        <a href="index.html">Home</a>
        <a href="about.html">楊欣瑜老師介紹</a>
        <!-- 添加更多導覽連結 -->
    </nav>

    <div class="main-container content-page">
        <!-- 你的內容在這裡 -->
    </div>

    <footer>
        <div class="footer-content">
            <p>iTalkShow Music Zone © 2025</p>
            <p>Theme by WP Puzzle</p>
        </div>
    </footer>
</body>
</html>
```

## 注意事項

- 所有圖片應該放在 `images/` 目錄中
- 確保所有內部連結使用相對路徑
- 如果需要添加 JavaScript，可以創建 `js/` 目錄
- 樣式修改請統一在 `css/style.css` 中進行

## 技術說明

- 純 HTML/CSS，無需服務器端處理
- 響應式設計，支援手機和平板
- 兼容現代瀏覽器

