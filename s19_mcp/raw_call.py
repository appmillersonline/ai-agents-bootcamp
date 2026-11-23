"""Talk MCP by hand: start the server, write JSON lines to its input, read JSON lines from its output."""
import json
import subprocess
from pathlib import Path

DATA = str(Path(__file__).parents[1] / "data")
server = subprocess.Popen(["npx", "-y", "@modelcontextprotocol/server-filesystem", DATA],
                          stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)


def send(message: dict) -> None:
    print("client ->", json.dumps(message)[:110])
    server.stdin.write(json.dumps(message) + "\n")
    server.stdin.flush()


def receive() -> dict:
    reply = json.loads(server.stdout.readline())
    print("server <-", json.dumps(reply)[:110], "\n")
    return reply


send({"jsonrpc": "2.0", "id": 1, "method": "initialize",
      "params": {"protocolVersion": "2025-06-18", "capabilities": {}, "clientInfo": {"name": "by-hand", "version": "1"}}})
receive()
send({"jsonrpc": "2.0", "method": "notifications/initialized"})

send({"jsonrpc": "2.0", "id": 2, "method": "tools/list"})
tools = receive()["result"]["tools"]
print(f"   ({len(tools)} tools; first one: {tools[0]['name']})\n")

send({"jsonrpc": "2.0", "id": 3, "method": "tools/call",
      "params": {"name": "read_text_file", "arguments": {"path": f"{DATA}/inventory.csv"}}})
print(receive()["result"]["content"][0]["text"])
server.terminate()
