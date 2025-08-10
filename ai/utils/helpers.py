from ai.models.message import AnyMessage, HumanMessage, AiMessage
from ai.models.payload import SystemInstruction, Part
import re

def add_message(state: list[AnyMessage], message: AnyMessage) -> list[AnyMessage]:
    state.append(message)
    return state

def to_human_msg(input: str) -> HumanMessage:
    return HumanMessage(
        content=input
    )

def to_ai_msg(input: str) -> AiMessage:
    return AiMessage(
        content=input
    )

def to_system_msg(input: str) -> SystemInstruction:
    return SystemInstruction(
        parts=[
            Part(
                text=input
            )
        ]
    )

def structure_llm_json(raw: str) -> str:
    # Remove opening triple backticks with optional "json"
    cleaned = re.sub(r"^```(?:json)?\s*", "", raw.strip(), flags=re.IGNORECASE)
    # Remove closing triple backticks
    cleaned = re.sub(r"\s*```$", "", cleaned.strip())
    return cleaned
