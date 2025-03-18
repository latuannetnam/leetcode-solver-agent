# Agent to help resolve LeetCode problems using the CrewAI API
from loguru import logger
logger.info("Loading library")
import os
import logging
import sys
# Get the root directory (assuming your notebook is in "test")
root_path = os.path.abspath(os.path.join(os.getcwd(), ".."))

# Add "src" folder to Python path
src_path = os.path.join(root_path, ".")
sys.path.append(src_path)

from crewai.knowledge.source.string_knowledge_source import StringKnowledgeSource
from datetime import datetime
from pydantic import BaseModel, Field
from crewai.project import CrewBase, agent, crew, task
from crewai.tools import BaseTool, tool
from crewai import Agent, Crew, Process, Task, LLM
import src.config as config
from typing import Type

from dotenv import load_dotenv
import argparse

logger.info("Library loaded")

load_dotenv(override=True)
config.init_trace()

VERBOSE = os.getenv('VERBOSE', 'false').lower() == 'true'
MAX_ITER=int(os.getenv('MAX_ITER', 5))

manager_llm = LLM(
    model="openai/gpt-4o-mini",
)

# llm = LLM(model="gemini/gemini-2.0-flash")

llm = LLM(
    # model="ollama/gemma3:4b",
    # model="ollama/gemma3:12b",
    # model="ollama/qwen2.5:7b",
    model="ollama/qwen2.5-coder:7b",
    # model="ollama/llama3.2:3b",
    # base_url="http://localhost:11434",
    max_tokens=8192,
    reasoning_effort="high",    
)

