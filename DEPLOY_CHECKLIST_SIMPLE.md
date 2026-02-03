# 评论系统部署检查清单

## ✅ 当前配置状态

你的评论系统已经配置完成！工作流程如下：

### 📝 评论提交流程

```
访客在网站填写评论
    ↓
点击"提交评论"（不跳转，留在当前页面）
    ↓
前端调用Vercel API (/api/submit_comment)
    ↓
API使用GitHub Token创建Issue (带pending标签)
    ↓
网站显示："✅ 评论提交成功！等待审核后将显示在页面上。"
    ↓
你在GitHub审核Issue，改标签为approved
    ↓
评论自动显示在网站上
```

## 🚀 部署步骤

### 第1步：在Vercel添加环境变量

由于你已经有Vercel项目了，只需添加环境变量：

1. 访问：https://vercel.com/dashboard
2. 选择你的项目
3. 进入 **Settings** → **Environment Variables**
4. 添加：

| Name | Value |
|------|-------|
| `GITHUB_TOKEN` | `ghp_你的GitHub_Token` |

> 如何获取Token：访问 https://github.com/settings/tokens/new
> - Note: `Blog Comment API`
> - 勾选: `repo` 权限
> - 复制生成的Token

### 第2步：推送代码到GitHub

```powershell
cd d:\hugo

# 添加新文件
git add api/
git add layouts/partials/article/comments.html
git add config/_default/params.toml
git add vercel.json

# 提交
git commit -m "Add comment system with Vercel API"

# 推送
git push
```

Vercel会自动检测到更新并重新部署。

### 第3步：等待部署完成

访问 Vercel Dashboard 查看部署进度（通常1-2分钟）。

### 第4步：测试评论功能

1. 访问你的网站
2. 打开任意文章
3. 点击"💬 发表评论"
4. 填写测试评论
5. 点击提交
6. 应该看到："✅ 评论提交成功！等待审核后将显示在页面上。"
7. **页面不会跳转，保持在当前位置**

### 第5步：审核评论

1. 访问：https://github.com/w2343419-del/WangScape/issues
2. 找到 `[Comment]` 开头的Issue
3. 将标签从 `pending` 改为 `approved`
4. 刷新博客页面，评论就显示了

## 📁 已配置的文件

- ✅ `api/submit_comment.go` - Vercel Serverless函数
- ✅ `api/go.mod` - Go模块配置
- ✅ `vercel.json` - Vercel配置
- ✅ `layouts/partials/article/comments.html` - 评论前端
- ✅ `config/_default/params.toml` - 评论配置

## 🔍 验证配置

### 检查Hugo配置

确认 `config/_default/params.toml` 包含：

```toml
[params]
    apiBase = ""  # 空值表示使用同域名API
    githubCommentsRepo = "w2343419-del/WangScape"
    githubCommentsLabelApproved = "approved"
    githubCommentsLabelPending = "pending"
    githubCommentsLabelComment = "comment"
```

### 检查Vercel配置

确认 `vercel.json` 存在并包含API路由配置。

### 检查API文件

确认 `api/submit_comment.go` 文件存在。

## ✨ 特性

- ✅ 用户留在当前页面，无需跳转
- ✅ 评论自动提交到GitHub Issues
- ✅ 审核机制（pending → approved）
- ✅ 实时显示已审核的评论
- ✅ 支持评论回复
- ✅ 支持多语言（中英文）

## 🐛 常见问题

**Q: 点击提交后显示网络错误？**

A: 检查：
- Vercel环境变量中GITHUB_TOKEN是否正确设置
- Token是否有repo权限
- 查看Vercel Functions日志

**Q: 评论提交成功但不显示？**

A: Issue标签还是pending，需要在GitHub改为approved

**Q: 怎么查看Vercel部署日志？**

A: 访问 https://vercel.com/dashboard → 选择项目 → 查看最新部署

## 📞 下一步

1. [ ] 在Vercel添加GITHUB_TOKEN环境变量
2. [ ] 推送代码到GitHub
3. [ ] 等待Vercel自动部署
4. [ ] 测试评论功能

---

**准备好了吗？开始第1步：在Vercel添加环境变量！** 🚀
