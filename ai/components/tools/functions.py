from ai.config.settings import options
from ai.models.tools import CrossrefResponse, TavilyResponse, WebResponse, ResearchResponse, WebResult, Item
from typing import Optional
import requests

# "web_search"
def web_search(query: str) -> Optional[WebResponse]:

    url = "https://api.tavily.com/search"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {options.tavily_api_key}"
    }
    data = {
        "query": query
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()

        print(f"TAVILY: {response.json()} \n\n")

        parsed = TavilyResponse.model_validate(response.json())

        results: list[WebResult] = []
        for result in parsed.results:

            results.append(WebResult(
                url=result.url,
                title=result.title,
                content=result.content
            ))
            
        return WebResponse(
            results=results
        )

    except Exception as e:
        print(f"ERROR in Tavily API: {str(e)}")

def research_papers(query: str) -> Optional[ResearchResponse]:

    url = f"https://api.staging.crossref.org/works?rows=5&select=title%2CURL&query={query}"

    try:
        response = requests.get(url=url)
        response.raise_for_status()

        print(f"CROSS REF API: {response.json()} \n\n")

        parsed = CrossrefResponse.model_validate(response.json())

        results: list[Item] = []
        for result in parsed.message.items:
            results.append(
                Item(
                    title=result.title,
                    URL=result.URL
                )
            )

        return ResearchResponse(
            results=results
        )

    except Exception as e:
        print(f"ERROR in CrossRef API: {str(e)}")

tool_manual = {
    "web_search": web_search,
    "research_papers": research_papers
}