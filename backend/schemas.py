from pydantic import BaseModel, Field
from typing import List

class TranslateRequest(BaseModel):
    text: str = Field(..., description="要翻译的中文内容")

class TranslateResponse(BaseModel):
    translation: str
    keywords: List[str]
