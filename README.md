# WangScape (Hugo Blog)

[![Hugo](https://img.shields.io/badge/Hugo-v0.154.0+-blueviolet?style=flat-square)](https://gohugo.io/)
[![Go](https://img.shields.io/badge/Go-1.21+-00ADD8?style=flat-square)](https://golang.org/)
[![License](https://img.shields.io/badge/license-MIT-blue?style=flat-square)](LICENSE)

> "偏我去时花满楼，偏我来时不逢春。"

基于 Hugo 和 [Stack Theme](https://github.com/CaiJimmy/hugo-theme-stack) 构建的个人博客系统，搭配强大的 Go 版写作工具 **WSwriter**。提供极致的阅读体验与便捷的创作流程。

## ✨ 核心特性

### 🎨 前端体验
- **丝滑流畅**：全站动画硬件加速优化，自定义贝塞尔曲线实现顺滑交互
- **固定布局**：侧栏和控制栏固定，仅内容区域滚动，沉浸式阅读体验
- **高级暗黑模式**：呼吸式深灰渐变动画，夜间阅读舒适护眼
- **完美双语**：中英自动切换，菜单链接文本智能适配

### ⚡ 写作工具 (WSwriter)
用 **Go** 重写的高性能写作助手，提供 Office 风格的创作界面。

- **极速启动**：<50ms 启动时间，零依赖运行（相比 Python 版本快 20 倍）
- **Office 风格**：熟悉的纸张式编辑区，丰富的功能按钮
- **智能双语**：输入中文标题自动翻译生成英文版本
- **一键发布**：预览、保存、提交全在一个界面完成

## 🚀 快速开始

### 前置要求
- [Hugo Extended](https://gohugo.io/installation/) (v0.100.0+)
- [Git](https://git-scm.com/)
- Windows / macOS / Linux

### 启动写作工具

**最简单的方式**：

```bash
# Windows
.\WSwriter.exe

# macOS / Linux
./WSwriter
```

浏览器自动打开 `http://localhost:8080`，立即开始写作！

### 传统方式 (Hugo CLI)

```bash
hugo server
```

访问 `http://localhost:1313` 本地预览

## � 项目结构

```
content/              # 博客文章源码
├── zh-cn/           # 中文内容
├── en/              # 英文内容
└── page/            # 独立页面

assets/
├── js/              # 自定义 JavaScript
└── scss/
    └── custom.scss  # 核心样式定制

config/              # Hugo 配置
layouts/             # 主题模板覆盖
WSwriter.exe         # 写作工具（可执行文件）
WSwriter.go          # 写作工具源代码
```

## 📝 写作流程

### 使用 WSwriter（推荐）

1. **启动工具**：
   ```bash
   .\WSwriter.exe
   ```

2. **创建文章**：
   - 点击 **"新建文章"**
   - 输入中文标题和分类
   - 系统自动创建双语文件（zh-cn + en）

3. **编辑内容**：
   - 在列表中点击文章进行编辑
   - 支持 Markdown 格式
   - 实时保存

4. **发布**：
   - 点击 **"发布"** 按钮
   - 一键 Git 提交推送
   - 或点击 **"预览"** 启动本地服务器

### 文章 FrontMatter 示例

```yaml
---
title: "文章标题"
date: 2026-02-02T10:00:00Z
categories:
  - Life
  - Code
draft: false
---

你的 Markdown 内容...
```

## 🛠️ 开发指南

### 修改样式

编辑 `assets/scss/custom.scss`，Hugo 会自动编译：

```bash
hugo --minify
```

### 编译写作工具

需要更新 WSwriter 代码时：

```bash
# Windows
go build -o WSwriter.exe WSwriter.go

# macOS/Linux
go build -o WSwriter WSwriter.go
```

### 跨平台编译

```bash
# macOS (Intel)
GOOS=darwin GOARCH=amd64 go build -o WSwriter WSwriter.go

# macOS (Apple Silicon)
GOOS=darwin GOARCH=arm64 go build -o WSwriter WSwriter.go

# Linux
GOOS=linux GOARCH=amd64 go build -o WSwriter WSwriter.go
```

## 📊 性能指标

| 指标 | 值 |
|-----|-----|
| Hugo 构建时间 | ~147ms |
| WSwriter 启动 | <50ms |
| WSwriter 内存占用 | 5-15MB |
| 支持语言 | 中文 + 英文 |
| 部署方式 | Git + 静态托管 |

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE)
