# Vercel部署完整指南

## 什么是Vercel？

Vercel是一个现代化的网站托管平台，专为静态网站和Serverless函数设计。它：
- ✅ **完全免费**（个人项目）
- ✅ 自动从GitHub部署
- ✅ 支持Hugo静态网站
- ✅ 支持Serverless Functions（API后端）
- ✅ 全球CDN，速度极快
- ✅ 免费HTTPS证书

## 🎯 部署后的效果

- 网站地址：`https://你的项目名.vercel.app`
- API地址：`https://你的项目名.vercel.app/api/submit_comment`
- 可以绑定自定义域名

## 📋 准备工作

### 1. 创建Vercel账号

访问：https://vercel.com
使用GitHub账号登录（推荐）

### 2. 确保项目已推送到GitHub

```powershell
# 如果还没有推送到GitHub
cd d:\hugo
git init
git add .
git commit -m "Initial commit with comment system"

# 在GitHub创建仓库后
git remote add origin https://github.com/你的用户名/你的仓库名.git
git push -u origin main
```

## 🚀 部署步骤

### 步骤1: 导入项目到Vercel

1. 访问：https://vercel.com/new
2. 点击 **Import Git Repository**
3. 选择你的Hugo博客仓库
4. 点击 **Import**

### 步骤2: 配置项目

**Framework Preset**: 选择 `Hugo`

**Build Settings**:
- Build Command: `hugo --gc --minify`
- Output Directory: `public`
- Install Command: `yum install -y golang || true`

**Environment Variables** (环境变量):

点击 **Environment Variables** 添加：

| Name | Value |
|------|-------|
| `GITHUB_TOKEN` | `ghp_你的GitHub_Token` |
| `HUGO_VERSION` | `0.154.5` |

### 步骤3: 部署

点击 **Deploy** 按钮，等待2-3分钟。

### 步骤4: 获取部署地址

部署成功后，你会看到：
```
🎉 Your project is ready!
https://your-project.vercel.app
```

### 步骤5: 更新Hugo配置

编辑 `config/_default/params.toml`：

```toml
[params]
    # 生产环境：使用Vercel域名
    apiBase = "https://your-project.vercel.app"
    
    # 或者使用环境变量（推荐）
    # apiBase = ""  # 空值表示使用同域名
```

### 步骤6: 推送更新

```powershell
git add config/_default/params.toml
git commit -m "Update API base URL"
git push
```

Vercel会自动检测到Git推送并重新部署。

## 📁 项目文件结构

确保你的项目包含以下文件：

```
d:\hugo\
├── api/
│   └── submit_comment.go    # ← Serverless函数
├── config/
│   └── _default/
│       └── params.toml
├── layouts/
│   └── partials/
│       └── article/
│           └── comments.html
├── vercel.json              # ← Vercel配置
└── (其他Hugo文件)
```

## 🔧 Vercel配置文件

我已经为你创建了 `vercel.json` 和 `api/submit_comment.go`。

## 🧪 测试部署

部署成功后：

1. 访问你的网站：`https://your-project.vercel.app`
2. 打开任意文章
3. 点击"发表评论"
4. 填写表单并提交
5. 检查GitHub仓库的Issues

## 🌐 绑定自定义域名（可选）

### 如果你有自己的域名：

1. 在Vercel项目页面点击 **Settings** → **Domains**
2. 输入你的域名，如：`blog.yourdomain.com`
3. 按照提示配置DNS记录：
   - 类型：`CNAME`
   - 名称：`blog`（或 `@` 如果是根域名）
   - 值：`cname.vercel-dns.com`
4. 等待DNS生效（几分钟到几小时）
5. Vercel自动配置HTTPS证书

### 更新Hugo配置：

```toml
[params]
    apiBase = "https://blog.yourdomain.com"
```

## 📊 监控和日志

### 查看部署日志：

1. 访问：https://vercel.com/dashboard
2. 选择你的项目
3. 点击某次部署查看详细日志

### 查看Serverless函数日志：

1. 项目页面 → **Functions**
2. 点击函数名查看调用日志和错误

## 🔍 故障排查

### 问题1: 部署失败

**解决方案：**
- 检查 `vercel.json` 格式是否正确
- 确保 `HUGO_VERSION` 环境变量设置正确
- 查看部署日志了解具体错误

### 问题2: API返回404

**可能原因：**
- `api/submit_comment.go` 文件位置不对
- 文件名错误（必须是 `.go` 结尾）

**解决方案：**
确保文件在项目根目录的 `api/` 文件夹中。

### 问题3: GitHub Token错误

**解决方案：**
1. 在Vercel项目 → **Settings** → **Environment Variables**
2. 编辑 `GITHUB_TOKEN`
3. 重新部署

### 问题4: CORS错误

Vercel的Serverless函数已经配置了CORS，应该不会有问题。如果还有错误，检查：
- `api/submit_comment.go` 中的CORS头设置
- 浏览器控制台的具体错误信息

## 🔐 安全建议

1. **GitHub Token安全**
   - ✅ 在Vercel环境变量中设置（已加密）
   - ❌ 不要提交到Git仓库
   - ✅ 定期轮换Token

2. **CORS配置**
   - 生产环境建议限制允许的域名
   - 可以在 `api/submit_comment.go` 中修改

## 📈 性能优化

Vercel自动提供：
- ✅ 全球CDN（边缘缓存）
- ✅ 自动图片优化
- ✅ HTTP/2和HTTP/3
- ✅ Brotli压缩

无需额外配置！

## 💰 成本

**免费套餐包含：**
- 100GB带宽/月
- Serverless函数执行时间：100小时/月
- 无限项目数

对于个人博客，完全够用！

## 🎓 进阶功能

### 自动预览部署

每次push到GitHub，Vercel会自动创建预览部署，可以在合并前查看效果。

### 分析和监控

Vercel提供：
- 访问量统计
- Core Web Vitals性能指标
- 函数调用统计

### CI/CD集成

可以配置GitHub Actions与Vercel集成，实现更复杂的CI/CD流程。

## 📞 获取帮助

- Vercel文档：https://vercel.com/docs
- Hugo on Vercel：https://vercel.com/guides/deploying-hugo-with-vercel
- Vercel社区：https://github.com/vercel/vercel/discussions

---

## ✅ 检查清单

部署前确认：

- [ ] GitHub仓库已创建并推送代码
- [ ] `api/submit_comment.go` 文件存在
- [ ] `vercel.json` 配置正确
- [ ] 已获取GitHub Personal Access Token
- [ ] Vercel账号已创建

部署后确认：

- [ ] 网站可以正常访问
- [ ] 评论表单可以正常显示
- [ ] 提交评论后有成功提示
- [ ] GitHub Issues中出现了新的评论Issue
- [ ] 将Issue标签改为approved后，评论显示在网站上

---

**准备好了吗？让我们开始部署！** 🚀
