from datetime import date

from company_researcher.crew import CompanyResearcher


def run():
    company = input("Company: ")
    inputs = {"company": company, "current_date": date.today().isoformat()}
    CompanyResearcher().crew().kickoff(inputs=inputs)
