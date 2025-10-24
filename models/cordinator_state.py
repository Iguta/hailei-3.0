# models/coordinator_state.py
from pydantic import BaseModel, Field
from typing import List, Dict, Union, Optional
from models.course_request import CourseRequest

class Message(BaseModel):
    role: str
    content: str

class CoordinatorState(BaseModel):
    course_request: Optional[CourseRequest] = None
    conversation_history: List[Message] = Field(default_factory=list)
    last_user_message: Optional[str] = None

    def reset(self):
        """Reset state for a new session."""
        self.course_request = None
        self.conversation_history = []
        self.last_user_message = None

    def add_user_message(self, message: str):
        """Record a user message."""
        self.last_user_message = message
        self.conversation_history.append(Message(role="user", content=message))

    def add_assistant_message(self, message: str):
        """Record an assistant message."""
        self.conversation_history.append(Message(role="assistant", content=message))

    def formatted_history(self) -> str:
        """Returns conversation as plain text for LLM input."""
        return "\n".join([f"{m.role}: {m.content}" for m in self.conversation_history])
