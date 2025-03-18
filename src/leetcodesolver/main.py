#!/usr/bin/env python
import sys
import warnings
import argparse

from datetime import datetime
from dotenv import load_dotenv
load_dotenv(override=True)

from leetcodesolver.crew import LeetcodeSolver
import leetcodesolver.config as config

# Init tracing to Phoenix
config.init_trace()

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", type=str, required=True, help="Path to the LeetCode problem file")
    args = parser.parse_args()
    
    with open(args.file, "r") as f:
        leetcode_problem = f.read()
    """
    Run the crew.
    """
    inputs = {
        'leetcode_problem': leetcode_problem
    }
    
    try:
        LeetcodeSolver().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        LeetcodeSolver().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        LeetcodeSolver().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "AI LLMs",
        "current_year": str(datetime.now().year)
    }
    try:
        LeetcodeSolver().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")
