# WangScape (Hugo Blog)

[![Hugo](https://img.shields.io/badge/Hugo-v0.120.0+-blueviolet?style=flat-square)](https://gohugo.io/)
[![License](https://img.shields.io/badge/license-MIT-blue?style=flat-square)](LICENSE)

> "Partial I go when flowers fill the tower, partial I come when spring is not met."

This project is a personal blog system based on Hugo and the [Stack Theme](https://github.com/CaiJimmy/hugo-theme-stack). It features extensive UI customizations and functional enhancements to provide an ultimate reading experience and a streamlined writing workflow.

## ✨ Key Features

### 1. Ultimate UI Experience
- **Silky Smooth**: Animations are optimized with hardware acceleration and custom Bezier curves for buttery-smooth interactions.
- **Fixed Layout**: A unique design where the page body doesn't scroll. Sidebars and controls remain fixed, while only the article content scrolls, offering an immersive reading environment.
- **Premium Dark Mode**: Replaces flat black backgrounds with a breathing, dark-gray gradient animation. Harsh shadows are replaced with subtle borders for comfortable night reading.
- **Full Internationalization**: Seamless switching between Chinese and English, with auto-adapted menus, links, and UI text.

### 2. Powerful Writing Assistant (WangScape Writer)
Includes an exclusive `hugo_writer.py` writing assistant that provides a Word-like experience.

- **Office-Style UI**: Familiar "paper-on-desk" writing area with a ribbon toolbar for common actions like previewing and publishing.
- **Bilingual Sync**: Simply input a Chinese title, and the system automatically translates it via API to generate a synchronized English draft.
- **One-Click Preview & Deploy**: No need to remember complex Hugo commands. Start the local server or push updates to GitHub with just a click.

## 🚀 Quick Start

### Prerequisites
- [Hugo Extended](https://gohugo.io/installation/) (Recommended v0.100.0+)
- Python 3.x (For the writing assistant)
- Git

### Installation & Usage

1. **Clone the repository**:
   ```bash
   git clone https://github.com/w2343419-del/WangScape.git
   cd WangScape
   ```

2. **Start the Writing Assistant** (Recommended):
   ```bash
   python hugo_writer.py
   ```
   The browser will automatically open `http://localhost:8080`, and you can start creating immediately.

3. **Run traditionally**:
   ```bash
   hugo server
   ```

## 🛠️ Project Structure

- `content/`: Blog post source code (Markdown)
  - `zh-cn/`: Chinese content
  - `en/`: English content
- `assets/scss/custom.scss`: Core style customizations
- `hugo_writer.py`: Writing assistant core script
- `config/`: Site configuration files (split by language)

## 📝 Writing Guide

It is highly recommended to use **WangScape Writer** for content creation as it automatically handles FrontMatter metadata and file paths.

1. Open the Assistant interface.
2. Click **"New Post"** in the ribbon.
3. Enter the title (Chinese) and categories.
4. Confirm, and the system will auto-create both Chinese and English files.
5. Select the file from the left list to preview.
6. Click **"Deploy"** to publish with one click.

## 📄 License

This project is licensed under the MIT License.
