from pydantic import BaseModel
from typing import List


class CVSchema(BaseModel):
    skills: List[str]
    title: str
    years_experience: float
