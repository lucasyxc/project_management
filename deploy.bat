@echo off
chcp 65001 >nul
REM ========================================
REM 项目管理系统 - Windows本地开发部署脚本
REM ========================================

echo =========================================
echo 开始部署项目管理系统（Windows本地）
echo =========================================

REM 进入后端目录
cd backend

REM 激活虚拟环境
echo 激活Python虚拟环境...
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
) else (
    echo 错误: 虚拟环境不存在，请先创建虚拟环境
    echo 运行: python -m venv venv
    pause
    exit /b 1
)

REM 更新依赖
echo 更新Python依赖...
pip install -r requirements.txt --quiet

REM 数据库迁移
echo 执行数据库迁移...
python manage.py migrate

REM 收集静态文件
echo 收集静态文件...
python manage.py collectstatic --noinput

echo =========================================
echo 部署完成！
echo =========================================
echo.
echo 启动开发服务器:
echo   python manage.py runserver 0.0.0.0:8000
echo.
echo 访问地址: http://localhost:8000
echo 管理后台: http://localhost:8000/admin
echo =========================================

pause

