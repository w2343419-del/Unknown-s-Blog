# 评论API服务

这是一个简单的Go后端服务，用于接收评论并将其提交到GitHub Issues。

## 功能特性

- 接收前端评论提交请求
- 自动创建GitHub Issue
- 支持CORS跨域请求
- 简单易部署

## 快速开始

### 1. 创建GitHub Personal Access Token

1. 访问 GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
2. 点击 "Generate new token (classic)"
3. 设置Token名称，例如: "Blog Comments API"
4. 选择权限: 勾选 `repo` (完整的仓库访问权限)
5. 点击 "Generate token" 并复制生成的token

### 2. 配置环境变量

创建 `.env` 文件（从 `.env.example` 复制）:

```bash
cp .env.example .env
```

编辑 `.env` 文件，填入你的GitHub Token:

```env
GITHUB_TOKEN=ghp_your_actual_token_here
CORS_ORIGIN=http://localhost:1313
PORT=8080
```

### 3. 运行服务

**开发环境运行：**

```bash
# 在 comment-api 目录下
go run main.go
```

**构建可执行文件：**

```bash
go build -o comment-api.exe main.go
```

然后运行：

```bash
# Windows
.\comment-api.exe

# Linux/Mac
./comment-api
```

### 4. 使用Windows批处理脚本运行

创建 `start-comment-api.bat`:

```batch
@echo off
cd /d "%~dp0comment-api"
set GITHUB_TOKEN=your_token_here
set CORS_ORIGIN=http://localhost:1313
set PORT=8080
comment-api.exe
pause
```

### 5. 配置Hugo网站

编辑 `config/_default/params.toml`:

```toml
[params]
    # 评论API基础地址
    apiBase = "http://localhost:8080"
    
    # GitHub仓库配置保持不变
    githubCommentsRepo = "w2343419-del/WangScape"
    githubCommentsLabelApproved = "approved"
    githubCommentsLabelPending = "pending"
    githubCommentsLabelComment = "comment"
```

## 部署到生产环境

### 方案1: 使用VPS或云服务器

1. 将代码上传到服务器
2. 设置环境变量
3. 运行服务（建议使用systemd或supervisor管理）

### 方案2: 使用Docker

创建 `Dockerfile`:

```dockerfile
FROM golang:1.22-alpine AS builder
WORKDIR /app
COPY . .
RUN go build -o comment-api main.go

FROM alpine:latest
WORKDIR /app
COPY --from=builder /app/comment-api .
EXPOSE 8080
CMD ["./comment-api"]
```

运行：

```bash
docker build -t comment-api .
docker run -p 8080:8080 \
  -e GITHUB_TOKEN=your_token \
  -e CORS_ORIGIN=https://yourdomain.com \
  comment-api
```

### 方案3: 使用Serverless平台

- **Vercel**: 可以使用Vercel Functions
- **Railway**: 直接部署Go应用
- **Fly.io**: 容器化部署

## API文档

### POST /api/submit_comment

提交评论到GitHub Issues。

**请求体：**

```json
{
  "post_path": "zh-cn/post/your-post/index.md",
  "post_title": "文章标题",
  "author": "用户名",
  "email": "user@example.com",
  "content": "评论内容",
  "parent_id": "",
  "use_github": true,
  "github_repo": "owner/repo",
  "github_labels": ["comment", "pending"]
}
```

**响应：**

成功:
```json
{
  "success": true,
  "message": "评论已提交到GitHub，等待审核"
}
```

失败:
```json
{
  "success": false,
  "message": "错误信息"
}
```

### GET /health

健康检查端点。

**响应：**

```json
{
  "status": "ok",
  "time": "2026-02-03T12:00:00Z"
}
```

## 安全建议

1. **生产环境必须设置CORS_ORIGIN**为你的实际域名
2. **不要将GITHUB_TOKEN提交到代码仓库**
3. 使用HTTPS部署API服务
4. 定期轮换GitHub Token
5. 考虑添加速率限制防止滥用

## 故障排查

**评论提交失败？**

1. 检查GitHub Token是否正确配置
2. 确认Token有`repo`权限
3. 查看服务器日志: `go run main.go` 会输出详细日志
4. 确认仓库名称格式正确: `owner/repo`
5. 检查CORS配置是否正确

**CORS错误？**

确保 `CORS_ORIGIN` 设置为你的Hugo网站URL（开发环境: `http://localhost:1313`）
