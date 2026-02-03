# 评论系统完整使用指南

## 🎯 系统架构

你的博客评论系统现在采用以下架构：

1. **前端**：Hugo静态网站，包含评论提交表单
2. **后端API**：Go语言编写的评论API服务
3. **存储**：GitHub Issues作为评论数据库
4. **展示**：从GitHub API读取已批准的评论并显示

## 📋 快速开始（3步配置）

### 步骤1: 获取GitHub Token

访问：https://github.com/settings/tokens

1. 点击 **Generate new token (classic)**
2. Note填写：`Blog Comment API`
3. 勾选权限：`repo` (完整仓库访问)
4. 点击生成并**立即复制Token**（格式：`ghp_xxxxxx...`）

> 详细步骤请查看：[GITHUB_TOKEN_GUIDE.md](comment-api/GITHUB_TOKEN_GUIDE.md)

### 步骤2: 配置并启动API服务

**编辑 `start-comment-api.bat` 文件：**

```batch
set GITHUB_TOKEN=ghp_你的实际token
set CORS_ORIGIN=http://localhost:1313
set PORT=8080
```

**运行服务：**

双击 `start-comment-api.bat` 或在PowerShell中运行：

```powershell
.\start-comment-api.bat
```

你应该看到：

```
评论API服务启动在端口 8080
```

### 步骤3: 启动Hugo网站

在另一个终端运行：

```powershell
hugo server -D
```

访问：http://localhost:1313/WangScape/

## ✅ 测试评论功能

1. 访问任意博客文章
2. 点击 **💬 发表评论** 按钮
3. 填写表单：
   - 姓名：`测试用户`
   - 邮箱：`test@example.com`
   - 评论内容：`这是一条测试评论`
4. 点击 **提交评论**
5. 如果看到 "✅ 评论提交成功！等待审核后将显示在页面上。" 说明成功！

## 📝 审核评论

评论提交后会在你的GitHub仓库中创建一个Issue：

1. 访问：https://github.com/w2343419-del/WangScape/issues
2. 找到标题为 `[Comment] 文章标题` 的Issue
3. 查看评论内容，确认无误
4. **重要**：将Issue的标签从 `pending` 改为 `approved`
5. 刷新博客页面，评论就会显示出来！

## 🔧 工作流程详解

```
用户填写评论表单
       ↓
前端提交到API服务 (localhost:8080/api/submit_comment)
       ↓
API使用GitHub Token创建Issue (带pending标签)
       ↓
你审核Issue，将标签改为approved
       ↓
前端从GitHub API读取approved标签的Issue
       ↓
评论显示在网站上
```

## 🚀 生产环境部署

### 选项1: VPS/云服务器部署

1. **编译Go程序：**

```bash
cd comment-api
go build -o comment-api main.go
```

2. **创建systemd服务** (`/etc/systemd/system/comment-api.service`):

```ini
[Unit]
Description=Blog Comment API Service
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/var/www/comment-api
Environment="GITHUB_TOKEN=ghp_你的token"
Environment="CORS_ORIGIN=https://yourdomain.com"
Environment="PORT=8080"
ExecStart=/var/www/comment-api/comment-api
Restart=always

[Install]
WantedBy=multi-user.target
```

3. **启动服务：**

```bash
sudo systemctl enable comment-api
sudo systemctl start comment-api
```

4. **配置Nginx反向代理：**

```nginx
server {
    listen 80;
    server_name api.yourdomain.com;

    location /api/ {
        proxy_pass http://localhost:8080/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

5. **更新Hugo配置** (`config/_default/params.toml`):

```toml
[params]
    apiBase = "https://api.yourdomain.com"
```

### 选项2: Docker部署

1. **构建镜像：**

```bash
cd comment-api
docker build -t comment-api .
```

2. **运行容器：**

```bash
docker run -d \
  --name comment-api \
  -p 8080:8080 \
  -e GITHUB_TOKEN=ghp_你的token \
  -e CORS_ORIGIN=https://yourdomain.com \
  comment-api
