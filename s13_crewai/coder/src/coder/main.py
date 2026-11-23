from coder.crew import Coder

ASSIGNMENT = (
    "sales.csv in the sandbox has every candle order Sara sold in October "
    "(columns: date, size, scent, quantity, price). Revenue is quantity times price. "
    "Print the total revenue, the revenue for each size, the best day of the week by revenue, "
    "and the top 3 scents by quantity sold."
)


def run():
    Coder().crew().kickoff(inputs={"assignment": ASSIGNMENT})
