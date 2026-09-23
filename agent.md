# 项目协作说明

## 项目概览

这是一个 Django + Vue 的前后端分离项目：

- Django 负责后端、数据库、管理后台和后续 API。
- SimpleUI 替换 Django Admin 的默认后台界面。
- Vue 3 + Vite 负责前台网站，代码位于 `frontend/`。
- 当前数据库使用项目根目录的 SQLite 文件 `db.sqlite3`。

## 目录结构

```text
.
├── config/                 # Django 项目配置、路由、WSGI/ASGI
├── main/                   # Django 主应用
├── frontend/               # Vue 3 + Vite 前端
├── manage.py               # Django 管理入口
├── db.sqlite3              # 本地开发数据库
└── .venv/                  # Python 虚拟环境
```

## 开发环境

Python 使用 3.12，Django 使用 6.1.1，前端使用 Vue 3、Vite 8 和 SimpleUI 2026.1.13。

PowerShell 中先激活 Python 环境：

```powershell
. .\.venv\Scripts\Activate.ps1
```

## 启动命令

启动 Django 后端和管理后台：

```powershell
python manage.py runserver 127.0.0.1:8000
```

管理后台地址：`http://127.0.0.1:8000/admin/`

启动 Vue 前台：

```powershell
cd frontend
npm install
npm run dev -- --host 127.0.0.1
```

Vue 前台默认地址：`http://127.0.0.1:5173/`。Vite 已将 `/api` 请求代理到 Django 的 `http://127.0.0.1:8000`。

生产构建：

```powershell
cd frontend
npm run build
```

## Django 开发约定

- 新增后端功能优先放入 `main/`，不要把业务逻辑堆积到 `config/`。
- 修改模型后执行 `python manage.py makemigrations` 和 `python manage.py migrate`。
- 修改路由时检查 `config/urls.py`，API 路径统一使用 `/api/` 前缀。
- 管理后台相关配置使用 Django Admin / SimpleUI 配置，不要修改 SimpleUI 安装包源码。
- 默认语言为简体中文 `zh-hans`；不要在业务代码中硬编码可翻译的界面文案。
- 不要提交真实密钥、生产数据库、密码或本地环境变量。

## Vue 开发约定

- 前台页面和组件放在 `frontend/src/`。
- 可复用界面拆分为 `frontend/src/components/` 组件。
- 与 Django 的数据交互通过 `/api/`，不要在组件中写死后端完整地址。
- 保持前端构建无错误；提交前运行 `npm run build`。
- 修改 UI 时同时考虑窄屏布局和中文文本长度。

## 验证清单

后端变更至少执行：

```powershell
python manage.py check
```

前端变更至少执行：

```powershell
cd frontend
npm run build
```

如果改动涉及数据库，再执行迁移并检查 `db.sqlite3` 是否产生预期变更。
