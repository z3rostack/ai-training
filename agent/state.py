from typing import Literal, NotRequired, TypedDict, Any
from pydantic import BaseModel


Intent = Literal[  # new code
    "northwind_query",  # new code
    "document_search",  # new code
    "reporting",  # new code
    "out_of_scope",  # new code
    "security_breach",  # new code
]  # new code

class IntentResult(BaseModel):
    intent: Intent
    reason: str

class AgentState(TypedDict):
    question: str
    intent: NotRequired[IntentResult]

StateUpdate = dict[str, Any]