```

### 选项3: Railway/Fly.io/Vercel等Serverless平台

这些平台通常支持直接从GitHub部署，具体步骤请参考各平台文档。

## 🛠️ 故障排查

### 问题1: 提交评论后显示"网络错误"

**检查清单：**

- [ ] API服务是否正在运行？（访问 http://localhost:8080/health）
- [ ] Hugo配置中的`apiBase`是否正确？
- [ ] 浏览器控制台是否有CORS错误？

**解决方案：**

```powershell
# 检查API服务
Invoke-WebRequest http://localhost:8080/health

# 应该返回：{"status":"ok","time":"..."}
```

### 问题2: API返回"提交到GitHub失败"

**可能原因：**

1. GitHub Token无效或过期
2. Token权限不足（需要repo权限）
3. 仓库名称配置错误

**解决方案：**

```bash
# 测试Token是否有效
curl -H "Authorization: Bearer ghp_你的token" https://api.github.com/user

# 检查仓库配置
# 格式必须是: owner/repo
# 正确: w2343419-del/WangScape
# 错误: https://github.com/w2343419-del/WangScape
```

### 问题3: 评论提交成功但不显示

**原因：** Issue标签还是`pending`，需要改为`approved`

**解决方案：**

1. 访问GitHub仓库的Issues页面
2. 找到对应的评论Issue
3. 将标签从`pending`改为`approved`
4. 刷新博客页面

### 问题4: CORS错误

**错误信息：** `Access to fetch at ... has been blocked by CORS policy`

**解决方案：**

确保API服务的`CORS_ORIGIN`设置正确：

- 开发环境：`http://localhost:1313`
- 生产环境：`https://yourdomain.com`

## 📊 监控与日志

API服务会在控制台输出日志：

```
2026/02/03 18:00:00 评论API服务器启动在端口 8080
2026/02/03 18:05:23 成功创建GitHub Issue - 作者: 测试用户, 文章: zh-cn/post/...
```

建议在生产环境使用日志管理工具收集日志。

## 🔐 安全最佳实践

1. **保护GitHub Token**
   - 使用环境变量，不要硬编码
   - 定期轮换Token
   - 不要提交到Git仓库

2. **限制CORS**
   - 生产环境必须设置具体域名
   - 不要使用通配符`*`

3. **添加速率限制**
   - 防止恶意提交
   - 可以使用中间件限制每IP的请求频率

4. **内容过滤**
   - 考虑添加敏感词过滤
   - 可以在API中添加黑名单检查

## 📚 文件结构

```
d:\hugo\
├── comment-api/              # API服务代码
│   ├── main.go              # 主程序
│   ├── go.mod               # Go模块文件
│   ├── .env.example         # 环境变量示例
│   ├── .gitignore           # Git忽略文件
│   ├── README.md            # API文档
│   └── GITHUB_TOKEN_GUIDE.md # Token获取指南
├── config/_default/
│   └── params.toml          # Hugo配置（含apiBase）
├── layouts/partials/article/
│   └── comments.html        # 评论前端代码
├── start-comment-api.bat    # Windows启动脚本
└── COMMENT_SYSTEM_GUIDE.md  # 本文档
```

## 🎓 进阶功能

### 添加邮件通知

当有新评论时发送邮件通知，可以修改API代码添加SMTP功能。

### 添加图片上传

目前代码中保留了图片上传的前端界面，你可以：

1. 添加图片存储服务（如S3、七牛云等）
2. 在API中实现`/api/upload_comment_image`端点
3. 将图片URL存储到GitHub Issue中

### 添加评论回复功能

当前已支持回复功能，回复的评论会作为子评论显示。

## 💡 常见问题

**Q: 为什么要用GitHub Issues存储评论？**

A: 对于静态网站，这是一个免费、可靠的解决方案。你可以利用GitHub的Issue管理功能来审核和管理评论。

**Q: 评论审核流程能自动化吗？**

A: 可以，你可以设置GitHub Actions，在Issue创建时自动检查内容，如果符合条件就自动添加`approved`标签。

**Q: 可以换成其他存储方式吗？**

A: 可以，修改API代码，将评论存储到数据库或其他服务即可。

## 📞 获取帮助

- API服务文档：`comment-api/README.md`
- GitHub Token指南：`comment-api/GITHUB_TOKEN_GUIDE.md`
- 前端代码：`layouts/partials/article/comments.html`

---

**祝你使用愉快！如有问题，欢迎提Issue。** 🎉
