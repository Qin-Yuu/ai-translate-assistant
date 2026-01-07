# AI 使用记录（模板，提交必备）

> 建议你在 Cursor / ChatGPT / Claude 中开发时边做边截图。
> 你可以把“关键节点”的对话截图放在 `screenshots/` 目录（或直接放到 README 里）。

---

## 1) 我如何使用 AI（对话记录/截图）

请按时间顺序贴：
- 截图 1：让 AI 生成后端 FastAPI 基础骨架（main.py + schemas）
- 截图 2：让 AI 生成 LLM 调用封装（requests 调 OpenAI-compatible chat/completions）
- 截图 3：让 AI 生成前端 HTML（fetch 调 /translate）
- 截图 4：遇到 bug（例如 CORS / JSON 解析失败 / 500 报错），把报错日志贴给 AI，请它给出定位步骤与 patch

---

## 2) 哪些代码是 AI 生成的？我做了哪些修改？

示例写法（请替换为你的真实情况）：
- AI 生成：
  - `backend/main.py` 初版路由与 CORS
  - `backend/llm_client.py` 调用模型与解析 JSON 的初版
  - `frontend/index.html` 的基础 UI 与 fetch 请求
- 我做的修改：
  - 增加输入校验（空字符串、长度限制）
  - 增加 JSON 解析容错：失败时尝试提取 {...} 子串
  - 增加 keywords 必须为 3 个的兜底逻辑
  - README 补全运行说明

---

## 3) 我遇到的问题 & 我如何让 AI 帮我解决？

建议用“可复现信息”描述：
- 问题现象：
- 复现步骤（最小复现）：
- 报错日志（关键堆栈）：
- 相关代码片段（30~80 行）：
- 我让 AI 做了什么（例如：先列原因列表与验证顺序，再给 patch）：
- 修复后如何验证（接口测试、回归用例）：

---

## 4) 最终总结（1~2 段）

建议包含：
- 我如何拆分任务（后端→前端→联调→容错→文档）
- 我如何用 AI 提升效率（搭骨架、定位 bug、补文档/README）
- 我如何保证结果可交付（能跑通、有测试/验证步骤）
