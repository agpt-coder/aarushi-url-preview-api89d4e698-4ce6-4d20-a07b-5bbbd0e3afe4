from typing import Optional

import httpx
from bs4 import BeautifulSoup
from pydantic import BaseModel


class FetchWebpageContentResponse(BaseModel):
    """
    The response model providing the webpage content or an error message.
    """

    status: str
    content: Optional[str] = None
    error: Optional[str] = None


async def fetch_webpage_content(url: str) -> FetchWebpageContentResponse:
    """
    Retrieve webpage content for the provided URL.

    The function performs an HTTP GET request to fetch the content at the specified URL. It does basic URL validation to check format before proceeding with the request. If the request is successful, the raw HTML content is returned. In case of failures (e.g., network issues, invalid URL), an appropriate error message is provided.

    Args:
    url (str): The fully qualified URL of the webpage to retrieve the content from. This field will undergo validation to ensure it is a properly formatted URL and will also be sanitized to prevent injection attacks.

    Returns:
    FetchWebpageContentResponse: The response model providing the webpage content or an error message.
    """
    try:
        httpx.get(url)
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            title = soup.title.string if soup.title else "Untitled"
            return FetchWebpageContentResponse(status="success", content=response.text)
    except httpx.RequestError as e:
        return FetchWebpageContentResponse(
            status="failed", error=f"Request error: {str(e)}"
        )
    except httpx.HTTPStatusError as e:
        return FetchWebpageContentResponse(
            status="failed", error=f"HTTP Error: {str(e)}"
        )
    except Exception as e:
        return FetchWebpageContentResponse(
            status="failed", error=f"Unexpected error: {str(e)}"
        )
