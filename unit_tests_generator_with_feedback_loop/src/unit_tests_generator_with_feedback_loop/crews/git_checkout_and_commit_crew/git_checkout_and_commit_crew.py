from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
import os

from unit_tests_generator_with_feedback_loop.tools.git_tool import GitTool
from unit_tests_generator_with_feedback_loop.tools.git_checkout_tool import GitCheckoutTool

@CrewBase
class GitCheckoutAndCommitCrew():
    """GitCheckoutAndCommitCrew crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    llm = LLM(
        model="gpt-4o-mini",
        api_key=os.getenv("OPENAI_API_KEY"),
    )

    @agent
    def git_checkout_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['git_checkout_agent'], # type: ignore[index]
            verbose=True,
            llm=self.llm,
            tools=[GitCheckoutTool()],
        )

    @agent
    def git_commit_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['git_commit_agent'], # type: ignore[index]
            verbose=True,
            llm=self.llm,
            tools=[GitTool()],
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def git_checkout_task(self) -> Task:
        return Task(
            config=self.tasks_config['git_checkout_task'], # type: ignore[index]
        )

    @task
    def git_commit_task(self) -> Task:
        return Task(
            config=self.tasks_config['git_commit_task'], # type: ignore[index]
        )

    @crew
    def crew(self) -> Crew:
        """Creates the GitCheckoutAndCommitCrew crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
