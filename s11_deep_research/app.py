"""A small web app for the research team. Run it, then open the link it prints."""
import gradio as gr

from research_manager import run


async def research(question):
    status = ""
    async for update in run(question):
        if isinstance(update, str):
            status += f"- {update}\n"
            yield status
        else:
            yield status + f"\n## Summary\n{update.summary}\n\n{update.report}"


with gr.Blocks(title="Sara's Research Desk") as app:
    gr.Markdown("# Sara's Research Desk\n"
                "Ask a business question. Four agents plan, search, write and email the answer.")
    question = gr.Textbox(label="Your question", placeholder="What do boutique hotels pay for candles?")
    button = gr.Button("Research it", variant="primary")
    answer = gr.Markdown()
    button.click(research, inputs=question, outputs=answer)
    question.submit(research, inputs=question, outputs=answer)

app.launch()
