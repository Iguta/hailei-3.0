# models/course_request.py
from pydantic import BaseModel, Field
from typing import List, Optional

class CourseModule(BaseModel):
    title: str = Field(..., min_length=5, description="The title of the module")
    description: str = Field(..., min_length=10, description="Short summary of the module")
    learning_objectives: List[str] = Field(..., description="List of learning objectives for the module")

class CourseFoundation(BaseModel):
    modules: List[CourseModule] = Field(..., description="List of modules for the course")


class CourseRequest(BaseModel):
    course_title: str = Field(..., min_length=5, description="The title of the course")
    course_description: str = Field(..., min_length=15, description="Detailed course description")
    course_credits: int = Field(..., gt=0, description="Number of credits for the course")
    course_duration_weeks: int = Field(..., gt=0, description="Course duration in weeks")
    course_level: str = Field(..., description="Academic level (e.g., Undergraduate, Graduate)")
    course_expectations: str = Field(..., min_length=10, description="What students are expected to achieve")

