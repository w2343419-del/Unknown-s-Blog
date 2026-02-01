## 快速故障排除清单

如果修复后仍有问题，请按以下步骤检查：

### 问题：头像仍然无法显示

**检查项**：
1. [ ] 清除浏览器缓存 (Ctrl+Shift+Delete)
2. [ ] 强制刷新页面 (Ctrl+F5)
3. [ ] 检查图片文件是否存在：
   ```
   /img/avatar.png 或 /static/img/avatar.png
   ```
4. [ ] 在浏览器控制台检查是否有 404 错误
5. [ ] 检查 CSS 是否成功编译：
   ```
   public/scss/ 中是否有 style.min.*.css 文件
   ```

### 问题：文章仍然显示不全

**检查项**：
1. [ ] 检查 `.main` 的实际计算高度（F12 开发者工具）
2. [ ] 检查是否有其他 CSS 文件覆盖了 custom.scss
3. [ ] 查看是否有浏览器插件影响
4. [ ] 尝试在隐私/隐身模式下打开页面

### 问题：加载时仍有跳动

**检查项**：
1. [ ] 打开 Chrome DevTools Performance 选项卡录制加载过程
2. [ ] 查看是否有频繁的重排（Layout Thrashing）
3. [ ] 检查网络速度（模拟较慢的连接以观察）
4. [ ] 查看是否有 JavaScript 导致的重排

### 问题：响应式设计不工作

**检查项**：
1. [ ] 检查移动端视口元素：
   ```html
   <meta name="viewport" content="width=device-width, initial-scale=1.0">
   ```
2. [ ] 在 DevTools 中测试不同的设备大小
3. [ ] 检查媒体查询是否正确编译
4. [ ] 清除浏览器缓存后重试

### 性能诊断

**打开 Chrome DevTools 性能分析**：
1. 打开 F12 → Performance 标签
2. 点击录制按钮
3. 刷新页面
4. 停止录制
5. 查看是否有长的黄色/红色任务（表示性能问题）

### Hugo 构建问题

如果上述检查都没有问题，可能是 Hugo 构建问题：

```bash
# 清理生成文件
rm -r resources/_gen
rm -r public

# 重新生成
hugo mod get -u
hugo

# 本地测试
hugo server --enableGitInfo
```

### CSS 验证

在 Hugo 模板中强制重新加载 CSS：
```html
<!-- 检查 CSS 文件是否包含了新的修改 -->
<link rel="stylesheet" href="/scss/custom.css?v={{ now.Unix }}">
```

### 最后的手段

如果以上都不管用，请：
1. 在 GitHub 上创建 Issue，附上浏览器控制台的完整错误日志
2. 提供屏幕截图说明问题
3. 说明浏览器版本和操作系统
4. 提供 Hugo 版本号：`hugo version`
