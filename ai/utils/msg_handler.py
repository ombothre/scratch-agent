from ai.models.message import AnyMessage
from ai.models.payload import Content, Part

def messages_to_history(messages: list[AnyMessage]) -> list[Content]:

    contents: list[Content] = []
    for message in messages:

        contents.append(Content(
            role=message.by,
            parts=[
                Part(
                    text=message.content
                )
            ]
        ))
    
    return contents