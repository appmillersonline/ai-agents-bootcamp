from crewai import Agent, Crew, Process, Task
from crewai.knowledge.source.text_file_knowledge_source import TextFileKnowledgeSource
from crewai.project import CrewBase, agent, crew, task

from content_crew.tools.web_search import web_search

handbook = TextFileKnowledgeSource(file_paths=["shop_handbook.md"])


@CrewBase
class ContentCrew:
    """A small marketing team for Sara's Shop: research, write, edit."""

    @agent
    def trend_researcher(self) -> Agent:
        return Agent(config=self.agents_config["trend_researcher"], tools=[web_search], verbose=True)

    @agent
    def content_writer(self) -> Agent:
        return Agent(config=self.agents_config["content_writer"], verbose=True)

    @agent
    def editor(self) -> Agent:
        return Agent(config=self.agents_config["editor"], verbose=True)

    @task
    def research_task(self) -> Task:
        return Task(config=self.tasks_config["research_task"])

    @task
    def writing_task(self) -> Task:
        return Task(config=self.tasks_config["writing_task"])

    @task
    def editing_task(self) -> Task:
        return Task(config=self.tasks_config["editing_task"])

    @crew
    def crew(self) -> Crew:
        return Crew(agents=self.agents, tasks=self.tasks, process=Process.sequential,
                    knowledge_sources=[handbook], verbose=True)
