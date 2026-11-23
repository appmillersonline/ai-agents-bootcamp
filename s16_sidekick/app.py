"""A small web app for Sara's Sidekick: a request, success criteria, the live plan, and approve/reject buttons."""
import gradio as gr

from sidekick import Sidekick

sidekick = None


def plan_markdown():
    if sidekick is None or not sidekick.todos():
        return "*The plan appears here.*"
    marks = {"completed": "✅", "in_progress": "▶️", "pending": "⬜"}
    return "### Plan\n\n" + "\n\n".join(f"{marks.get(t['status'], '⬜')} {t['content']}" for t in sidekick.todos())


def show(outcome, chat):
    if outcome[0] == "approve":
        ask = "**Approval needed:**\n\n" + "\n\n".join(f"`{r['name']}` {r['args']}" for r in outcome[1])
        return chat, plan_markdown(), gr.update(value=ask, visible=True), gr.update(visible=True), gr.update(visible=True)
    _, reply, evaluation = outcome
    verdict = "✅ Success criteria met" if evaluation.success_criteria_met else "⚠️ Not met"
    chat = chat + [{"role": "assistant", "content": f"{reply}\n\n**Evaluator:** {verdict}. {evaluation.feedback}"}]
    return chat, plan_markdown(), gr.update(visible=False), gr.update(visible=False), gr.update(visible=False)


async def go(task, criteria, chat):
    global sidekick
    if sidekick is None:
        sidekick = Sidekick()
        await sidekick.setup()
    chat = (chat or []) + [{"role": "user", "content": f"{task}\n\n*Success criteria:* {criteria}"}]
    return show(await sidekick.start(task, criteria), chat)


async def approve(chat):
    return show(await sidekick.resume(True), chat)


async def reject(chat):
    return show(await sidekick.resume(False, "Sara rejected this. Don't do it."), chat)


with gr.Blocks(title="Sara's Sidekick") as demo:
    gr.Markdown("# Sara's Sidekick")
    with gr.Row():
        with gr.Column(scale=3):
            chat = gr.Chatbot(label="Sidekick", height=420)
            task = gr.Textbox(label="Your request", lines=2)
            criteria = gr.Textbox(label="How will we know it's done?", lines=1)
            go_button = gr.Button("Go", variant="primary")
        with gr.Column(scale=2):
            plan = gr.Markdown("*The plan appears here.*", label="Plan")
            approval = gr.Markdown(visible=False)
            approve_button = gr.Button("Approve", variant="primary", visible=False)
            reject_button = gr.Button("Reject", visible=False)
    outputs = [chat, plan, approval, approve_button, reject_button]
    go_button.click(go, [task, criteria, chat], outputs)
    approve_button.click(approve, [chat], outputs)
    reject_button.click(reject, [chat], outputs)

demo.launch()
