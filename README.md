# AI 翻译助手（后端 + 简单界面）

实现内容：
- **后端**：FastAPI `POST /translate`，调用 OpenAI 兼容的大模型 API（默认 DeepSeek）返回：
  - `translation`: 英文翻译
  - `keywords`: 3 个中文关键词
- **前端**：纯 HTML 页面：输入中文 → 点击翻译 → 展示翻译与关键词

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
  ai_usage_record_template.md
```

---

## Part 1：运行后端（FastAPI）

### 1) 安装依赖

```bash
cd backend
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
# source .venv/bin/activate

pip install -r requirements.txt
```

### 2) 配置 API Key

把 `.env.example` 复制为 `.env`，并填入你的 key：

```bash
cp .env.example .env
# 编辑 .env，把 LLM_API_KEY=YOUR_API_KEY_HERE 改成你的真实 key
```

> 默认使用 DeepSeek：
> - base_url: `https://api.deepseek.com`
> - model: `deepseek-chat`
>
> 你也可以切换到其他 OpenAI 兼容服务（或 OpenAI），改 `.env` 中：
> - `LLM_PROVIDER=other`
> - `LLM_BASE_URL=https://api.openai.com/v1`
> - `LLM_MODEL=gpt-4o-mini`（或你可用的模型）

DeepSeek 官方文档说明其 API 与 OpenAI 格式兼容，可用 `https://api.deepseek.com` 或 `https://api.deepseek.com/v1` 作为 base_url。citeturn0search1

### 3) 启动服务

```bash
uvicorn main:app --reload --port 8000
```

测试接口：

```bash
curl -X POST http://localhost:8000/translate \
  -H "Content-Type: application/json" \
  -d '{"text":"我想做一个AI翻译助手，用于学习英语。"}'
```

---

## Part 2：运行前端（纯 HTML）

方式 A：直接双击打开 `frontend/index.html`（部分浏览器可能限制 file:// 发起请求）

方式 B（推荐）：起一个本地静态服务器：

```bash
cd frontend
python -m http.server 5173
```

然后浏览器打开：
- http://localhost:5173

页面上可以修改“后端地址”（默认 http://localhost:8000）。

---

## 常见问题

1) **跨域（CORS）问题**
- 本项目在 FastAPI 中已添加 `CORSMiddleware`，并默认允许 `*`，便于 demo。FastAPI 官方文档说明可用 `allow_origins=['*']` 允许任意域名。citeturn0search2

2) **LLM 输出不是严格 JSON**
- 后端做了容错：尝试提取 `Ellipsis` JSON 块并解析；仍失败则返回 raw 文本 + 简单关键词兜底。

---

## 提交建议

- 把整个仓库 push 到 GitHub / Gitee
- 提交时附带：
  1. 仓库链接
  2. 运行说明（本 README）
  3. AI 对话截图/记录（参考 `ai_usage_record_template.md`）
  4. 开发过程文字说明
