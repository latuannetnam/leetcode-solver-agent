from loguru import logger
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
import os
from dotenv import load_dotenv
load_dotenv(override=True)


# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class LeetcodeSolver():
    """Leetcodesolver crew"""

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    def __init__(self):
        self.llm = self.load_llm_model()
        self.MAX_ITER = int(os.getenv('MAX_ITER', 5))
        self.VERBOSE = os.getenv('VERBOSE', 'false').lower() == 'true'

    def load_llm_model(self):
        LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")
        MODEL = os.getenv("MODEL", "gpt-4o-mini")
        MODEL_TEMPERATURE = float(os.getenv("MODEL_TEMPERATURE", 0.0))
        CONTEXT_WINDOW_SIZE = 0
        if LLM_PROVIDER == "google":
            model = f"gemini/{MODEL}"
        elif LLM_PROVIDER == "ollama":
            model = f"ollama/{MODEL}"
            CONTEXT_WINDOW_SIZE = int(os.getenv("CONTEXT_WINDOW_SIZE", 8192))

        elif LLM_PROVIDER == "openai":
            model = f"openai/{MODEL}"

        else:
            raise ValueError(
                f"Unsupported LLM provider: {LLM_PROVIDER}")
        
        logger.info(f"Loading LLM model: {model}")
        if CONTEXT_WINDOW_SIZE>0:
            llm = LLM(
                model=model,
                temperature=MODEL_TEMPERATURE,
                max_tokens=CONTEXT_WINDOW_SIZE,                
            )
        else:
            llm = LLM(
                model=model,
                temperature=MODEL_TEMPERATURE,					
            )
        
        return llm

    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    def crew_manager(self) -> Agent:
        return Agent(
            config=self.agents_config['crew_manager'],
            llm=self.llm,
            max_iter=self.MAX_ITER,
            verbose=self.VERBOSE
        )

    @agent
    def software_architect(self) -> Agent:
        return Agent(
            config=self.agents_config['software_architect'],
            llm=self.llm,
            max_iter=self.MAX_ITER,
            verbose=self.VERBOSE
        )

    @agent
    def sofware_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['software_engineer'],
            llm=self.llm,
            max_iter=self.MAX_ITER,
            verbose=self.VERBOSE
        )

    @agent
    def tester(self) -> Agent:
        return Agent(
            config=self.agents_config['tester'],
            llm=self.llm,
            max_iter=self.MAX_ITER,
            verbose=self.VERBOSE
        )

    @agent
    def qa_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config['qa_specialist'],
            llm=self.llm,
            max_iter=self.MAX_ITER,
            verbose=self.VERBOSE
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def analyze_problem_task(self) -> Task:
        return Task(
            config=self.tasks_config['analyze_problem_task'],
        )

    @task
    def create_algorithm_task(self) -> Task:
        return Task(
            config=self.tasks_config['create_algorithm_task'],
        )

    @task
    def write_code_task(self) -> Task:
        return Task(
            config=self.tasks_config['write_code_task'],
        )

    @task
    def write_test_cases_task(self) -> Task:
        return Task(
            config=self.tasks_config['write_test_cases_task'],
        )

    @task
    def run_test_cases_task(self) -> Task:
        return Task(
            config=self.tasks_config['run_test_cases_task'],
        )

    @task
    def review_code_task(self) -> Task:
        return Task(
            config=self.tasks_config['review_code_task'],
        )

    @task
    def suggest_improvements_task(self) -> Task:
        return Task(
            config=self.tasks_config['suggest_improvements_task'],
        )

    @task
    def finalize_code_task(self) -> Task:
        return Task(
            config=self.tasks_config['finalize_code_task'],
        )

    @crew
    def crew(self) -> Crew:
        """Creates the LeetcodeSolver crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.hierarchical,
            manager_agent=self.crew_manager(),
            verbose=self.VERBOSE,

        )
