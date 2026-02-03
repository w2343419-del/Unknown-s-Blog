# 部署清单

## ✅ 部署前检查

- [ ] 已创建GitHub仓库
- [ ] 已获取GitHub Personal Access Token (`ghp_...`)
- [ ] 已创建Vercel账号（使用GitHub登录）
- [ ] 代码已推送到GitHub

## 📁 必需文件检查

- [ ] `api/submit_comment.go` - Serverless函数
- [ ] `api/go.mod` - Go模块配置
- [ ] `vercel.json` - Vercel配置
- [ ] `config/_default/params.toml` - Hugo配置
- [ ] `layouts/partials/article/comments.html` - 评论界面

## 🚀 Vercel部署步骤

1. [ ] 访问 https://vercel.com/new
2. [ ] 使用GitHub账号登录
3. [ ] 选择Hugo博客仓库
4. [ ] 设置Framework Preset: **Hugo**
5. [ ] 添加环境变量：
   - [ ] `GITHUB_TOKEN` = `ghp_你的Token`
   - [ ] `HUGO_VERSION` = `0.154.5`
6. [ ] 点击 **Deploy**
7. [ ] 等待部署完成（2-3分钟）

## ✅ 部署后验证

- [ ] 访问网站正常（`https://your-project.vercel.app`）
- [ ] 打开任意文章页面
- [ ] 评论表单正常显示
- [ ] 填写测试评论并提交
- [ ] 看到成功提示："✅ 评论提交成功！等待审核..."
- [ ] GitHub Issues中出现新Issue
- [ ] Issue标签包含：`comment` 和 `pending`

## 🔧 审核评论测试

- [ ] 访问 https://github.com/w2343419-del/WangScape/issues
- [ ] 找到测试评论Issue
- [ ] 将标签从 `pending` 改为 `approved`
- [ ] 刷新博客页面
- [ ] 评论正常显示

## 🎯 可选配置

- [ ] 绑定自定义域名
- [ ] 配置自定义构建命令
- [ ] 设置Webhook通知

## 📊 部署信息记录

| 项目 | 信息 |
|------|------|
| Vercel项目名 | ________________ |
| 部署URL | https://________________.vercel.app |
| GitHub仓库 | https://github.com/________________/________________ |
| 部署时间 | ________________ |

## 🐛 遇到问题？

查看故障排查指南：
- [ ] 阅读 `VERCEL_DEPLOYMENT_GUIDE.md`
- [ ] 检查Vercel部署日志
- [ ] 检查Serverless函数日志
- [ ] 验证环境变量设置

---

**部署成功后，记得删除测试评论！** ✨
