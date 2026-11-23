"""Step 2: Claude analyses the sales spreadsheet with code execution and makes a real chart."""
from common import DATA, MODEL, client, cost

JOB = ("Using Python on october_sales.csv (revenue = qty × price_eur): give revenue per item and per weekday, "
       "and the October total, as short bullet points. Save a bar chart of revenue per item, best first, "
       "with a title and euro labels, as october_chart.png in $OUTPUT_DIR.")


def analyse_sales():
    uploaded = client.files.upload(file=DATA / "october_sales.csv")
    response = client.messages.create(
        model=MODEL,
        max_tokens=8000,
        tools=[{"type": "code_execution_20260521", "name": "code_execution"}],
        messages=[{"role": "user", "content": [
            {"type": "text", "text": JOB},
            {"type": "container_upload", "file_id": uploaded.id},
        ]}],
    )
    numbers, chart = "", None
    for block in response.content:
        if block.type == "text":
            numbers += block.text
        elif block.type == "bash_code_execution_tool_result":
            for item in getattr(block.content, "content", None) or []:  # files Claude saved
                if item.type == "bash_code_execution_output":
                    chart = DATA / "october_chart.png"
                    client.files.download(item.file_id).write_to_file(chart)
    client.files.delete(uploaded.id)
    return numbers, chart, response.usage


if __name__ == "__main__":
    numbers, chart, usage = analyse_sales()
    print(numbers)
    print(f"\nChart saved: {chart}")
    print(f"Step 2 cost: ${cost(usage):.4f}")
