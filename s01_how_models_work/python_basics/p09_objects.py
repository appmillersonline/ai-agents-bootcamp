class Order:
    """A small blueprint for making orders."""

    def __init__(self, order_id, status):
        self.order_id = order_id
        self.status = status

    def is_late(self):
        return self.status == "delayed"


order = Order(1044, "delayed")
print(order.order_id, order.status)   # read an attribute with a dot
print(order.is_late())                # call a method with a dot
