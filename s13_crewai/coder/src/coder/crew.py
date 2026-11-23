from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from coder.tools.sandbox import sandbox_tools


@CrewBase
class Coder:
    """One agent that writes Python in a sandbox folder and runs it inside Docker."""

    @agent
    def coder(self) -> Agent:
        return Agent(config=self.agents_config["coder"], tools=sandbox_tools, verbose=True)

    @task
    def coding_task(self) -> Task:
        return Task(config=self.tasks_config["coding_task"])

    @crew
    def crew(self) -> Crew:
        return Crew(agents=self.agents, tasks=self.tasks, process=Process.sequential, verbose=True)
