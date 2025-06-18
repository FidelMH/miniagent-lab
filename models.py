from  pydantic import BaseModel, Field, HttpUrl

class SearchResult(BaseModel):
    """
    Represents a search result with a title, URL, and description.
    """
    title: str = Field(..., description="The title of the search result")
    url: HttpUrl = Field(..., description="The URL of the search result")
    snippet: str = Field(..., description="A brief description of the search result")
    
class SearchResume(BaseModel):
    """
    Represents a summary of search results.
    """
    resultats: list[SearchResult] = Field(
        ...,
        description="A list of search results with their titles, URLs, and descriptions"
    )
    summary: str = Field(
        ...,
        description="A summary of the search results"
    )
