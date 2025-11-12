from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from database import db, create_document, get_documents
from schemas import Template, TemplateQuery

app = FastAPI(title="Creative Templates & Editor API", version="0.1.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/test")
async def test():
    # basic db ping
    status = await db.command({"ping": 1})
    return {"status": "ok", "db": status}


@app.post("/templates", response_model=Template)
async def create_template(template: Template):
    data = template.dict(exclude_none=True)
    inserted = await create_document("template", data)
    return Template(**inserted)


def _build_filter(q: Optional[str], category: Optional[str], type_: Optional[str]):
    f = {}
    if q:
        f["$or"] = [
            {"title": {"$regex": q, "$options": "i"}},
            {"tags": {"$elemMatch": {"$regex": q, "$options": "i"}}},
            {"description": {"$regex": q, "$options": "i"}},
        ]
    if category:
        f["category"] = category
    if type_:
        f["type"] = type_
    return f


class TemplatesResponse(BaseModel):
    items: List[Template]
    total: int


@app.get("/templates", response_model=TemplatesResponse)
async def list_templates(
    q: Optional[str] = Query(default=None),
    category: Optional[str] = Query(default=None),
    type: Optional[str] = Query(default=None),
    limit: int = Query(default=24, ge=1, le=100),
):
    filter_dict = _build_filter(q, category, type)
    docs = await get_documents("template", filter_dict=filter_dict, limit=limit)
    total = len(docs)
    items = [Template(**d) for d in docs]
    return TemplatesResponse(items=items, total=total)
