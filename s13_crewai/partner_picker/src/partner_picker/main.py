from datetime import date

from partner_picker.crew import PartnerPicker


def run():
    inputs = {"city": "Lisbon", "current_date": date.today().isoformat()}
    PartnerPicker().crew().kickoff(inputs=inputs)
