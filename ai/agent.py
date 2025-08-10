from ai.components.graph.graph import AiGraph
from ai.components.graph.state import State
from ai.models.io import FinalOutput, Chat

def chat(query: str) -> Chat:
    
    ai = AiGraph()
    result: FinalOutput = ai.invoke(query)
    final_state = result['state']

    if final_state['latest_content']:
        response =  final_state['latest_content']
    else:
        response = "Not Available"

    return {
        "response": response,
        "flow": result['flow']
    }