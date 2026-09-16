@echo off
echo ========================================
echo   WSL2 + Docker 重启后配置脚本
echo ========================================
echo.

echo [1/4] 启动Ubuntu并初始化...
echo 首次启动Ubuntu会要求创建用户名和密码
echo 请记住你设置的用户名和密码
echo.
pause

echo.
echo [2/4] 启动Docker Desktop...
start "" "C:\Program Files\Docker\Docker\Docker Desktop.exe"
echo 等待Docker启动（约30秒）...
timeout /t 30 /nobreak >nul

echo.
echo [3/4] 验证Docker安装...
docker --version
docker-compose --version
echo.
echo 如果上面显示了版本号，说明Docker安装成功！
echo.

echo [4/4] 测试Docker运行...
docker run hello-world
echo.
echo ========================================
echo   配置完成！
echo ========================================
echo.
echo 接下来你可以：
echo 1. 在Ubuntu中运行：cd /mnt/e/ai-project/E-commerce-ai
echo 2. 开始第1周的学习和项目开发
echo.
pause
