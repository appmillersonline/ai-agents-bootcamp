import json

from approvals import reader

requests = json.load(open("requests.json"))
for name in ["vase", "tape"]:
    form = reader.invoke(f"Fill in the form for this refund or expense request. Do not decide anything.\n\n{requests[name]}")
    print(f"--- {name} ---")
    print(form.model_dump_json(indent=2))
