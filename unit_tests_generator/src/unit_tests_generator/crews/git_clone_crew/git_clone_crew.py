from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
import os

from unit_tests_generator.tools.git_clone_tool import GitCloneTool
from unit_tests_generator.tools.directory_list_tool import DirectoryListTool
from unit_tests_generator.tools.project_build_tool import ProjectBuildTool

@CrewBase
class GitCloneCrew():
    """GitCloneCrew crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    llm = LLM(
        model="gpt-4o-mini",
        api_key=os.getenv("OPENAI_API_KEY"),
    )

    GitCloneTool = GitCloneTool()
    DirectoryListTool = DirectoryListTool()
    ProjectBuildTool = ProjectBuildTool()

    @agent
    def git_cloner_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['git_cloner_agent'], # type: ignore[index]
            verbose=True,
            llm=self.llm,
            tools=[self.GitCloneTool, self.DirectoryListTool],
        )

    @agent
    def project_builder_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['project_builder_agent'], # type: ignore[index]
            verbose=True,
            llm=self.llm,
            tools=[self.DirectoryListTool, self.ProjectBuildTool],
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def git_clone_task(self) -> Task:
        return Task(
            config=self.tasks_config['git_clone_task'], # type: ignore[index]
        )

    @task
    def project_build_task(self) -> Task:
        return Task(
            config=self.tasks_config['project_build_task'], # type: ignore[index]
        )

    @crew
    def crew(self) -> Crew:
        """Creates the GitCloneCrew crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
