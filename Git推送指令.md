# Git推送指令 - 极简版

## 仓库地址
```
https://github.com/lucasyxc/project_management.git
```

## 首次推送（只需要执行一次）

```bash
# 1. 添加所有文件
git add .

# 2. 提交
git commit -m "首次提交"

# 3. 推送到GitHub（首次需要-u参数）
git push -u origin master
```

---

## 日常更新推送（每次修改后）

```bash
# 1. 前端打包（如果修改了前端）
cd frontend
npm run build
cd ..

# 2. 添加修改的文件
git add .

# 3. 提交（把"更新内容"改成你的描述）
git commit -m "更新内容"

# 4. 推送
git push
```

---

## 快捷命令（三步走）

```bash
git add .
git commit -m "更新"
git push
```

就这么简单！🎉

---

## 注意事项

- ✅ **会推送**: `backend/`、`dist/`、`*.md`、`deploy.sh`、`deploy.bat`
- ❌ **不会推送**: `frontend/`源码、`node_modules/`、`venv/`、`.env`

---

## 遇到问题？

### 问题1: 提示需要登录
- 第一次推送会要求输入GitHub用户名和密码
- 或使用GitHub Personal Access Token

### 问题2: 提示推送失败
```bash
# 先拉取远程更新
git pull origin master

# 再推送
git push
```

