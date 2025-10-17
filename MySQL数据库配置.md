# MySQL数据库配置指南

## 🎯 配置说明

本项目使用**独立的MySQL数据库**，与旧项目`lens_order_dev`数据库完全隔离，互不影响。

---

## 📋 数据库信息

### 旧项目数据库（不动它）
- ❌ 数据库名：`lens_order_dev`
- ❌ **绝不使用此数据库**

### 新项目数据库（要创建）
- ✅ 数据库名：`project_management`
- ✅ MySQL主机：1.14.110.116
- ✅ 端口：3306
- ✅ 用户名：ubuntu
- ✅ 密码：Ubuntu123!
- ✅ 字符集：utf8mb4

---

## 🔧 服务器配置步骤

### 第一步：创建新数据库

SSH登录服务器：
```bash
ssh ubuntu@1.14.110.116
```

登录MySQL并创建数据库：
```bash
mysql -u ubuntu -p
# 输入密码：Ubuntu123!
```

在MySQL命令行执行：
```sql
-- 创建新项目的独立数据库
CREATE DATABASE project_management CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 验证数据库已创建
SHOW DATABASES;

-- 应该能看到：
-- lens_order_dev（旧项目，不动）
-- project_management（新项目）

-- 退出MySQL
EXIT;
```

---

### 第二步：配置Django使用MySQL

在服务器上创建 `.env` 文件：

```bash
cd ~/projects/project_management/backend

# 复制生产环境配置
cp env.production .env

# 编辑配置（已经预设好了MySQL配置）
nano .env
```

`.env` 文件内容（已预配置好）：
```env
DEBUG=False
SECRET_KEY=your-random-secret-key-change-this
ALLOWED_HOSTS=1.14.110.116,localhost

# CORS配置
CORS_ALLOWED_ORIGINS=http://1.14.110.116:8080

# MySQL配置
DB_ENGINE=mysql
DB_NAME=project_management        # 新项目独立数据库
DB_USER=ubuntu
DB_PASSWORD=Ubuntu123!
DB_HOST=1.14.110.116
DB_PORT=3306
```

---

### 第三步：安装MySQL驱动并迁移

```bash
cd ~/projects/project_management/backend
source venv/bin/activate

# 安装MySQL客户端库
pip install mysqlclient

# 执行数据库迁移（会在project_management数据库中创建表）
python manage.py migrate

# 创建管理员账号
python manage.py createsuperuser

# 测试连接
python manage.py dbshell
# 应该能连接到MySQL，输入 \q 退出
```

---

### 第四步：重启服务

```bash
# 重启后端服务
pkill -f gunicorn
nohup gunicorn --bind 0.0.0.0:8001 --workers 3 project_management.wsgi:application > gunicorn.log 2>&1 &
```

---

## ✅ 验证配置

### 1. 检查数据库表
```bash
mysql -u ubuntu -p
# 输入密码：Ubuntu123!
```

```sql
USE project_management;
SHOW TABLES;

-- 应该能看到Django创建的表：
-- auth_user
-- django_migrations
-- apps_projects_project
-- apps_tasks_task
-- 等等...

EXIT;
```

### 2. 访问测试
```
http://1.14.110.116:8080/api/test/
http://1.14.110.116:8080/admin
```

---

## 📊 数据库隔离验证

### 两个项目完全独立

**旧项目：**
```sql
USE lens_order_dev;
SHOW TABLES;  -- 旧项目的表
```

**新项目：**
```sql
USE project_management;
SHOW TABLES;  -- 新项目的表
```

✅ 两个数据库互不影响，完全隔离！

---

## 🔄 本地开发 vs 生产环境

### 本地开发（自动使用SQLite）
```bash
# 本地不需要配置.env，默认使用SQLite
cd backend
venv\Scripts\activate
python manage.py runserver
```

### 生产环境（使用MySQL）
```bash
# 服务器上配置了.env后，自动使用MySQL
cd ~/projects/project_management/backend
source venv/bin/activate
python manage.py runserver 0.0.0.0:8001
```

---

## 🆘 常见问题

### Q1: 如何切换数据库？
**A:** 修改 `.env` 中的 `DB_ENGINE`
- `DB_ENGINE=sqlite3` → SQLite
- `DB_ENGINE=mysql` → MySQL

### Q2: MySQL连接失败怎么办？
```bash
# 检查MySQL服务
sudo systemctl status mysql

# 检查防火墙
sudo ufw status

# 测试连接
mysql -h 1.14.110.116 -u ubuntu -p
```

### Q3: 忘记创建数据库？
```bash
# 会报错：Unknown database 'project_management'
# 解决：按第一步创建数据库
```

### Q4: 想重置数据库？
```bash
# 登录MySQL
mysql -u ubuntu -p

# 删除并重建数据库
DROP DATABASE project_management;
CREATE DATABASE project_management CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;

# 重新迁移
python manage.py migrate
python manage.py createsuperuser
```

---

## 🎯 部署流程总结

### 首次部署（包含MySQL配置）
```bash
# 1. 创建MySQL数据库
mysql -u ubuntu -p
CREATE DATABASE project_management CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;

# 2. 拉取代码
cd ~/projects/project_management
git pull origin master

# 3. 配置环境
cd backend
cp env.production .env
# 配置已预设好，无需修改

# 4. 安装依赖并迁移
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser

# 5. 启动服务
pkill -f gunicorn
nohup gunicorn --bind 0.0.0.0:8001 --workers 3 project_management.wsgi:application > gunicorn.log 2>&1 &
```

### 日常更新（无需重新配置数据库）
```bash
cd ~/projects/project_management
git pull origin master
cd backend
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
pkill -f gunicorn
nohup gunicorn --bind 0.0.0.0:8001 --workers 3 project_management.wsgi:application > gunicorn.log 2>&1 &
```

---

## 🔒 安全提示

1. ✅ 新旧项目数据库完全隔离
2. ✅ 使用独立的数据库名
3. ✅ 密码不要提交到Git（.env已被忽略）
4. ✅ 生产环境记得设置强密码的SECRET_KEY

---

**配置完成！** 🎉

现在您有了：
- 旧项目：`lens_order_dev` 数据库
- 新项目：`project_management` 数据库
- 两个项目互不影响，共享同一个MySQL服务器

