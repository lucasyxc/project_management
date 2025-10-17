# 项目管理系统

基于 Django + Vue 的项目管理系统

## 技术栈

- **后端**: Python Django + Django REST Framework
- **前端**: Vue 3 + Vite
- **数据库**: SQLite (开发) / PostgreSQL/MySQL (生产)

## 项目结构

```
项目管理系统/
├── backend/          # Django后端代码
├── frontend/         # Vue前端开发代码 (不推送到Git)
├── dist/            # 前端打包产物 (推送到Git)
├── deploy.sh        # Linux服务器部署脚本
├── deploy.bat       # Windows本地部署脚本
└── README.md        # 项目说明文档
```

## 开发环境搭建

### 后端开发

```bash
# 进入后端目录
cd backend

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 数据库迁移
python manage.py migrate

# 创建超级用户
python manage.py createsuperuser

# 启动开发服务器
python manage.py runserver 0.0.0.0:8000
```

### 前端开发

```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev

# 打包生产环境代码
npm run build
```

## 部署流程

### 1. 本地提交代码

```bash
# 确保前端已打包
cd frontend
npm run build
cd ..

# 提交代码到Git
git add .
git commit -m "更新说明"
git push origin main
```

### 2. 服务器拉取代码

```bash
# SSH登录服务器
ssh user@your-server

# 进入项目目录
cd /path/to/项目管理系统

# 拉取最新代码
git pull origin main
```

### 3. 更新服务器

```bash
# 运行部署脚本
chmod +x deploy.sh
./deploy.sh
```

或者手动执行：

```bash
# 更新后端依赖
cd backend
source venv/bin/activate
pip install -r requirements.txt

# 数据库迁移
python manage.py migrate

# 收集静态文件
python manage.py collectstatic --noinput

# 重启后端服务 (使用gunicorn + supervisor)
sudo supervisorctl restart project_backend

# 重新加载Nginx配置
sudo nginx -t
sudo systemctl reload nginx
```

## 服务器配置

### Nginx配置示例

由于80端口已被占用，建议使用其他端口（如8080）或配置子域名。

配置文件路径: `/etc/nginx/sites-available/project-management`

```nginx
server {
    listen 8080;  # 或使用其他端口
    server_name your-domain.com;  # 或IP地址

    # 前端静态文件
    location / {
        root /path/to/项目管理系统/dist;
        try_files $uri $uri/ /index.html;
    }

    # 后端API代理
    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Django静态文件
    location /static/ {
        alias /path/to/项目管理系统/backend/staticfiles/;
    }

    # Django媒体文件
    location /media/ {
        alias /path/to/项目管理系统/backend/media/;
    }
}
```

### Gunicorn配置

```bash
# 安装gunicorn
pip install gunicorn

# 启动命令
gunicorn --bind 127.0.0.1:8000 --workers 3 project_management.wsgi:application
```

### Supervisor配置示例

配置文件路径: `/etc/supervisor/conf.d/project_backend.conf`

```ini
[program:project_backend]
command=/path/to/项目管理系统/backend/venv/bin/gunicorn --bind 127.0.0.1:8000 --workers 3 project_management.wsgi:application
directory=/path/to/项目管理系统/backend
user=your-user
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/project_backend.log
```

## 环境变量配置

在服务器上创建 `backend/.env` 文件：

```env
DEBUG=False
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=your-domain.com,your-ip
DATABASE_URL=sqlite:///db.sqlite3
CORS_ALLOWED_ORIGINS=http://your-domain.com:8080
```

## 常见问题

### 1. 如何更改端口？
修改Nginx配置中的 `listen` 端口号。

### 2. 如何查看日志？
- 后端日志: `/var/log/project_backend.log`
- Nginx日志: `/var/log/nginx/error.log`

### 3. 如何重启服务？
```bash
sudo supervisorctl restart project_backend
sudo systemctl reload nginx
```

## API文档

API文档地址: `http://your-domain.com:8080/api/docs/`

## 许可证

MIT License