@CrewBase
class LeetCodeCrew():
    # Dot not use @agent decorator here, as this is a manager agent
    def crew_manager(self) -> Agent:
        return Agent(
            role="Crew Manager",
            goal="Manage the team to complete the task in the best way possible.",
            backstory="""You are a seasoned manager with a knack for getting the best out of your team.
            You are also known for your ability to delegate work to the right people, and to ask the right questions to get the best out of your team.
            Even though you don't perform tasks by yourself, you have a lot of experience in the field, which allows you to properly evaluate the work of your team members.""",
            llm=llm,
            max_iter=MAX_ITER,
            verbose=VERBOSE,
        )

    @agent
    def architect_agent(self) -> Agent:
        return Agent(
            role='Software Architect',
            goal='Design algorithm to solve the LeetCode problem. ',
            backstory="You are an expert in algorithm design and problem-solving. Your mission is to analyze the problem and create an efficient algorithm to solve it. ",
            llm=llm,
            max_iter=MAX_ITER,
            verbose=VERBOSE,
        )

    @agent
    def code_agent(self) -> Agent:
        return Agent(
            role='Software Engineer',
            goal='Write code to solve the LeetCode problem based on the provided algorithm. ',
            backstory="You are a skilled software engineer with expertise in coding and debugging. Your mission is to write clean, efficient, and well-documented code. ",
            llm=llm,
            max_iter=MAX_ITER,
            verbose=VERBOSE,
        )

    @agent
    def test_agent(self) -> Agent:
        return Agent(
            role='Software Tester',
            goal='Test the code to ensure it solves the LeetCode problem correctly. ',
            backstory="You are an experienced Tester with a keen eye for detail. Your mission is to write comprehensive test cases and run them to identify any bugs or issues in the code. ",
            llm=llm,
            max_iter=MAX_ITER,
            verbose=VERBOSE,
        )

    @agent
    def qa_agent(self) -> Agent:
        return Agent(
            role='QA Specialist',
            goal='Review the codeto ensure quality and suggest improvements. ',
            backstory="You are an experienced quality assurance engineer with a deep understanding of coding best practices and testing methodologies. Your mission is to review the code, identify potential issues, and suggest improvements to enhance the overall quality of the solution. ",
            llm=llm,
            max_iter=MAX_ITER,
            verbose=VERBOSE,
        )

    # @agent
    def report_agent(self) -> Agent:
        return Agent(
            role='Reporter',
            goal='Report the final code and test cases, including any suggestions for improvements',
            backstory="You are a detailed-oriented reporter who reports the final code and test cases, including any suggestions for improvements.",
            llm=llm,
            max_iter=MAX_ITER,
            verbose=VERBOSE,
        )

    @task
    def analyze_problem_task(self) -> Task:
        return Task(
            description="Analyze the LeetCode problem and understand its requirements:\n\n{leetcode_problem}",
            expected_output="An analysis of the problem, including its requirements and constraints.",
            agent=self.architect_agent()
        )

    @task
    def create_algorithm_task(self) -> Task:
        return Task(
            description="""Create an efficient algorithm to solve the LeetCode problem.
            - The algorithm should be well-defined and efficient.
            - The algorithm should be easy to understand and implement.
            - The algorithm should be optimized for performance and memory.""",
            expected_output="""A well-defined algorithm that efficiently solves the LeetCode problem.
               - Do not generate any code, just the algorithm.""",
            agent=self.architect_agent()
        )

    @task
    def write_code_task(self) -> Task:
        return Task(
            description="""Implement the algorithm by writing Python code to solve the LeetCode problem.
            - Use only native Python libraries.
            - Document the code thoroughly, explaining the functionality of each line.""",
            expected_output="Well-documented, efficient Python code adhering to the provided algorithm.",
            agent=self.code_agent()
        )

    @task
    def write_test_cases_task(self) -> Task:
        return Task(
            description="Write comprehensive test cases to verify the correctness of the code.",
            expected_output="Test cases that cover all edge cases and ensure the code works as intended.",
            agent=self.test_agent()
        )

    @task
    def run_test_cases_task(self) -> Task:
        return Task(
            description="Run the test cases and identify any bugs or issues in the code.",
            expected_output="A report of any bugs or issues found during testing.",
            agent=self.test_agent()
        )

    @task
    def review_code_task(self) -> Task:
        return Task(
            description="""Review the code for coding style, efficiency, and potential issues.
            - the code must use native Python libraries
            - the code must be clean and efficient
            - the code must be well-documented
            - the code must follow the provided algorithm
            - the code must be optimized for performance and memory""",
            expected_output="Feedback on the code's structure and style.",
            agent=self.qa_agent()
        )

    # @task
    def review_test_cases_task(self) -> Task:
        return Task(
            description="Review the test cases for completeness and effectiveness.",
            expected_output="Recommendations for improving the test cases.",
            agent=self.qa_agent()
        )

    @task
    def suggest_improvements_task(self) -> Task:
        return Task(
            description="""Suggest improvements to the code to enhance the overall quality of the solution.
            - The code should be optimized for performance and readability.""",
            expected_output="Suggestions for quality and performance improvements.",
            agent=self.qa_agent()
        )
    
    @task
    def finalize_code_task(self) -> Task:
        return Task(
            description="Finalize the code based on the feedback received.",
            expected_output="Finalized code.",
            agent=self.code_agent()
        )
    
    # @task
    def report_task(self) -> Task:
        return Task(
            description="Report the final code and test cases, including any suggestions for improvements.",
            expected_output="""
             1. Final Code
             2. Test Cases"
            """,
            agent=self.report_agent()
        )


    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            manager_agent=self.crew_manager(),
            # manager_llm=manager_llm,
            process=Process.hierarchical,
            verbose=VERBOSE
        )

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", type=str, required=True, help="Path to the LeetCode problem file")
    args = parser.parse_args()
    
    with open(args.file, "r") as f:
        leetcode_problem = f.read()
    
    leetcode_crew = LeetCodeCrew().crew()
    result = leetcode_crew.kickoff(inputs={"leetcode_problem": leetcode_problem})
    logger.info(f"Final result: {result}")
