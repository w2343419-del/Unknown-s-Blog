@echo off
chcp 65001 >nul
echo ========================================
echo   评论系统测试脚本
echo ========================================
echo.

REM 测试1: 检查API服务是否运行
echo [1/3] 检查API服务...
powershell -Command "try { $response = Invoke-WebRequest -Uri 'http://localhost:8080/health' -TimeoutSec 2; if ($response.StatusCode -eq 200) { Write-Host '✓ API服务正常运行' -ForegroundColor Green } else { Write-Host '✗ API服务异常' -ForegroundColor Red } } catch { Write-Host '✗ API服务未启动，请先运行 start-comment-api.bat' -ForegroundColor Yellow }"
echo.

REM 测试2: 检查Hugo配置
echo [2/3] 检查Hugo配置...
findstr /C:"apiBase" config\_default\params.toml >nul
if %errorlevel%==0 (
    echo ✓ Hugo配置文件存在
    findstr /C:"apiBase" config\_default\params.toml
) else (
    echo ✗ 配置文件异常
)
echo.

REM 测试3: 检查Hugo服务器
echo [3/3] 检查Hugo服务器...
powershell -Command "try { $response = Invoke-WebRequest -Uri 'http://localhost:1313/WangScape/' -TimeoutSec 2; if ($response.StatusCode -eq 200) { Write-Host '✓ Hugo服务器正常运行' -ForegroundColor Green } else { Write-Host '✗ Hugo服务器异常' -ForegroundColor Red } } catch { Write-Host '✗ Hugo服务器未启动，请运行: hugo server -D' -ForegroundColor Yellow }"
echo.

echo ========================================
echo   测试完成！
echo ========================================
echo.
echo 下一步操作：
echo 1. 访问: http://localhost:1313/WangScape/
echo 2. 打开任意文章
echo 3. 点击 "发表评论" 测试功能
echo.

pause
