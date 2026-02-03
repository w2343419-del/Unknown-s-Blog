@echo off
echo ========================================
echo   评论API服务启动脚本
echo ========================================
echo.

cd /d "%~dp0comment-api"

REM 检查是否已构建
if not exist "comment-api.exe" (
    echo 首次运行，正在构建程序...
    go build -o comment-api.exe main.go
    if errorlevel 1 (
        echo 构建失败！请检查Go环境是否正确安装。
        pause
        exit /b 1
    )
    echo 构建成功！
    echo.
)

REM 设置环境变量（请替换为你的实际值）
echo 正在设置环境变量...
set GITHUB_TOKEN=ghp_YOUR_GITHUB_TOKEN_HERE
set CORS_ORIGIN=http://localhost:1313
set PORT=8080

echo.
echo 配置信息:
echo - API端口: %PORT%
echo - CORS源: %CORS_ORIGIN%
echo - GitHub Token: %GITHUB_TOKEN:~0,10%...
echo.

echo 启动评论API服务...
echo 按 Ctrl+C 可以停止服务
echo.
comment-api.exe

pause
