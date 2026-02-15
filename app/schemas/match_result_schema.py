from pydantic import BaseModel

class MatchResult(BaseModel):
    score: float              # 0.0 -> 1.0
    percentage: float         # 0 -> 100
    decision: str             # ACCEPT / REVIEW / REJECT
    details: dict             # explainability
