# 🚀 快速上传项目到 GitHub 标准流程

## 一、前置准备（只需一次）

### 1. 配置 Git 用户信息
```bash
git config --global user.name "你的GitHub用户名"
git config --global user.email "你的邮箱@example.com"
```

### 2. 配置代理（国内网络需要）
```bash
# 设置代理（端口根据你的代理软件调整，常见：7890、10809）
git config --global http.proxy http://127.0.0.1:7890
git config --global https.proxy http://127.0.0.1:7890

# 取消代理（后续不想用代理时）
git config --global --unset http.proxy
git config --global --unset https.proxy
```

### 3. 生成 GitHub Token
1. 打开 https://github.com/settings/tokens
2. 点击 **Generate new token (classic)**
3. 勾选 **`repo`** 权限，生成并保存 Token（以 `ghp_` 开头）

---

## 二、每次新项目上传（标准 5 步）

### 第1步：进入项目目录并初始化
```bash
cd 你的项目目录
git init
```

### 第2步：添加所有文件
```bash
git add -A
```

### 第3步：提交代码
```bash
git commit -m "首次提交：项目描述"
```

### 第4步：在 GitHub 创建仓库（用 Token + API）
```bash
# 将下面命令中的 TOKEN 和 仓库名 替换为你自己的
curl -X POST https://api.github.com/user/repos \
  -H "Authorization: token ghp_你的Token" \
  -H "Content-Type: application/json" \
  -d '{"name":"仓库名","private":false}'
```

> **Windows PowerShell 替代方案**（如果 curl 报错，用 Python）：
> ```python
> import urllib.request, json
> token = 'ghp_你的Token'
> repo_name = '仓库名'
> url = 'https://api.github.com/user/repos'
> data = json.dumps({'name': repo_name, 'private': False}).encode()
> req = urllib.request.Request(url, data=data, method='POST')
> req.add_header('Authorization', 'token ' + token)
> req.add_header('Content-Type', 'application/json')
> resp = urllib.request.urlopen(req)
> print('创建成功:', json.loads(resp.read())['clone_url'])
> ```

### 第5步：推送到远程仓库
```bash
git remote add origin https://github.com/你的用户名/仓库名.git
git push -u origin master
```

> 如果报 `Repository not found`，说明第4步仓库没创建成功，检查 Token 权限或网络。

---

## 三、一键脚本（推荐）

把以下内容保存为 `git_push.bat`，以后每个项目直接用：

```bash
@echo off
set /p repo_name="请输入仓库名: "
set /p desc="请输入提交描述: "

git init
git add -A
git commit -m "%desc%"

REM 创建GitHub仓库
curl -X POST https://api.github.com/user/repos ^
  -H "Authorization: token ghp_你的Token" ^
  -H "Content-Type: application/json" ^
  -d "{\"name\":\"%repo_name%\",\"private\":false}"

git remote add origin https://github.com/你的用户名/%repo_name%.git
git push -u origin master
pause
```

---

## 四、本次操作回顾（参考）

| 步骤 | 命令/操作 | 说明 |
|------|-----------|------|
| 1 | `git init` | 初始化本地仓库 |
| 2 | `git add -A` | 添加所有文件到暂存 |
| 3 | `git commit -m "..."` | 提交代码 |
| 4 | 用Token调用GitHub API | 创建远程仓库 |
| 5 | `git remote add origin ...` | 关联远程仓库 |
| 6 | `git push -u origin master` | 推送到GitHub |
| 特殊 | `git config --global http.proxy` | 配置代理解决网络问题 |

**核心要点**：
- **Token** 是访问GitHub的钥匙，生成一次永久使用
- **代理** 解决国内访问GitHub的网络问题
- **5步流程** 适用于任何新项目