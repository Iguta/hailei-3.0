from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from frameworks import KDKA_FRAMEWORK, PRRR_FRAMEWORK
from tools.blooms_taxonomy_tool import blooms_taxonomy_tool
from models.models import (
    CoordinatorState,
    CourseFoundation,
    CourseAuditReport,
    CourseContent,
    CourseTechnicalDesign,
    CourseContentReview,
    CourseSearchReport,
)


# ---------------------
# Define HAILEI Crew
# ---------------------
@CrewBase
class HaileiCrew():
    """HAILEI (Higher AI-Assisted Learning & Educational Intelligence) Crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # ---------- AGENTS ----------
    @agent
    def coordinator_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['hailei4t_coordinator_agent'],
            verbose=True,
        )

    @agent
    def ipdai_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['ipdai_agent'],
            verbose=True,
            tools=[blooms_taxonomy_tool],
        )

    @agent
    def cauthai_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['cauthai_agent'],
            verbose=True,
        )

    @agent
    def tfdai_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['tfdai_agent'],
            verbose=True,
        )

    @agent
    def editorai_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['editorai_agent'],
            verbose=True,
            output_pydantic=CourseContent,
        )

    @agent
    def ethosai_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['ethosai_agent'],
            verbose=True,
            output_pydantic=CourseAuditReport,
        )

    @agent
    def searchai_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['searchai_agent'],
            verbose=True,
            output_pydantic=CourseSearchReport,
        )

    # ---------- TASKS ----------
    @task
    def coordination_task(self) -> Task:
        return Task(
            config=self.tasks_config['coordination_task'],
            verbose=True,
        )

    @task
    def instructional_planning_task(self) -> Task:
        return Task(
            config=self.tasks_config['instructional_planning_task'],
            verbose=True,
            output_pydantic=CourseFoundation,
        )
    
    @task
    def content_authoring_task(self) -> Task:
        return Task(
            config=self.tasks_config['content_authoring_task'],
            verbose=True,
            output_pydantic=CourseContent,
        )
    @task
    def technical_design_task(self) -> Task:
        return Task(
            config=self.tasks_config['technical_design_task'],
            verbose=True,
            output_pydantic=CourseTechnicalDesign,
        )
    @task
    def content_review_task(self) -> Task:
        return Task(
            config=self.tasks_config['content_review_task'],
            verbose=True,
            output_pydantic=CourseContentReview,
        )

    @task
    def ethical_audit_task(self) -> Task:
        return Task(
            config=self.tasks_config['ethical_audit_task'],
            verbose=True,
            output_pydantic=CourseAuditReport,
        )
    
    @task
    def searchai_task(self) -> Task:
        return Task(
            config=self.tasks_config['searchai_task'],
            verbose=True,
            output_pydantic=CourseSearchReport,
        )
    

    # ==================================================
    # PHASE 1: Coordinator Crew (before approval)
    # ==================================================
    @crew
    def coordination_crew(self) -> Crew:
        """Crew responsible for course request refinement only."""
        return Crew(
            agents=[self.coordinator_agent()],
            tasks=[self.coordination_task()],
            # process=Process.hierarchical,
            # manager_agent=self.coordinator_agent(),
            verbose=True,
            memory=True,
        )

    # ==================================================
    # PHASE 2: Design Crew (after approval)
    # ==================================================
    @crew
    def design_crew(self) -> Crew:
        """Crew responsible for instructional planning and audits after approval."""
        return Crew(
            agents=[
                self.ipdai_agent(),
                self.cauthai_agent(),
                self.tfdai_agent(),
                self.editorai_agent(),
                self.ethosai_agent(),
                self.searchai_agent(),
            ],
            tasks=[
                self.instructional_planning_task(),
                self.content_authoring_task(),
                self.technical_design_task(),
                self.content_review_task(),
                self.ethical_audit_task(),
                self.searchai_task(),
            ],
            process=Process.sequential,
            verbose=True,
            memory=True,
        )

    # ==================================================
    # Kickoff Methods
    # ==================================================
    def kickoff_coordination(self, coordinator_state: CoordinatorState):
        """Run the Coordinator refinement phase."""
        course_request = coordinator_state.course_request
        return self.coordination_crew().kickoff(
            inputs={
                "course_request": course_request.dict(),
                "course_title": course_request.course_title,
                "course_description": course_request.course_description,
                "course_credits": course_request.course_credits,
                "course_duration_weeks": course_request.course_duration_weeks,
                "course_level": course_request.course_level,
                "course_expectations": course_request.course_expectations,
                "conversation_history": coordinator_state.formatted_history(),
                "last_user_message": coordinator_state.last_user_message,
                "kdka_framework": KDKA_FRAMEWORK,
                "prrr_framework": PRRR_FRAMEWORK,
            }
        )

    def kickoff_design_phase(self, coordinator_state: CoordinatorState):
        """Run the instructional design phase after approval."""
        course_request = coordinator_state.course_request
        return self.design_crew().kickoff(
            inputs={
                "course_request": course_request.dict(),
                "course_title": course_request.course_title,
                "course_description": course_request.course_description,
                "course_credits": course_request.course_credits,
                "course_duration_weeks": course_request.course_duration_weeks,
                "course_level": course_request.course_level,
                "course_expectations": course_request.course_expectations,
                "conversation_history": coordinator_state.formatted_history(),
                "last_user_message": coordinator_state.last_user_message,
                "lms_platform": "To be determined",  # Default value, can be customized later
                "kdka_framework": KDKA_FRAMEWORK,
                "prrr_framework": PRRR_FRAMEWORK,
            }
        )
