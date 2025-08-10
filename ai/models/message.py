from pydantic import BaseModel, Field
from typing import Literal, Union

gemini_model = Literal["gemini-2.0-flash", "gemini-1.5-pro"]

class Message(BaseModel):
    by: Literal["user", "model"]
    content: str

class HumanMessage(Message):
    by: Literal["user"] = Field(default="user")

class AiMessage(Message):
    by: Literal["model"] = Field(default="model")

AnyMessage = Union[HumanMessage, AiMessage]
