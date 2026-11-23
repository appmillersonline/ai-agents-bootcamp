"""Run Claude Code headless and print each step it takes: tools, results, final answer."""
import json
import subprocess
import sys
import time

prompt, *flags = [a for a in sys.argv[1:] if a != "--show-answer"]
cmd = ["claude", "-p", prompt, "--output-format", "stream-json", "--verbose", *flags]
agents = {}  # tool_use id -> subagent name
last = {"total_cost_usd": 0}
start = time.monotonic()
proc = subprocess.Popen(cmd, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, text=True)
for line in proc.stdout:
    event = json.loads(line)
    pad = "      " if event.get("parent_tool_use_id") else "  "  # steps inside a subagent are indented
    if event["type"] == "assistant":
        for block in event["message"]["content"]:
            if block["type"] == "tool_use" and block["name"] in ("Agent", "Task"):
                agents[block["id"]] = block["input"].get("subagent_type", "agent")
                print(f"{pad}[{block['name']}] -> {agents[block['id']]}: {block['input'].get('description', '')}")
            elif block["type"] == "tool_use":
                args = block["input"]
                shown = args.get("command") or args.get("file_path") or args.get("pattern") or json.dumps(args)
                shown = shown.split("/")[-1] if "file_path" in args else shown.splitlines()[0][:70]
                print(f"{pad}[{block['name']}] {shown}")
            elif block["type"] == "text" and block["text"].strip():
                print(f"{pad}claude: {block['text'].strip().splitlines()[0][:220]}")
    elif event["type"] == "user":
        for block in event["message"]["content"]:
            if isinstance(block, dict) and block.get("tool_use_id") in agents:
                report = block["content"][0]["text"] if isinstance(block["content"], list) else str(block["content"])
                if report.startswith("Async agent launched"):
                    print(f"  <- {agents[block['tool_use_id']]} started, working in parallel")
                else:
                    print(f"  <- {agents[block['tool_use_id']]} reports: {report.strip().splitlines()[0][:150]}")
            elif isinstance(block, dict) and block.get("is_error"):
                text = str(block["content"]).replace("<tool_use_error>", "").replace("</tool_use_error>", "")
                text = text.split("]: ")[-1]  # a hook's own message comes after the command
                print(f"{pad}   {'blocked: needs approval' if 'approval' in text else 'failed: ' + text.strip().splitlines()[0][:90]}")
    elif event["type"] == "result":
        last = event  # with parallel subagents there can be several; the last one has the full cost
if "--show-answer" in sys.argv:  # print the whole final answer, not just its first line
    print("\n".join("  | " + l for l in last.get("result", "").strip().splitlines()[:8]))
print(f"== done: {time.monotonic() - start:.0f} s, ${last['total_cost_usd']:.3f}")
