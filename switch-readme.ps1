# 一键切换 README 语言脚本

本脚本可在中英文 README 文件间一键切换（重命名），适用于 Windows PowerShell 环境。

## 使用方法

1. 将本脚本保存为 `switch-readme.ps1` 到项目根目录。
2. 在 PowerShell 终端运行：
   ```powershell
   ./switch-readme.ps1 zh   # 切换为中文 README
   ./switch-readme.ps1 en   # 切换为英文 README
   ```

---

```powershell
param(
    [string]$lang = "zh"
)

$zh = "README.md"
$en = "README.en.md"
$tmp = "README.tmp.md"

if ($lang -eq "en") {
    if (Test-Path $zh -and Test-Path $en) {
        Rename-Item $zh $tmp -Force
        Rename-Item $en $zh -Force
        Rename-Item $tmp $en -Force
        Write-Host "已切换为英文版 README (README.md)"
    } else {
        Write-Host "README 文件不存在，无法切换。"
    }
} elseif ($lang -eq "zh") {
    if (Test-Path $zh -and Test-Path $en) {
        # 如果当前是英文版，切回中文版
        Rename-Item $zh $tmp -Force
        Rename-Item $en $zh -Force
        Rename-Item $tmp $en -Force
        Write-Host "已切换为中文版 README (README.md)"
    } else {
        Write-Host "README 文件不存在，无法切换。"
    }
} else {
    Write-Host "参数错误。用法: ./switch-readme.ps1 zh 或 ./switch-readme.ps1 en"
}
```

---

> 脚本会交换 README.md 与 README.en.md 的内容，实现一键切换显示语言。
