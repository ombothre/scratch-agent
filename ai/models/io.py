from pydantic import BaseModel
from typing import Literal, Any, Optional

class Tool(BaseModel):
    name: Literal["web_search", "research_papers"]
    used: Literal["yes", "no"]
    input: str

class ToolOutput(Tool):
    result: Optional[dict[str, Any]]

class ResearchOutput(BaseModel):
    ai: str
    tools: list[Tool]

class OutputerInput(BaseModel):
    ai: str
    tools: list[ToolOutput]