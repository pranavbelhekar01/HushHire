from typing import List
from langchain_core.pydantic_v1 import BaseModel, Field


class Candidate(BaseModel):
    name: str = Field(description="First name and last name of the candidate.")
    email: str = Field(description="Email address of the candidate.")
    phone: str = Field(description="Contact number with country code of the candidate.")
    location: str = Field(description="City and state where the candidate resides.")
    degree: List[str] = Field(description="List of the candidate's college degrees.")
    college: List[str] = Field(description="List of all the colleges candidate went to")
    skills: List[str] = Field(description="List of technical skills of the user.")
    companies: List[str] = Field(
        description="List only the name of the companies the user has worked at."
    )
    roles: List[str] = Field(
        description="List all the job roles of the user at previous companies."
    )
    degree_year: int = Field(
        description="The year in which candidate completed their degree."
    )
    experience: float = Field(
        description="Number of years of professional experience of the candidate"
    )