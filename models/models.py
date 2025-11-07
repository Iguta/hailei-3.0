# models/models.py
# Unified data models for HAILEI course design system

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

# ============================================================================
# SECTION 1: Coordinator & State Management
# ============================================================================

class Message(BaseModel):
    """Message in conversation history."""
    role: str
    content: str


class CoordinatorState(BaseModel):
    """State management for the coordinator phase."""
    course_request: Optional['CourseRequest'] = None
    conversation_history: List[Message] = Field(default_factory=list)
    last_user_message: Optional[str] = None
    approved: bool = False

    def reset(self):
        """Reset state for a new session."""
        self.course_request = None
        self.conversation_history = []
        self.last_user_message = None
        self.approved = False

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


# ============================================================================
# SECTION 2: Course Request (Initial Input)
# ============================================================================

class CourseRequest(BaseModel):
    """Initial course request from the educator."""
    course_title: str = Field(..., min_length=5, description="The title of the course")
    course_description: str = Field(..., min_length=15, description="Detailed course description")
    course_credits: int = Field(..., gt=0, description="Number of credits for the course")
    course_duration_weeks: int = Field(..., gt=0, description="Course duration in weeks")
    course_level: str = Field(..., description="Academic level (e.g., Undergraduate, Graduate)")
    course_expectations: str = Field(..., min_length=10, description="What students are expected to achieve")


# ============================================================================
# SECTION 3: Shared Components (used across multiple models)
# ============================================================================

class LearningObjective(BaseModel):
    """Learning objective with Bloom's taxonomy level."""
    statement: str = Field(..., description="The statement of the learning objective")
    bloom_level: Optional[str] = Field(
        None,
        description="Bloom's level (e.g., Remember/Understand/Apply/Analyze/Evaluate/Create)",
    )


class ModuleResource(BaseModel):
    """Resource associated with a course module."""
    title: str = Field(..., description="The title of the resource")
    url: Optional[str] = Field(None, description="The URL of the resource")
    type: Optional[str] = Field(
        None,
        description="The type of the resource (reading, video, dataset, tool, etc.)",
    )


class KDKAAlignment(BaseModel):
    """KDKA structure per module."""
    knowledge: List[str] = Field(default_factory=list, description="Facts/concepts/skills")
    delivery: List[str] = Field(default_factory=list, description="Modalities/methods")
    context: List[str] = Field(default_factory=list, description="Authentic scenarios & constraints")
    assessment: List[str] = Field(default_factory=list, description="Formative/summative checks")


class PRRRSignals(BaseModel):
    """PRRR infusion prompts captured per module."""
    personal: Optional[str] = Field(None, description="Personal dimension signal")
    relatable: Optional[str] = Field(None, description="Relatable dimension signal")
    relative: Optional[str] = Field(None, description="Relative dimension signal")
    real_world: Optional[str] = Field(None, description="Real-world dimension signal")


# ============================================================================
# SECTION 4: IPDAi Output Models
# ============================================================================

class CourseModule(BaseModel):
    """Simplified module structure for CourseFoundation (used by IPDAi)."""
    title: str = Field(..., description="The title of the module")
    description: str = Field(..., description="The description of the module")
    learning_objectives: List[LearningObjective] = Field(..., description="The learning objectives of the module")


class CourseFoundation(BaseModel):
    """Course foundation created by IPDAi (instructional planning)."""
    course_title: str = Field(..., description="The title of the course")   
    course_description: str = Field(..., description="The description of the course")
    credits: int = Field(..., description="The credits of the course")
    duration_weeks: int = Field(..., description="The duration of the course in weeks")
    level: str = Field(..., description="The level of the course")
    expectations: str = Field(..., description="The expectations of the course")
    modules: List[CourseModule] = Field(..., description="The modules of the course")


class CourseAuditReport(BaseModel):
    """Ethical audit report from EthosAi."""
    ethical_compliance: bool = Field(..., description="Whether the course is ethically compliant e.g., privacy, bias, fairness")
    notes: str = Field(..., description="Notes on the ethical audit")


# ============================================================================
# SECTION 5: Worker Agent Output Models
# ============================================================================

