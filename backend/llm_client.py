import os
import json
import re
from typing import Dict, Any, List
import requests

DEFAULT_SYSTEM_PROMPT = """你是一个专业的翻译与信息抽取助手。
任务：把输入的中文翻译成自然、准确的英文；并从中文原文中提取3个最关键的中文关键词（不是英文）。
要求：
- 只输出严格 JSON（不要包含额外文本、不要 markdown）
- JSON 结构必须为：{"translation": "...", "keywords": ["关键词1","关键词2","关键词3"]}
- keywords 必须是中文、且正好 3 个；如不足，请用更通用的相关词补足
"""

def _fallback_keywords(text: str) -> List[str]:
    """
    Very lightweight fallback: extract up to 3 Chinese "chunks" (2-6 chars) that appear early and look contentful.
    This is only used if the model output isn't parseable.
    """
    chunks = re.findall(r"[\u4e00-\u9fff]{2,6}", text)
    seen = []
    for c in chunks:
        if c not in seen:
            seen.append(c)
        if len(seen) == 3:
            break
    while len(seen) < 3:
        seen.append("关键词")
    return seen[:3]

def _extract_json_object(s: str) -> Dict[str, Any]:
    """
    Try parse JSON. If it fails, try to locate the first {...} block.
    """
    s = s.strip()
    try:
        return json.loads(s)
    except Exception:
        # find first JSON object
        m = re.search(r"\{.*\}", s, flags=re.DOTALL)
        if not m:
            raise
        return json.loads(m.group(0))

def _post_chat_completions(base_url: str, api_key: str, model: str, messages: List[Dict[str, str]]) -> str:
    base_url = base_url.rstrip("/")
    url = f"{base_url}/chat/completions"
    timeout = float(os.getenv("HTTP_TIMEOUT", "60"))

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": model,
        "messages": messages,
        "temperature": float(os.getenv("TEMPERATURE", "0.2")),
        "max_tokens": int(os.getenv("MAX_TOKENS", "400")),
    }

    resp = requests.post(url, headers=headers, json=payload, timeout=timeout)
    if resp.status_code >= 400:
        raise RuntimeError(f"LLM API error {resp.status_code}: {resp.text[:500]}")
    data = resp.json()
    # OpenAI-compatible chat.completions format: choices[0].message.content
    return data["choices"][0]["message"]["content"]

def translate_with_llm(text: str) -> Dict[str, Any]:
    """
    Uses an OpenAI-compatible Chat Completions endpoint.
    - Works with DeepSeek (base_url=https://api.deepseek.com)
    - Works with OpenAI-style base_url that includes /v1 (e.g., https://api.openai.com/v1)
    """
    provider = os.getenv("LLM_PROVIDER", "deepseek").lower()

    if provider == "deepseek":
        base_url = os.getenv("LLM_BASE_URL", "https://api.deepseek.com")
        model = os.getenv("LLM_MODEL", "deepseek-chat")
    else:
        # generic OpenAI-compatible provider
        base_url = os.getenv("LLM_BASE_URL", "https://api.openai.com/v1")
        model = os.getenv("LLM_MODEL", "gpt-4o-mini")

    api_key = os.getenv("LLM_API_KEY", "")
    if not api_key:
        raise RuntimeError("Missing LLM_API_KEY. Put it in .env or environment variables.")

    system_prompt = os.getenv("SYSTEM_PROMPT", DEFAULT_SYSTEM_PROMPT)

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"中文原文：{text}"},
    ]

    raw = _post_chat_completions(base_url, api_key, model, messages)

    try:
        obj = _extract_json_object(raw)
        translation = str(obj.get("translation", "")).strip()
        keywords = obj.get("keywords", [])
        if not translation:
            raise ValueError("empty translation")
        if not isinstance(keywords, list):
            raise ValueError("keywords not list")
        keywords = [str(k).strip() for k in keywords if str(k).strip()]
        # enforce exactly 3
        if len(keywords) < 3:
            keywords = keywords + _fallback_keywords(text)[len(keywords):]
        keywords = keywords[:3]
        return {"translation": translation, "keywords": keywords}
    except Exception:
        # best-effort fallback
        return {
            "translation": raw.strip(),
            "keywords": _fallback_keywords(text),
        }
