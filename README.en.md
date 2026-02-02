# WangScape (Hugo Blog)

[![Hugo](https://img.shields.io/badge/Hugo-v0.154.0+-blueviolet?style=flat-square)](https://gohugo.io/)
[![Go](https://img.shields.io/badge/Go-1.21+-00ADD8?style=flat-square)](https://golang.org/)
[![License](https://img.shields.io/badge/license-MIT-blue?style=flat-square)](LICENSE)

> "Partial I go when flowers fill the tower, partial I come when spring is not met."

A personal blog system built with Hugo and the [Stack Theme](https://github.com/CaiJimmy/hugo-theme-stack), paired with the powerful Go-based writing tool **WSwriter**. Delivering an ultimate reading experience and streamlined creative workflow.

## ✨ Key Features

### 🎨 Frontend Experience
- **Silky Smooth**: Full-site animations with hardware acceleration and custom Bezier curves for seamless interactions
- **Fixed Layout**: Sidebars and controls remain fixed, only content scrolls for immersive reading
- **Premium Dark Mode**: Breathing dark-gray gradient animation, comfortable and easy on the eyes at night
- **Perfect Bilingual**: Auto-switching between Chinese and English with intelligent menu and text adaptation

### ⚡ Writing Tool (WSwriter)
High-performance writing assistant rewritten in **Go**, offering Office-style creative interface.

- **Lightning Fast**: <50ms startup time, zero dependencies (20x faster than Python version)
- **Office Style**: Familiar paper-like editing area with rich feature buttons
- **Smart Bilingual**: Input Chinese title and auto-generate English version
- **One-Click Publish**: Preview, save, and commit all in one interface

## 🚀 Quick Start

### Prerequisites
- [Hugo Extended](https://gohugo.io/installation/) (v0.100.0+)
- [Git](https://git-scm.com/)
- Windows / macOS / Linux

### Start the Writing Tool

**Simplest way**:

\\\ash
# Windows
.\WSwriter.exe

# macOS / Linux
./WSwriter
\\\

Browser automatically opens \http://localhost:8080\, start writing immediately!

### Traditional Way (Hugo CLI)

\\\ash
hugo server
\\\

Visit \http://localhost:1313\ for local preview

## 📁 Project Structure

\\\
content/              # Blog posts source
├── zh-cn/           # Chinese content
├── en/              # English content
└── page/            # Pages

assets/
├── js/              # Custom JavaScript
└── scss/
    └── custom.scss  # Core style customizations

config/              # Hugo configuration
layouts/             # Theme template overrides
WSwriter.exe         # Writing tool (executable)
WSwriter.go          # Writing tool source code
\\\

## 📝 Writing Workflow

### Using WSwriter (Recommended)

1. **Start the tool**:
   \\\ash
   .\WSwriter.exe
   \\\

2. **Create a post**:
   - Click **"New Post"**
   - Enter Chinese title and categories
   - System auto-creates bilingual files (zh-cn + en)

3. **Edit content**:
   - Click post in the list to edit
   - Supports Markdown format
   - Real-time save

4. **Publish**:
   - Click **"Publish"** button
   - One-click Git commit and push
   - Or click **"Preview"** to launch local server

### FrontMatter Example

\\\yaml
---
title: "Your Title Here"
date: 2026-02-02T10:00:00Z
categories:
  - Life
  - Tech
draft: false
---

Your Markdown content here...
\\\

## 🛠️ Development Guide

### Modify Styles

Edit \ssets/scss/custom.scss\, Hugo auto-compiles:

\\\ash
hugo --minify
\\\

### Compile Writing Tool

To update WSwriter:

\\\ash
# Windows
go build -o WSwriter.exe WSwriter.go

# macOS/Linux
go build -o WSwriter WSwriter.go
\\\

### Cross-Platform Build

\\\ash
# macOS (Intel)
GOOS=darwin GOARCH=amd64 go build -o WSwriter WSwriter.go

# macOS (Apple Silicon)
GOOS=darwin GOARCH=arm64 go build -o WSwriter WSwriter.go

# Linux
GOOS=linux GOARCH=amd64 go build -o WSwriter WSwriter.go
\\\

## 📊 Performance Metrics

| Metric | Value |
|--------|-------|
| Hugo Build Time | ~147ms |
| WSwriter Startup | <50ms |
| Memory Usage | 5-15MB |
| Languages | Chinese + English |
| Deployment | Git + Static Hosting |

## 📄 License

MIT License - See [LICENSE](LICENSE) for details
