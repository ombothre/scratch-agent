from __future__ import annotations
from typing import TypedDict, Annotated, Callable, Optional
from ai.models.message import AnyMessage
from ai.utils.helpers import add_message

class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_message]
    next_node: Optional[state_fun]
    latest_content: Optional[str]

state_fun = Callable[[State], State]