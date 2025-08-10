from ai.components.graph.graph import AiGraph
from ai.components.graph.state import State

def chat(query: str) -> str:
    
    ai = AiGraph()
    result: State = ai.invoke(query)

    if result['latest_content']:
        return result['latest_content']
    
    return "Not Available"