class WeeklyModule(BaseModel):
    """Detailed weekly module structure (used by CAuthAi and others)."""
    week_number: int = Field(..., description="The week number of the module")
    title: str = Field(..., description="The title of the module")
    overview: Optional[str] = Field(None, description="The overview of the module")
    learning_objectives: List[LearningObjective] = Field(default_factory=list, description="The learning objectives of the module")
    activities: List[str] = Field(default_factory=list, description="The activities of the module e.g reading, writing, problem solving, etc.")
    assessments: List[str] = Field(default_factory=list, description="The assessments of the module e.g multiple choice, essay, project, etc.")
    resources: List[ModuleResource] = Field(default_factory=list, description="The resources of the module")
    kdka: KDKAAlignment = Field(default_factory=KDKAAlignment, description="KDKA-aligned elements for this module")
    prrr: PRRRSignals = Field(default_factory=PRRRSignals, description="PRRR signals infused in this module")


class CourseContent(BaseModel):
    """Course content output from CAuthAi (content_authoring_task)."""
    course_title: str
    course_description: str
    duration_weeks: int
    level: str
    tlos: List[LearningObjective] = Field(default_factory=list)
    elos_by_tlo: Dict[str, List[LearningObjective]] = Field(default_factory=dict)
    weekly_modules: List[WeeklyModule] = Field(default_factory=list)
    syllabus_markdown: Optional[str] = None
    kdka_overview: Optional[str] = Field(None, description="Global notes on KDKA alignment across the course")
    prrr_overview: Optional[str] = Field(None, description="Global notes on PRRR infusion across the course")


class LMSIntegration(BaseModel):
    """LMS integration details."""
    lms_platform: Optional[str] = None
    navigation_structure: List[str] = Field(default_factory=list)
    feature_mapping: Dict[str, Any] = Field(default_factory=dict)  # quizzes, discussions, gradebook
    integrations: List[str] = Field(default_factory=list)  # SCORM/LTI/tools
    accessibility_notes: Optional[str] = None


class CourseTechnicalDesign(BaseModel):
    """Technical design output from TFDAi (technical_design_task)."""
    course_title: str = Field(..., description="The title of the course")
    implementation_plan_markdown: str = Field(..., description="The implementation plan of the course in Markdown")
    lms: LMSIntegration = Field(default_factory=LMSIntegration, description="The LMS integration details")
    timeline_weeks: List[str] = Field(default_factory=list, description="The timeline of the course in weeks")


class EditFinding(BaseModel):
    """Edit finding from EditorAi."""
    area: str = Field(..., description="The area of the edit finding e.g., Clarity, Tone, Accessibility, Consistency, Grammar")
    issue: str = Field(..., description="The issue of the edit finding e.g., content is not clear, tone is not professional, accessibility is not compliant, consistency is not maintained")
    recommendation: str = Field(..., description="The recommendation for the edit finding e.g., improve clarity, use professional tone, ensure accessibility compliance, maintain consistency, improve grammar")


class CourseContentReview(BaseModel):
    """Content review output from EditorAi (content_review_task)."""
    udl_compliance: bool = Field(..., description="Whether the course is UDL compliant")
    accessibility_passed: bool = Field(..., description="Whether the course is accessible")
    summary_markdown: Optional[str] = Field(None, description="The summary of the content review in Markdown")
    findings: List[EditFinding] = Field(default_factory=list, description="The findings of the content review")
    accessibility_checks: List[str] = Field(default_factory=list, description="The accessibility checks of the content review")
    blooms_alignment_notes: Optional[str] = Field(None, description="The blooms alignment notes of the content review")
    


class SearchHit(BaseModel):
    """Search result hit from SearchAi."""
    title: str
    url: Optional[str] = Field(None, description="The URL of the resource")
    description: Optional[str] = None
    relevance_reason: Optional[str] = None


class CourseSearchReport(BaseModel):
    """Search report output from SearchAi (searchai_task)."""
    query: Optional[str] = None
    resources: List[SearchHit] = Field(default_factory=list)
    curation_notes: Optional[str] = None


# class CourseDesign(BaseModel):
#     """ Final educator facing course design from the HAILEI4T Course Design Crew. """
#     course_design: CourseContent,
#     course_technical_design: CourseTechnicalDesign,
#     course_editor_review: CourseContentReview,
#     course_ethical_audit: CourseAuditReport,
#     course_search_report: CourseSearchReport,
#     manager_remarks: Optional[str] = Field(None, description="short remarks from the manager about the course design")

# Forward reference resolution
CoordinatorState.model_rebuild()

