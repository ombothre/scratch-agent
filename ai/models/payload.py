from pydantic import BaseModel
from typing import List, Dict, Any, Literal, Optional

class Part(BaseModel):
    text: str

class Content(BaseModel):
    role: Literal["user", "model"]
    parts: List[Part]

class ResponseSchemaProperties(BaseModel):
    authorName: str
    birthYear: int
    famousSeries: List[str]
    iRobotDescription: str

class GenerationConfig(BaseModel):
    responseMimeType: str = "application/json"
    responseSchema: str              # JSON with gemini schema
    temperature: Optional[float] = None

class SystemInstruction(BaseModel):
    parts: List[Part]

class GeminiPayload(BaseModel):
    system_instruction: Optional[SystemInstruction] = None
    contents: List[Content]
    generationConfig: Optional[GenerationConfig] = None