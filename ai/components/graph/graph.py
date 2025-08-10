from ai.components.graph.state import State
from ai.components.llm.llm import LLM
from ai.components.llm.prompts import researcher_prompt, outputer_prompt
from ai.models.message import AiMessage
from ai.models.io import ResearchOutput, OutputerInput, FinalOutput
from ai.utils.helpers import to_human_msg, to_ai_msg, add_message, structure_llm_json
from ai.components.tools.helpers import has_tools, run_tools
from pydantic import ValidationError
from typing import cast, Callable
import json

def named_node(name: str):
    def decorator(func: Callable):
        func.__name__ = name
        return func
    return decorator

class AiGraph:

    def __init__(self) -> None:
        self.flash_llm = LLM("gemini-2.0-flash")
        self.pro_llm = LLM("gemini-2.0-flash")          # pro not available
        self.flow: list[str] = [self.start_node.__name__]

    def _compile(self, input: str):

        first_msg = to_human_msg(input)

        self.state: State = {
            "messages": [first_msg],
            "next_node": self.start_node,
            "latest_content": None
        }

    def invoke(self, input: str) -> FinalOutput:

        self._compile(input)

        while self.state["next_node"] != None:
            curr_node = self.state["next_node"]
            self.state = curr_node(self.state)
        
        return {
            "state": self.state,
            "flow": self.flow
        }

    #State

    #Nodes
    # "start"
    @named_node("Start")
    def start_node(self, state: State) -> State:

        #EDGE
        next_node = self.research_llm
        state['next_node'] = next_node
        self.flow.append(next_node.__name__)
        return state

    # "researcher"
    @named_node("Researcher")
    def research_llm(self, state: State) -> State:

        payload = self.pro_llm.get_payload(messages=state["messages"], system_prompt=researcher_prompt())
        result: str | None = self.pro_llm.run(payload)

        if result:
            # validate
            try:
                cleaned_result = structure_llm_json(result)
                structured_result = ResearchOutput.model_validate_json(cleaned_result)

                print(f"RESEARCHER: {structured_result} \n\n")

                # state update
                state["messages"] = add_message(state["messages"], to_ai_msg(structured_result.model_dump_json()))
                state["latest_content"] = structured_result.ai

                # EDGE
                next_node = self.tool_condition
                state['next_node'] = next_node
                self.flow.append(next_node.__name__)

            except ValidationError as e:
                print(f"AI response wrong strcuture: {str(e)}")
                next_node = self.end_node
                state['next_node'] = next_node
                self.flow.append(next_node.__name__)

        return state
    
    @named_node("Tools")
    def tool_condition(self, state: State) -> State:

        latest = cast(AiMessage, state["messages"][-1])
        research_output = ResearchOutput(**json.loads(latest.content))
        
        # Conditionl Edge
        if has_tools(research_output.tools):
            tool_results = run_tools(research_output.tools)

            print(f"TOOLS: {tool_results} \n\n")

            # Update message
            latest_message = OutputerInput(
                ai = research_output.ai,
                tools=tool_results
            )
            state["messages"][-1] = AiMessage(
                content=latest_message.model_dump_json()
            )

            # EDGE
            next_node = self.output_llm
            state['next_node'] = next_node
            self.flow.append(next_node.__name__)

        # Second Edge
        else:
            #EDGE
            next_node = self.end_node
            state['next_node'] = next_node
            self.flow.append(next_node.__name__)

        return state

    @named_node("Writer")
    def output_llm(self, state: State) -> State:

        latest = cast(AiMessage, state["messages"][-1])

        system_prompt = outputer_prompt(latest.content)
        payload = self.flash_llm.get_payload(messages=state["messages"], system_prompt=system_prompt)
        result: str | None = self.flash_llm.run(payload)

        try:
            if result:
                cleaned_result = structure_llm_json(result)

                print("FINAL RESPONSE: ", cleaned_result)
                
                # state update
                state["messages"] = add_message(state["messages"], to_ai_msg(cleaned_result))
                state["latest_content"] = cleaned_result

                # EDGE
                next_node = self.end_node
                state['next_node'] = next_node
                self.flow.append(next_node.__name__)

        except ValidationError as e:
            print(f"AI response wrong strcuture: {str(e)}")
            next_node = self.end_node
            state['next_node'] = next_node
            self.flow.append(next_node.__name__)
        return state
    
    @named_node("End")
    def end_node(self, state: State) -> State:
        # Edge
        state["next_node"] = None
        return state
