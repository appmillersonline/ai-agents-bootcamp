from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from pydantic import BaseModel, Field

from partner_picker.tools.push import send_push
from partner_picker.tools.web_search import web_search


class Partner(BaseModel):
    name: str = Field(description="The business name")
    city: str = Field(description="Where it operates")
    why_now: str = Field(description="Why it is interesting right now")


class PartnerList(BaseModel):
    partners: list[Partner] = Field(description="The businesses found")


class PartnerResearch(BaseModel):
    name: str = Field(description="The business name")
    size: str = Field(description="Number of locations, rooms or seats")
    recent_news: str = Field(description="What happened in the last 12 months")
    supplier_signals: str = Field(description="Signs it likes local or sustainable suppliers")


class ResearchList(BaseModel):
    research: list[PartnerResearch] = Field(description="One entry per business")


@CrewBase
class PartnerPicker:
    """Find growing hospitality businesses, research them, and pick Sara's best first pitch."""

    @agent
    def partner_finder(self) -> Agent:
        return Agent(config=self.agents_config["partner_finder"], tools=[web_search], verbose=True)

    @agent
    def partner_researcher(self) -> Agent:
        return Agent(config=self.agents_config["partner_researcher"], tools=[web_search], verbose=True)

    @agent
    def partner_picker(self) -> Agent:
        return Agent(config=self.agents_config["partner_picker"], tools=[send_push], verbose=True)

    @task
    def find_partners(self) -> Task:
        return Task(config=self.tasks_config["find_partners"], output_pydantic=PartnerList)

    @task
    def research_partners(self) -> Task:
        return Task(config=self.tasks_config["research_partners"], output_pydantic=ResearchList)

    @task
    def pick_partner(self) -> Task:
        return Task(config=self.tasks_config["pick_partner"])

    @crew
    def crew(self) -> Crew:
        manager = Agent(config=self.agents_config["manager"], allow_delegation=True)
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.hierarchical,
            manager_agent=manager,
            memory=True,
            verbose=True,
        )
