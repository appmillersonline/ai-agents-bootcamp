from debate.crew import Debate


def run():
    motion = input("Motion: ")
    Debate().crew().kickoff(inputs={"motion": motion})
