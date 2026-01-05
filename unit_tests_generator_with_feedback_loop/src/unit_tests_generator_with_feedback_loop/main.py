#!/usr/bin/env python
from typing import Optional

from crewai.flow.flow import Flow, listen, router, start
from pydantic import BaseModel

from unit_tests_generator_with_feedback_loop.crews.generate_unit_test_crew.generate_unit_test_crew import GenerateUnitTestCrew
from unit_tests_generator_with_feedback_loop.crews.build_project_crew.build_project_crew import BuildProjectCrew
from unit_tests_generator_with_feedback_loop.crews.git_checkout_and_commit_crew.git_checkout_and_commit_crew import GitCheckoutAndCommitCrew


class UnitTestFlowState(BaseModel):
    clone_path: str = "./Business_Management_Project/"
    service_package_name: str = "com.business.services"
    test_write_path: str = "./Business_Management_Project/src/test/java/com/business/services/"
    test_package_name: str = "com.business.services"
    coding_language: str = "Java"
    build_tool: str = "Maven"
    service_class_name: str = "OrderServices.java"
    generated_test_code: str = ""
    build_feedback: Optional[str] = None
    build_success: bool = False
    retry_count: int = 0
    max_retry: int = 3
    git_url: str = "https://github.com/SuhasKamate/Business_Management_Project.git"
    new_branch_name: str = "Agent-branch"
    commit_message: str = ""


class UnitTestGeneratorWithFeedbackFlow(Flow[UnitTestFlowState]):

    @start("retry")
    def generate_unit_test_flow_start(self):
        print("Generating Unit Tests")

    @listen(generate_unit_test_flow_start)
    def generate_unit_test(self):
        print(f"Generating unit test (Attempt {self.state.retry_count + 1}/{self.state.max_retry})")
        result = (
            GenerateUnitTestCrew()
            .crew()
            .kickoff(
                inputs={
                    "clone_path": self.state.clone_path,
                    "service_class_name": self.state.service_class_name,
                    "test_write_path": self.state.test_write_path,
                    "test_package_name": self.state.test_package_name,
                    "coding_language": self.state.coding_language,
                    "build_tool": self.state.build_tool,
                    "service_package_name": self.state.service_package_name,
                    "build_feedback": self.state.build_feedback or "",
                    "generated_test_code": self.state.generated_test_code,
                }
            )
        )
        print("Generated Unit Test Result:", result.raw)
        self.state.generated_test_code = result.raw

    @router(generate_unit_test)
    def build_and_evaluate(self):
        if self.state.retry_count >= self.state.max_retry:
            print(f"Max retry count ({self.state.max_retry}) exceeded")
            return "max_retry_exceeded"

        print("Building project and evaluating tests...")
        result = (
            BuildProjectCrew()
            .crew()
            .kickoff(
                inputs={
                    "clone_path": self.state.clone_path,
                    "build_tool": self.state.build_tool,
                }
            )
        )

        self.state.build_success = result.pydantic.build_success if hasattr(result, 'pydantic') else False
        self.state.build_feedback = result.pydantic.build_result if hasattr(result, 'pydantic') else result.raw

        print("Build Success:", self.state.build_success)
        print("Build Feedback:", self.state.build_feedback)

        self.state.retry_count += 1

        if self.state.build_success:
            return "completed"

        print("Build failed. Retrying with feedback...")
        return "retry"

    @listen("completed")
    def checkout_and_commit(self):
        print("Build successful! Checking out branch and committing changes...")
        self.state.commit_message = f"Added unit tests for {self.state.service_class_name}"

        result = (
            GitCheckoutAndCommitCrew()
            .crew()
            .kickoff(
                inputs={
                    "clone_path": self.state.clone_path,
                    "git_url": self.state.git_url,
                    "new_branch_name": self.state.new_branch_name,
                    "service_class_name": self.state.service_class_name,
                    "generated_test_code": self.state.generated_test_code,
                    "test_write_path": self.state.test_write_path,
                    "commit_message": self.state.commit_message,
                }
            )
        )
        print("Git Checkout and Commit Result:", result.raw)
        print(f"Successfully completed! Unit tests committed to branch: {self.state.new_branch_name}")

    @listen("max_retry_exceeded")
    def max_retry_exceeded_exit(self):
        print(f"Max retry count ({self.state.max_retry}) exceeded")
        print(f"Service Class: {self.state.service_class_name}")
        print(f"Last Generated Test Code:\n{self.state.generated_test_code}")
        print(f"Last Build Feedback:\n{self.state.build_feedback}")
        print("Flow ended without successful build. Please review the feedback and try again.")


def kickoff():
    unit_test_flow = UnitTestGeneratorWithFeedbackFlow()
    unit_test_flow.kickoff()


def plot():
    unit_test_flow = UnitTestGeneratorWithFeedbackFlow()
    unit_test_flow.plot()


if __name__ == "__main__":
    kickoff()
