from pydantic import BaseModel, Field, HttpUrl
from typing import List, Dict, Optional, Literal

class Tool(BaseModel):
    name: Literal["web_search", "research_papers"]
    used: Literal["yes", "no"]
    input: str


# ---------- web_search ----------
class WebResult(BaseModel):
    url: HttpUrl
    title: str
    content: str


class Result(WebResult):
    score: float
    raw_content: Optional[str] = None


class TavilyResponse(BaseModel):
    query: str
    follow_up_questions: Optional[List[str]] = None
    answer: Optional[str] = None
    images: List[str] = []
    results: List[Result]
    response_time: float


class WebResponse(BaseModel):
    results: list[WebResult]


# ---------- research_paper ----------
class Query(BaseModel):
    start_index: int = Field(..., alias="start-index")
    search_terms: str = Field(..., alias="search-terms")


class Item(BaseModel):
    title: List[str]
    URL: HttpUrl


class Message(BaseModel):
    facets: Dict[str, dict]
    total_results: int = Field(..., alias="total-results")
    items: List[Item]
    items_per_page: int = Field(..., alias="items-per-page")
    query: Query


class CrossrefResponse(BaseModel):
    status: str
    message_type: str = Field(..., alias="message-type")
    message_version: str = Field(..., alias="message-version")
    message: Message

    class Config:
        populate_by_name = True


class ResearchResponse(BaseModel):
    results: list[Item]
