import requests
from ai.config.settings import options
from ai.models.message import AnyMessage, gemini_model
from ai.models.payload import GeminiPayload, GenerationConfig
from ai.utils.helpers import to_system_msg
from ai.utils.msg_handler import messages_to_history
from ai.utils.schema import get_response_schema
from typing import Optional

class LLM:
    def __init__(self, model: gemini_model) -> None:
        self.api_url = self._get_url(model)
        self.headers = {
            "Content-Type": "application/json"
        }

    def _get_url(self, model: str) -> str:
        return f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={options.llm_api_key}"
    
    def get_payload(
            self, messages: list[AnyMessage], 
            system_prompt: Optional[str] = None, 
            schema: Optional[type] = None) -> GeminiPayload:

        return GeminiPayload(
            system_instruction=to_system_msg(system_prompt) if system_prompt else None,
            contents = messages_to_history(messages),
            generationConfig=GenerationConfig(
                responseMimeType="application/json",
                responseSchema=get_response_schema(schema),
            ) if schema else None
        )
    
    # RUN
    def run(self, payload: GeminiPayload):

        try:
            response = requests.post(self.api_url, headers=self.headers, data=payload.model_dump_json())
            response.raise_for_status()
            response_json = response.json()
            generated_text = response_json['candidates'][0]['content']['parts'][0]['text']

            return generated_text

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            if response and response.text:
                print(f"Response from API: {response.text} \n\n")
        