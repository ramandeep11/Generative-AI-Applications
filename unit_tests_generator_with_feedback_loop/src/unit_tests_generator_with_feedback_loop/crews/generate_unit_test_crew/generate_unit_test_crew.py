from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
import os

from unit_tests_generator_with_feedback_loop.tools.directory_list_tool import DirectoryListTool
from unit_tests_generator_with_feedback_loop.tools.file_writer_tool import FileWriterTool
from crewai_tools import FileReadTool

@CrewBase
class GenerateUnitTestCrew():
    """GenerateUnitTestCrew crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    directoryListTool = DirectoryListTool()
    fileReadTool = FileReadTool()
    fileWriterTool = FileWriterTool()

    llm = LLM(
        model="gpt-4o-mini",
        api_key=os.getenv("OPENAI_API_KEY"),
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

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def generate_unit_test_task(self) -> Task:
        return Task(
            config=self.tasks_config['generate_unit_test_task'], # type: ignore[index]
        )

    @task
    def write_unit_test_task(self) -> Task:
        return Task(
            config=self.tasks_config['write_unit_test_task'], # type: ignore[index]
        )

    @crew
    def crew(self) -> Crew:
        """Creates the GenerateUnitTestCrew crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
