from datetime import date

from content_crew.crew import ContentCrew


def run():
    today = date.today()
    ContentCrew().crew().kickoff(inputs={
        "month": today.strftime("%B"),
        "current_date": today.isoformat(),
    })
