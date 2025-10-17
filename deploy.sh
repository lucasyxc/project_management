#!/bin/bash

# ========================================
# 项目管理系统 - 服务器部署脚本
# ========================================

echo "========================================="
echo "开始部署项目管理系统"
echo "========================================="

# 获取脚本所在目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
BACKEND_DIR="$SCRIPT_DIR/backend"

# 检查是否在正确的目录
if [ ! -d "$BACKEND_DIR" ]; then
    echo "错误: 找不到backend目录"
    exit 1
fi

# 进入后端目录
cd "$BACKEND_DIR"

# 激活虚拟环境
echo "激活Python虚拟环境..."
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
else
    echo "错误: 虚拟环境不存在，请先创建虚拟环境"
    echo "运行: python3 -m venv venv"
    exit 1
fi

# 更新依赖
echo "更新Python依赖..."
pip install -r requirements.txt --quiet

# 数据库迁移
echo "执行数据库迁移..."
python manage.py migrate --noinput

# 收集静态文件
echo "收集静态文件..."
python manage.py collectstatic --noinput

# 重启后端服务
echo "重启后端服务..."
if command -v supervisorctl &> /dev/null; then
    sudo supervisorctl restart project_backend
    echo "后端服务已重启"
else
    echo "警告: supervisorctl未安装，请手动重启后端服务"
    echo "或使用: sudo systemctl restart project_backend (如果使用systemd)"
fi

# 重新加载Nginx
echo "重新加载Nginx配置..."
if command -v nginx &> /dev/null; then
    sudo nginx -t && sudo systemctl reload nginx
    echo "Nginx已重新加载"
else
    echo "警告: Nginx未安装或未在PATH中"
fi

echo "========================================="
echo "部署完成！"
echo "========================================="
echo "访问地址: http://your-server-ip:8080"
echo "管理后台: http://your-server-ip:8080/admin"
echo "API测试: http://your-server-ip:8080/api/test/"
echo ""
echo "端口配置:"
echo "  前端: 8080 (Nginx)"
echo "  后端: 8001 (Gunicorn)"
echo ""
echo "查看日志:"
echo "  后端: sudo tail -f /var/log/project_backend.log"
echo "  Nginx: sudo tail -f /var/log/nginx/error.log"
echo "========================================="

