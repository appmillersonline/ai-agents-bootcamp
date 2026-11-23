import json

for line in open("audit_log.jsonl"):
    e = json.loads(line)
    print(f"{e['time'][11:16]}  {e['who']:9} {e['kind']:8} {e['amount_eur']:6.2f}  {e['decision']:9} by {e['decided_by']:8}  {e['rule']}")
