from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from pydantic import BaseModel, Field
from typing import List, Optional

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
            verbose=True,
        )

    @agent
    def ipdai_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['ipdai_agent'],
            verbose=True,
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
            agents=[self.coordinator_agent()],
            tasks=[self.coordination_task()],    # collected automatically HAILEI requires coordination
            verbose=True,
        )

    def kickoff(self, course_request: dict):
        """Kick off the HAILEI crew"""
        return self.crew().kickoff(
            inputs={
                "course_request": course_request
            }
            )
