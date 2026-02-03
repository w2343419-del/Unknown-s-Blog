# Vercel部署 - 快速开始

## 🚀 一键部署到Vercel

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new)

## 📋 部署前准备

### 1. GitHub Token

访问：https://github.com/settings/tokens/new

- **Note**: `Blog Comment API`
- **Scopes**: 勾选 `repo`
- 复制生成的Token（格式：`ghp_xxxxxx`）

### 2. 推送代码到GitHub

```powershell
cd d:\hugo

# 初始化Git仓库（如果还没有）
git init

# 添加所有文件
git add .

# 提交
git commit -m "Add Vercel serverless comment system"

# 关联远程仓库（替换为你的仓库地址）
git remote add origin https://github.com/你的用户名/仓库名.git

# 推送
git push -u origin main
```

## 🌐 Vercel部署步骤

### 方法1: 通过网页部署（推荐）

1. **访问Vercel**
   - 打开：https://vercel.com/new
   - 使用GitHub账号登录

2. **导入仓库**
   - 点击 **Import Git Repository**
   - 选择你的Hugo博客仓库
   - 点击 **Import**

3. **配置项目**
   
   **Framework Preset**: Hugo
   
   **Environment Variables**（点击展开并添加）:
   ```
   GITHUB_TOKEN = ghp_你的实际Token
   HUGO_VERSION = 0.154.5
   ```

4. **部署**
   - 点击 **Deploy**
   - 等待2-3分钟

5. **完成！**
   - 你会看到：`🎉 Your project is ready!`
   - 网站地址：`https://your-project.vercel.app`

### 方法2: 使用Vercel CLI

```powershell
# 安装Vercel CLI
npm i -g vercel

# 登录
vercel login

# 部署
cd d:\hugo
vercel

# 按照提示操作
```

## ✅ 部署后配置

### 更新Hugo配置

如果你的Vercel项目地址是 `https://my-blog.vercel.app`

编辑 `config/_default/params.toml`:

```toml
[params]
    # 留空即可（API和网站在同一域名）
    apiBase = ""
```

### 测试评论功能

1. 访问：`https://your-project.vercel.app`
2. 打开任意文章
3. 点击"发表评论"
4. 填写并提交
5. 检查GitHub Issues是否创建成功

## 🎯 环境变量设置

在Vercel Dashboard设置环境变量：

1. 进入项目 → **Settings** → **Environment Variables**
2. 添加：

| Name | Value | Environment |
|------|-------|-------------|
| `GITHUB_TOKEN` | `ghp_你的Token` | Production, Preview, Development |
| `HUGO_VERSION` | `0.154.5` | Production, Preview, Development |

## 🔄 自动部署

配置完成后，每次推送到GitHub，Vercel会自动重新部署：

```powershell
git add .
git commit -m "Update content"
git push
```

Vercel会自动：
1. 检测到新的push
2. 运行Hugo构建
3. 部署Serverless函数
4. 更新网站

## 🌍 绑定自定义域名（可选）

1. Vercel项目 → **Settings** → **Domains**
2. 输入域名：`blog.yourdomain.com`
3. 配置DNS记录：
   ```
   类型: CNAME
   名称: blog
   值: cname.vercel-dns.com
   ```
4. 等待生效

## 📊 监控

查看部署状态和日志：
- Dashboard: https://vercel.com/dashboard
- 选择项目查看详细信息

## 🐛 常见问题

**Q: 部署失败怎么办？**

A: 查看部署日志，常见原因：
- Hugo版本不匹配
- 环境变量未设置
- vercel.json配置错误

**Q: API返回404？**

A: 确保：
- `api/submit_comment.go` 文件存在
- `vercel.json` 配置正确
- 重新部署项目

**Q: 评论提交失败？**

A: 检查：
- GITHUB_TOKEN环境变量是否正确
- Token是否有repo权限
- 查看Vercel函数日志

## 📞 获取帮助

- Vercel文档：https://vercel.com/docs
- GitHub Issues：https://github.com/vercel/vercel/issues

---

**准备好了吗？开始部署！** 🎉
