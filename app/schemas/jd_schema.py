from pydantic import BaseModel
from typing import List, Optional


class JDSchema(BaseModel):
    skills: List[str]
    title: str
    min_years_experience: float
    max_years_experience: Optional[float] = None
