import operator
from pydantic import BaseModel
from typing import Annotated, List, Optional
# class SearchAssistantState(BaseModel):
#     query: str
#     context: Optional[str] = ""
#     answers: List[str] = []
#     feedback: Optional[str] = None

class SearchState(BaseModel):
    query: str
    context: Annotated[List[str], operator.add] = []
    answer: Optional[str] = None
