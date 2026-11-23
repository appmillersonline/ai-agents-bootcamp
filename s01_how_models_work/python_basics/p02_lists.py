orders = [1040, 1041, 1042]

print(orders[0])        # the first item: counting starts at 0
print(orders[-1])       # the last item

orders.append(1043)     # add one item to the end
print(orders)
print(len(orders), "orders today")
print(1042 in orders)   # is it in the list?
