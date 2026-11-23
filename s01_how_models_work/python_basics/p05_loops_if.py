orders = [
    {"id": 1042, "status": "shipped"},
    {"id": 1043, "status": "processing"},
    {"id": 1044, "status": "delayed"},
]

for order in orders:
    if order["status"] == "shipped":
        print(order["id"], "is on its way")
    elif order["status"] == "delayed":
        print(order["id"], "needs a check")
    else:
        print(order["id"], "is being packed")
