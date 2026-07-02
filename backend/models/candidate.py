from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Candidate:
    candidate_id: str
    name: str
    skills: List[str]
    experience_years: float
    education: Optional[str]
    location: Optional[str]
    resume_text: str