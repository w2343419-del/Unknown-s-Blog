# 静态网站评论系统 - Vercel Serverless方案

## 🎯 方案概述

这是一个专为**GitHub Pages等静态网站托管**设计的评论系统解决方案。

### 特点

✅ **完全免费** - Vercel免费套餐足够个人博客使用  
✅ **无需服务器** - 使用Serverless Functions  
✅ **自动部署** - Git推送后自动更新  
✅ **GitHub Issues存储** - 利用GitHub作为评论数据库  
✅ **审核机制** - 通过标签控制评论显示  
✅ **全球CDN** - Vercel提供高速访问  

### 工作原理

```
用户提交评论
    ↓
前端调用Vercel Serverless API
    ↓
API使用GitHub Token创建Issue (pending标签)
    ↓
你审核Issue，改标签为approved
    ↓
前端从GitHub API读取approved评论
    ↓
评论显示在网站上
```

## 📚 文档索引

### 快速开始

1. **[QUICK_START_VERCEL.md](QUICK_START_VERCEL.md)** - 5分钟快速部署指南
2. **[DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)** - 部署检查清单

### 详细文档

- **[VERCEL_DEPLOYMENT_GUIDE.md](VERCEL_DEPLOYMENT_GUIDE.md)** - Vercel完整部署教程
- **[STATIC_COMMENT_SOLUTIONS.md](STATIC_COMMENT_SOLUTIONS.md)** - 静态网站评论方案对比
- **[comment-api/GITHUB_TOKEN_GUIDE.md](comment-api/GITHUB_TOKEN_GUIDE.md)** - GitHub Token获取指南

### 旧文档（仅供参考）

- `COMMENT_SYSTEM_GUIDE.md` - 原后端服务器方案（已不适用）
- `comment-api/README.md` - 本地Go服务文档（已不适用）

## 🚀 快速部署（3步）

### 第1步：获取GitHub Token

访问：https://github.com/settings/tokens/new

- Note: `Blog Comment API`
- 勾选: `repo` 权限
- 复制Token（`ghp_xxxxxx`）

### 第2步：推送到GitHub

```powershell
cd d:\hugo
git init
git add .
git commit -m "Add Vercel serverless comment system"
git remote add origin https://github.com/你的用户名/仓库名.git
git push -u origin main
```

### 第3步：部署到Vercel

1. 访问：https://vercel.com/new
2. 选择你的仓库
3. 添加环境变量：
   - `GITHUB_TOKEN` = `ghp_你的Token`
   - `HUGO_VERSION` = `0.154.5`
4. 点击 **Deploy**

完成！网站会部署到 `https://your-project.vercel.app`

## 📁 项目结构

```
d:\hugo\
├── api/
│   ├── submit_comment.go    # Vercel Serverless函数
│   └── go.mod               # Go模块配置
├── config/_default/
│   └── params.toml          # Hugo配置（评论设置）
├── layouts/partials/article/
│   └── comments.html        # 评论前端界面
├── vercel.json              # Vercel部署配置
├── QUICK_START_VERCEL.md    # 快速开始指南
├── VERCEL_DEPLOYMENT_GUIDE.md
├── DEPLOYMENT_CHECKLIST.md
└── (其他Hugo文件...)
```

## 🧪 测试评论功能

部署成功后：

1. 访问你的网站
2. 打开任意文章
3. 点击"💬 发表评论"
4. 填写表单提交
5. 查看GitHub Issues验证评论已创建
6. 将Issue标签从`pending`改为`approved`
7. 刷新页面，评论显示

## 🔧 配置说明

### Hugo配置

`config/_default/params.toml`:

```toml
[params]
    # API地址（留空表示同域）
    apiBase = ""
    
    # GitHub仓库配置
    githubCommentsRepo = "w2343419-del/WangScape"
    githubCommentsLabelApproved = "approved"
    githubCommentsLabelPending = "pending"
    githubCommentsLabelComment = "comment"
```

### Vercel环境变量

必需设置：

| 变量名 | 值 | 说明 |
|--------|-----|------|
| `GITHUB_TOKEN` | `ghp_...` | GitHub Personal Access Token |
| `HUGO_VERSION` | `0.154.5` | Hugo版本号 |

## 🌐 自定义域名（可选）

在Vercel项目设置中绑定域名后，更新Hugo配置：

```toml
[params]
    # 如果API和网站在同一域名，留空即可
    apiBase = ""
```

## 💰 成本

**完全免费！**

Vercel免费套餐包含：
- 100GB带宽/月
- Serverless执行时间：100小时/月
- 无限项目和部署

对于个人博客绰绰有余。

## 🔐 安全性

- ✅ GitHub Token存储在Vercel环境变量（加密）
- ✅ CORS配置防止跨域攻击
- ✅ 评论需要审核才能显示（pending → approved）
- ✅ 不在代码中暴露敏感信息

## 📊 vs 其他方案

| 方案 | 优点 | 缺点 | 适用场景 |
|------|------|------|----------|
| **Vercel Serverless** | 免费、快速、保留现有设计 | 需要部署 | ✅ 推荐 |
| GitHub Actions | 完全免费 | 配置复杂 | 高级用户 |
| giscus | 最简单 | 需要用户有GitHub账号 | 技术博客 |
| 第三方服务 | 现成方案 | 可能收费、广告 | 商业网站 |

## 🐛 故障排查

### 问题1：评论提交失败

**检查：**
- Vercel环境变量中GITHUB_TOKEN是否正确
- Token是否有repo权限
- 查看Vercel Functions日志

### 问题2：评论不显示

**原因：** Issue标签仍是`pending`

**解决：** 在GitHub Issues中将标签改为`approved`

### 问题3：部署失败

**检查：**
- `vercel.json` 格式是否正确
- `api/submit_comment.go` 文件是否存在
- 查看Vercel部署日志

## 📞 获取帮助

- **Vercel文档**: https://vercel.com/docs
- **Hugo文档**: https://gohugo.io/documentation/
- **GitHub Issues**: 在仓库中提Issue

## 🎓 进阶功能

- [ ] 添加评论邮件通知
- [ ] 实现评论点赞功能
- [ ] 添加Markdown支持
- [ ] 实现评论搜索
- [ ] 添加评论统计

## 📝 更新日志

### 2026-02-03
- ✅ 创建Vercel Serverless方案
- ✅ 实现GitHub Issues评论存储
- ✅ 添加完整部署文档
- ✅ 前端评论界面优化

## 📄 License

MIT License

---

**开始你的评论系统之旅！** 🚀

如有问题，请查看文档或提Issue。
