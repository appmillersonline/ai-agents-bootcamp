from shop import check_stock

print("name:       ", check_stock.name)
print("description:", check_stock.description)
print("args:       ", check_stock.args)
print("invoke:     ", check_stock.invoke({"item": "Candle trio"}))
