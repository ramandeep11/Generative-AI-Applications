from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
import os

from unit_tests_generator_with_feedback_loop.tools.project_build_tool import ProjectBuildTool
from unit_tests_generator_with_feedback_loop.tools.directory_list_tool import DirectoryListTool

from pydantic import BaseModel

class BuildProjectState(BaseModel):
    build_result: str = ""
    build_success: bool = False

@CrewBase
class BuildProjectCrew():
    """BuildProjectCrew crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    projectBuildTool = ProjectBuildTool()
    directoryListTool = DirectoryListTool()

    llm = LLM(
        model="gpt-4o-mini",
        api_key=os.getenv("OPENAI_API_KEY"),
    )

    @agent
    def build_project_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['build_project_agent'], # type: ignore[index]
            verbose=True,
            tools=[self.projectBuildTool, self.directoryListTool],
            llm=self.llm,
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def build_project_task(self) -> Task:
        return Task(
            config=self.tasks_config['build_project_task'], # type: ignore[index]
            output_pydantic=BuildProjectState,
        )

    @crew
    def crew(self) -> Crew:
        """Creates the BuildProjectCrew crew"""

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )
