# 如何获取 GitHub Personal Access Token

## 步骤1: 访问GitHub设置页面

1. 登录你的GitHub账号
2. 点击右上角头像 → **Settings**（设置）
3. 在左侧菜单滚动到底部，点击 **Developer settings**（开发者设置）

## 步骤2: 创建新Token

1. 点击左侧菜单中的 **Personal access tokens** → **Tokens (classic)**
2. 点击右上角的 **Generate new token** → **Generate new token (classic)**

## 步骤3: 配置Token

填写以下信息：

### Note (备注)
```
Blog Comment API
```

### Expiration (过期时间)
建议选择: **No expiration** (永不过期) 或 **90 days** (90天)

### Select scopes (选择权限)

**必须勾选以下权限：**

- ✅ **repo** (完整的仓库访问权限)
  - ✅ repo:status
  - ✅ repo_deployment
  - ✅ public_repo
  - ✅ repo:invite
  - ✅ security_events

这个权限允许API代表你创建和管理Issues。

## 步骤4: 生成并保存Token

1. 点击页面底部的 **Generate token** (生成token)
2. **重要**: 复制生成的token（格式类似：`ghp_xxxxxxxxxxxxxxxxxx`）
3. **警告**: Token只会显示一次，务必立即保存！

## 步骤5: 配置到你的项目

### 方法1: 使用批处理脚本

编辑 `start-comment-api.bat` 文件，替换这一行：

```batch
set GITHUB_TOKEN=ghp_YOUR_GITHUB_TOKEN_HERE
```

改为：

```batch
set GITHUB_TOKEN=ghp_你刚才复制的实际token
```

### 方法2: 使用环境变量文件

在 `comment-api` 目录下创建 `.env` 文件：

```env
GITHUB_TOKEN=ghp_你刚才复制的实际token
CORS_ORIGIN=http://localhost:1313
PORT=8080
```

然后使用以下命令运行：

```bash
# 需要先安装 dotenv 工具，或者直接在代码中读取.env
# 简单方式是使用批处理脚本
```

## 安全注意事项

⚠️ **重要安全提醒：**

1. **不要将Token提交到Git仓库**
   - `.env` 文件已添加到 `.gitignore`
   - 不要在公开的代码中硬编码Token

2. **定期轮换Token**
   - 建议每3-6个月更换一次Token
   - 如果Token泄露，立即删除并重新生成

3. **最小权限原则**
   - 只授予必要的权限（repo权限）
   - 不要授予不需要的其他权限

4. **生产环境部署**
   - 使用环境变量而不是硬编码
   - 使用密钥管理服务（如AWS Secrets Manager）

## 验证Token是否有效

可以使用以下命令测试Token：

```bash
curl -H "Authorization: Bearer ghp_你的token" https://api.github.com/user
```

如果返回你的GitHub用户信息，说明Token有效。

## 如果忘记保存Token

如果你忘记复制Token，需要重新生成：

1. 回到 **Personal access tokens** 页面
2. 找到刚才创建的Token
3. 点击 **Regenerate token** 或删除后重新创建

## 快速链接

直接访问: https://github.com/settings/tokens
