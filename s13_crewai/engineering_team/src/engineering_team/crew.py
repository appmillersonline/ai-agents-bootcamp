from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from engineering_team.tools.workspace import workspace_tools


@CrewBase
class EngineeringTeam:
    """A lead who designs, and three engineers who build, the UI and the tests."""

    @agent
    def engineering_lead(self) -> Agent:
        return Agent(config=self.agents_config["engineering_lead"], verbose=True)

    @agent
    def backend_engineer(self) -> Agent:
        return Agent(config=self.agents_config["backend_engineer"], tools=workspace_tools, cache=False, verbose=True)

    @agent
    def frontend_engineer(self) -> Agent:
        return Agent(config=self.agents_config["frontend_engineer"], tools=workspace_tools, cache=False, verbose=True)

    @agent
    def test_engineer(self) -> Agent:
        return Agent(config=self.agents_config["test_engineer"], tools=workspace_tools, cache=False, verbose=True)

    @task
    def design_task(self) -> Task:
        return Task(config=self.tasks_config["design_task"])

    @task
    def backend_task(self) -> Task:
        return Task(config=self.tasks_config["backend_task"])

    @task
    def frontend_task(self) -> Task:
        return Task(config=self.tasks_config["frontend_task"])

    @task
    def test_task(self) -> Task:
        return Task(config=self.tasks_config["test_task"])

    @crew
    def crew(self) -> Crew:
        return Crew(agents=self.agents, tasks=self.tasks, process=Process.sequential, verbose=True)
