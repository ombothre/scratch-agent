from pydantic import BaseModel
from ai.models.io import Tool, ToolOutput
from ai.components.tools.functions import tool_manual
from typing import Callable, Optional
import json

def has_tools(tools: list[Tool]) -> bool:
    for tool in tools:
        if tool.used == "yes":
            return True
    return False

def run_tools(tools: list[Tool]) -> list[ToolOutput]:

    tool_results: list[ToolOutput] = []

    for tool in tools:
        if tool.used == "yes":
            func: Callable = tool_manual[tool.name]
            args = tool.input
            result: Optional[BaseModel] = func(args)
            # print(f"TOOL: {tool.name} -> {result}")
        else:
            result = None

        output = ToolOutput(**tool.model_dump(), result=result.model_dump() if result else None)
        tool_results.append(output)
    
    return tool_results

def jsonify(tool_results: list[ToolOutput]) -> str:
    return json.dumps([result.model_dump_json(indent=4) for result in tool_results])