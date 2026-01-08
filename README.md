# AI 翻译助手（FastAPI 后端 + 纯 HTML 前端）

一个面试/学习向的小项目：输入中文，调用 OpenAI 兼容的大模型 API（默认 DeepSeek）完成：
- 英文翻译 `translation`
- 抽取 3 个中文关键词 `keywords`

---

## 功能

- 后端：FastAPI `POST /translate`
- 前端：纯 HTML + 原生 JS（可配置后端地址，带“翻译中…”状态与错误提示）
- 支持 DeepSeek / 其他 OpenAI 兼容服务（通过 `.env` 配置）

---

## 目录结构

```
ai-translate-assistant/
  backend/
    main.py
    llm_client.py
    schemas.py
    requirements.txt
    .env.example
  frontend/
    index.html
  scripts/
    dev.py
  README.md
```

---

## 快速开始（推荐：一键同时启动前后端）

### 1）克隆项目

```bash
git clone https://github.com/Qin-Yuu/ai-translate-assistant.git
cd ai-translate-assistant
```

### 2）安装后端依赖（建议使用虚拟环境）

进入后端目录创建并激活虚拟环境：

**Windows（PowerShell）**
```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

**macOS / Linux**
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

> 说明：后端依赖安装在虚拟环境里后，请保持该终端的虚拟环境处于激活状态，再回到根目录运行脚本。

### 3）配置 API Key（必需）

在 `backend/` 下复制环境变量模板：

```bash
cd backend
# macOS/Linux
cp .env.example .env
# Windows（PowerShell）也可以手动复制重命名 .env.example -> .env
```

编辑 `backend/.env`，填入你的 Key（以 `.env.example` 为准）。常用字段如下：

```env
LLM_API_KEY=YOUR_API_KEY_HERE
LLM_BASE_URL=https://api.deepseek.com/v1
LLM_MODEL=deepseek-chat
LLM_PROVIDER=deepseek
```

### 4）一键启动（后端 + 前端）

回到仓库根目录（确保虚拟环境仍激活）：

```bash
cd ..
python scripts/dev.py
```

启动后：
- 前端：http://127.0.0.1:5173
- 后端：http://127.0.0.1:8000
- 后端 Swagger：http://127.0.0.1:8000/docs

如端口冲突：
```bash
python scripts/dev.py --api-port 8001 --web-port 5174
```

---

## 分开启动（可选）

### 启动后端

```bash
cd backend
# （先激活虚拟环境）
uvicorn main:app --reload --port 8000
```

### 启动前端

```bash
cd frontend
python -m http.server 5173
```

打开：http://127.0.0.1:5173

---

## API 使用说明

### POST /translate

**Request**
```json
{
  "text": "要翻译的中文内容"
}
```

**Response**
```json
{
  "translation": "English translation result",
  "keywords": ["关键词1", "关键词2", "关键词3"]
}
```

### curl 测试

```bash
curl -X POST "http://127.0.0.1:8000/translate" \
  -H "Content-Type: application/json" \
  -d "{\"text\":\"我想做一个AI翻译助手，用于学习英语。\"}"
```

---

## 常见问题（Troubleshooting）

### 1）前端报错：Failed to fetch / CORS
- 确认后端已启动，且前端配置的后端地址正确（默认 `http://localhost:8000`）
- 本项目后端通常会添加 `CORSMiddleware` 方便 demo；若你改过代码导致跨域失败，请在 FastAPI 中开启 CORS。

### 2）脚本启动时报 `No module named uvicorn`
原因：你运行 `python scripts/dev.py` 的 Python 环境没有安装后端依赖。  
解决：确保已在 `backend/` 里安装依赖，并且当前终端虚拟环境已激活。

### 3）接口返回 401/403
原因：`LLM_API_KEY` 未配置或无效 / 额度不足。  
解决：检查 `backend/.env` 是否存在且值正确。

### 4）端口占用
用参数改端口：
```bash
python scripts/dev.py --api-port 8001 --web-port 5174
```

---

