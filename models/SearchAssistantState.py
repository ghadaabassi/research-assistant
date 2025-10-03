from dataclasses import field
import operator
from pydantic import BaseModel
from typing import Annotated, List, Optional

class SearchState(BaseModel):
    query: str
    sub_topics: List[str] = []
    context: Annotated[List[str], operator.add] = []
    answer: Optional[str] = None
    human_feedback: Optional[str] = None
