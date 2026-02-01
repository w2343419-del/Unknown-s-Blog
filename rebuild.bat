@echo off
REM 清理 Hugo 生成的文件
echo Cleaning Hugo build artifacts...
if exist public rmdir /s /q public
if exist resources\_gen rmdir /s /q resources\_gen
echo Cleanup complete.

REM 重新生成网站
echo Building Hugo site...
hugo

echo Done! Your site is ready in the public folder.
echo You can now run: hugo server
