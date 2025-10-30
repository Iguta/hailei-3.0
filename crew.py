from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from pydantic import BaseModel, Field
from typing import List, Optional
from frameworks import KDKA_FRAMEWORK, PRRR_FRAMEWORK
from tools.blooms_taxonomy_tool import blooms_taxonomy_tool
from models.cordinator_state import CoordinatorState

# ---------------------
# Define Pydantic schemas
# ---------------------
class CourseModule(BaseModel):
    title: str
    description: Optional[str] = None
    learning_objectives: Optional[List[str]] = None


class CourseFoundation(BaseModel):
    course_title: str
    course_description: str
    credits: int
    duration_weeks: int
    level: str
    expectations: str
    modules: List[CourseModule]


class CourseAuditReport(BaseModel):
    ethical_compliance: bool
    udl_compliance: bool
    accessibility_passed: bool
    notes: str

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
            verbose=True
        )

    @agent
    def ipdai_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['ipdai_agent'],
            verbose=True,
            tools=[blooms_taxonomy_tool]
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
        )

    @agent
    def ethosai_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['ethosai_agent'],
            verbose=True,
        )

    @agent
    def searchai_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['searchai_agent'],
            verbose=True,
        )

    # ---------- TASKS ----------
    @task
    def coordination_task(self) -> Task:
        return Task(
            config=self.tasks_config['coordination_task'],
            verbose=True,
            # output_pydantic=CourseFoundation,
        )

    @task
    def instructional_planning_task(self) -> Task:
        return Task(
            config=self.tasks_config['instructional_planning_task'],
            verbose=True,
            output_pydantic=CourseFoundation,
        )

    @task
    def ethical_audit_task(self) -> Task:
        return Task(
            config=self.tasks_config['ethical_audit_task'],
            verbose=True,
            output_pydantic=CourseAuditReport,
        )

    # ---------- CREW ----------
    @crew
    def crew(self) -> Crew:
        """Creates the HAILEI agent crew"""
        return Crew(
            agents=[self.ipdai_agent()],
            tasks=[self.coordination_task(), self.instructional_planning_task() ],  
            process=Process.hierarchical,
            manager_agent=self.coordinator_agent(),
            verbose=False,
            memory=True,
        )

    def kickoff(self, coordinator_state: CoordinatorState):
        """Kick off the HAILEI crew"""
        course_request = coordinator_state.course_request
        return self.crew().kickoff(
            inputs={
                "course_request": course_request.dict(), #conver from Pydantic to dict,
                "course_title": course_request.course_title,
                "course_description": course_request.course_description,
                "course_credits": course_request.course_credits,
                "course_duration_weeks": course_request.course_duration_weeks,
                "course_level": course_request.course_level,
                "course_expectations": course_request.course_expectations,
        

                # other fields for the task
                "conversation_history": coordinator_state.conversation_history,
                "last_user_message": coordinator_state.last_user_message,

                #framework data
                "kdka_framework": KDKA_FRAMEWORK,
                "prrr_framework": PRRR_FRAMEWORK,
            }
            )
