from typing import List, Optional
from pydantic import BaseModel, HttpUrl, Field


class Template(BaseModel):
    """Schema for creative templates (photo/video). Collection name: template"""
    id: Optional[str] = Field(default=None, description="Document ID")
    title: str
    category: str
    type: str = Field(pattern="^(photo|video)$")
    thumbnail_url: HttpUrl
    source_url: Optional[HttpUrl] = None
    tags: List[str] = []
    description: Optional[str] = None


class TemplateQuery(BaseModel):
    q: Optional[str] = None
    category: Optional[str] = None
    type: Optional[str] = None
    limit: int = 24
