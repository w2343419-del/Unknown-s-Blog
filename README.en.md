# Hugo Blog Project

<palign="center">
  <img src="https://gohugo.io/images/hugo-logo-wide.svg" alt="Hugo Logo" width="300" />
</p>

> 🚀 A multilingual static blog powered by [hugo-theme-stack](https://github.com/CaiJimmy/hugo-theme-stack), supporting custom layouts, analytics, and a modern UI.

---

## 📁 Directory Structure

- `content/`: Blog content (posts, categories, tags, etc.)
- `config/`: Site configuration (languages, menus, parameters, etc.)
- `theme/`: Theme files
- `public/`: Generated static pages (for deployment)
- `static/`: Static resources (images, styles, etc.)
- `assets/`: Custom styles and scripts

## 🏁 Quick Start

1. Install [Hugo](https://gohugo.io/getting-started/installing/)
2. Clone this repository
3. Run in the project root:
   ```bash
   hugo server -D
   ```
4. Preview locally at: `http://localhost:1313`

## 🎨 Theme & Customization

- Theme: Stack (modern card style, responsive design)
- Multilingual support: Chinese & English
- Customizable sidebar, footer, analytics (e.g. Umami)
- Features: math typesetting, image gallery, search, archives
- Markdown, shortcodes, math supported in posts

## ⚡️ Quickly Generate New Post/Page

Use Hugo commands to quickly create new posts or page templates:

- New post:
  ```bash
  hugo new en/post/your-article/index.md
  ```
  or Chinese:
  ```bash
  hugo new zh-cn/post/你的文章名/index.md
  ```
  This will auto-create a Markdown file with basic front matter in the target directory.

- New page (e.g. archives, links):
  ```bash
  hugo new en/page/archives/index.md
  ```

> Edit the generated file directly, supporting custom categories, tags, summary, etc.

## 🐞 Debugging & Development

- Local live preview (recommended for development/debugging):
  ```bash
  hugo server -D
  ```
  - Watches file changes and auto-refreshes browser
  - `-D` shows draft posts
  - Default address: `http://localhost:1313`

- Check config/content errors:
  - If Hugo reports errors, check `config/` files and front matter format
  - Use VS Code or other editors with Markdown/Linter plugins

- Common debugging tips:
  - Comment/uncomment config items to locate issues
  - Use `hugo --verbose` for detailed logs
  - Clean cache/output:
    ```bash
    hugo --cleanDestinationDir
    ```
    Or manually delete `public/` and regenerate

- Theme/layout debugging:
  - Edit files in `layouts/` or `theme/`, then refresh browser
  - Use browser dev tools (F12) to inspect styles and DOM

## 🚚 Deployment

Generate static files:
```bash
hugo
```
Deploy the contents of `public/` to any static hosting platform:
- GitHub Pages
- Vercel
- Netlify
- Tencent Cloud/Aliyun OSS

## 💡 FAQ

- How to add a new post?
  > Create a folder and `index.md` under `content/en/post/` or `content/zh-cn/post/`, refer to existing content.
- How to change theme?
  > Replace the `theme/` directory and specify the theme in `config.toml`.
- How to add custom styles?
  > Write custom CSS in `assets/scss/custom.scss`.

## 🤝 Contributing

Feel free to submit Issues or PRs to improve this blog!
- Bug fixes
- Style optimization
- New features

## 📜 License

MIT License

---

> Powered by [Hugo](https://gohugo.io/), theme [Stack](https://github.com/CaiJimmy/hugo-theme-stack) designed by Jimmy Cai.
