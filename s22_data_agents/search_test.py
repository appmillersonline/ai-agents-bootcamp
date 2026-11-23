"""B11: test the search on its own, no agent: which sections come back, and how strong is the match?"""
from kb_server import search_docs

for query in ["mug arrived broken", "how long does Clayworks take", "office wifi password"]:
    print(f"== {query}")
    for block in search_docs(query, k=2).split("\n\n"):
        print("  " + block.splitlines()[0])
