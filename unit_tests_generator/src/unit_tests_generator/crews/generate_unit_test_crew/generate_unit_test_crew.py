from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
import os

from unit_tests_generator.tools.directory_list_tool import DirectoryListTool
from unit_tests_generator.tools.project_build_tool import ProjectBuildTool
from unit_tests_generator.tools.file_writer_tool import FileWriterTool
from crewai_tools import FileReadTool

from pydantic import BaseModel

class GenerateUnitTestState(BaseModel):
    generated_code: str = ""
    build_result: str = ""
    build_success: bool = False

@CrewBase
class GenerateUnitTestCrew():
    """GenerateUnitTestCrew crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    directoryListTool = DirectoryListTool()
    projectBuildTool = ProjectBuildTool()
    fileReadTool = FileReadTool()
    fileWriterTool = FileWriterTool()

    llm = LLM(
        model="gpt-4o-mini",
        api_key=os.getenv("OPENAI_API_KEY"),
    )

    def managers_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['managers_agent'], # type: ignore[index]
            verbose=True,
            llm=self.llm,
        )

    @agent
    def generate_unit_test_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['generate_unit_test_agent'], # type: ignore[index]
            verbose=True,
            tools=[self.directoryListTool, self.fileReadTool],
            llm=self.llm,
        )

    @agent
    def write_unit_test_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['write_unit_test_agent'], # type: ignore[index]
            verbose=True,
            llm=self.llm,
            tools=[self.fileWriterTool, self.fileReadTool],
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
    def generate_unit_test_task(self) -> Task:
        return Task(
            config=self.tasks_config['generate_unit_test_task'], # type: ignore[index]
            output_pydantic=GenerateUnitTestState,
        )

    @task
    def write_unit_test_task(self) -> Task:
        return Task(
            config=self.tasks_config['write_unit_test_task'], # type: ignore[index]
        )

    @task
    def build_project_task(self) -> Task:
        return Task(
            config=self.tasks_config['build_project_task'], # type: ignore[index]
            output_pydantic=GenerateUnitTestState,
        )

    @crew
    def crew(self) -> Crew:
        """Creates the GenerateUnitTestCrew crew"""

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.hierarchical,
            manager_agent=self.managers_agent(),
            verbose=True,
        )
