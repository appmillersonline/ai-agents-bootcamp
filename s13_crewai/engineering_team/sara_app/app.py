import gradio as gr

from giftcards import GiftCards

cards = GiftCards()


def issue_card(amount):
    try:
        code = cards.issue_card(amount)
        balance = cards.get_balance(code)
        return f"Issued card: {code}", code, str(balance), f"Created {code} with balance {balance}."
    except Exception as exc:
        return f"Error: {exc}", "", "", str(exc)


def spend_card(card_code, amount):
    try:
        success = cards.spend(card_code, amount)
        balance = cards.get_balance(card_code)
        message = "Spend approved." if success else "Spend refused: not enough balance."
        return message, str(balance), str(cards.get_history(card_code))
    except Exception as exc:
        return f"Error: {exc}", "", ""


def get_balance(card_code):
    try:
        balance = cards.get_balance(card_code)
        return f"Balance: {balance}"
    except Exception as exc:
        return f"Error: {exc}"


def get_history(card_code):
    try:
        history = cards.get_history(card_code)
        return str(history)
    except Exception as exc:
        return f"Error: {exc}"


def cancel_card(card_code):
    try:
        cards.cancel_card(card_code)
        return "Card cancelled."
    except Exception as exc:
        return f"Error: {exc}"


with gr.Blocks(title="Sara's Gift Cards") as demo:
    gr.Markdown("# Sara's Gift Cards\nUse one shared gift card manager for the whole session.")

    with gr.Tab("Issue card"):
        amount_issue = gr.Textbox(label="Initial amount", placeholder="25.00")
        btn_issue = gr.Button("Issue card")
        issue_status = gr.Textbox(label="Status")
        issued_code = gr.Textbox(label="Card code")
        issued_balance = gr.Textbox(label="Balance")
        issued_note = gr.Textbox(label="Details")
        btn_issue.click(issue_card, inputs=amount_issue, outputs=[issue_status, issued_code, issued_balance, issued_note])

    with gr.Tab("Spend on card"):
        spend_code = gr.Textbox(label="Card code", placeholder="SARA-1234")
        spend_amount = gr.Textbox(label="Amount", placeholder="5.00")
        btn_spend = gr.Button("Spend")
        spend_status = gr.Textbox(label="Status")
        spend_balance = gr.Textbox(label="New balance")
        spend_history = gr.Textbox(label="History")
        btn_spend.click(spend_card, inputs=[spend_code, spend_amount], outputs=[spend_status, spend_balance, spend_history])

    with gr.Tab("Check balance"):
        balance_code = gr.Textbox(label="Card code", placeholder="SARA-1234")
        btn_balance = gr.Button("Get balance")
        balance_result = gr.Textbox(label="Result")
        btn_balance.click(get_balance, inputs=balance_code, outputs=balance_result)

    with gr.Tab("View history"):
        history_code = gr.Textbox(label="Card code", placeholder="SARA-1234")
        btn_history = gr.Button("Get history")
        history_result = gr.Textbox(label="Result")
        btn_history.click(get_history, inputs=history_code, outputs=history_result)

    with gr.Tab("Cancel card"):
        cancel_code = gr.Textbox(label="Card code", placeholder="SARA-1234")
        btn_cancel = gr.Button("Cancel card")
        cancel_result = gr.Textbox(label="Status")
        btn_cancel.click(cancel_card, inputs=cancel_code, outputs=cancel_result)


demo.launch()
