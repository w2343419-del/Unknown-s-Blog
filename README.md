# WangScape (Hugo Blog)

[![Hugo](https://img.shields.io/badge/Hugo-v0.120.0+-blueviolet?style=flat-square)](https://gohugo.io/)
[![License](https://img.shields.io/badge/license-MIT-blue?style=flat-square)](LICENSE)

> "偏我去时花满楼，偏我来时不逢春。"

本项目是基于 Hugo 和 [Stack Theme](https://github.com/CaiJimmy/hugo-theme-stack) 构建的个人博客系统。经过深度的 UI 定制和功能增强，旨在提供极致的阅读体验和便捷的写作流程。

## ✨ 核心特性

### 1. 极致 UI 体验
- **丝滑流畅**：全站动画经过硬件加速优化，配合自定义贝塞尔曲线，带来如丝般顺滑的交互体验。
- **固定布局 (Fixed Layout)**：独特的无整页滚动设计。侧边栏和控制栏始终固定，仅文章内容区域滚动，提供沉浸式阅读感。
- **高级暗色模式**：摒弃死板的纯黑背景，采用呼吸式的深灰渐变动画，配合无阴影的边框设计，夜晚阅读更舒适。
- **国际化支持**：完美的中英双语切换，自动适配菜单、链接和界面文本。

### 2. 强大的写作工具 (WangScape Writer)
本项目内置了独家开发的 `hugo_writer.py` 写作助手，为您提供类似 Word 的写作体验。

- **Office 风格界面**：熟悉的纸张式写作区，顶部功能区包含预览、发布等常用操作。
- **双语同步生成**：只需输入中文标题，系统会自动调用 API 翻译并同步创建英文版草稿。
- **一键预览与发布**：无需记忆复杂的 Hugo 命令行，点点鼠标即可启动本地服务器或推送更新到 GitHub。

## 🚀 快速开始

### 环境要求
- [Hugo Extended](https://gohugo.io/installation/) (建议 v0.100.0+)
- Python 3.x (用于写作助手)
- Git

### 安装与运行

1. **克隆仓库**：
   ```bash
   git clone https://github.com/w2343419-del/WangScape.git
   cd WangScape
   ```

2. **启动写作助手** (推荐)：
   ```bash
   python hugo_writer.py
   ```
   浏览器将自动打开 `http://localhost:8080`，你可以立即开始创作。

3. **传统方式运行**：
   ```bash
   hugo server
   ```

## 🛠️ 项目结构

- `content/`: 博客文章源码 (Markdown)
  - `zh-cn/`: 中文内容
  - `en/`: 英文内容
- `assets/scss/custom.scss`: 核心样式定制 (CSS Override)
- `hugo_writer.py`: 写作助手核心脚本
- `config/`: 站点配置文件 (已拆分为多语言配置)

## 📝 写作指南

建议始终使用 **WangScape Writer** 进行创作，因为它会自动处理 FrontMatter 元数据和文件路径。

1. 打开助手界面。
2. 点击顶部 **"New Post"**。
3. 输入中文标题和分类。
4. 确认后，系统会自动创建中英双语文件。
5. 在左侧列表选择文件进行预览。
6. 点击 **"Deploy"** 一键发布。

## 📄 许可证

本项目遵循 MIT 许可证。
