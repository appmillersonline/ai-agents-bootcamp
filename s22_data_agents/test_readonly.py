"""B10: prove the database can't be changed through the server, even by a sneaky query. No model involved."""
from sales_server import run_sql

print("1.", run_sql("DELETE FROM orders WHERE channel = 'wholesale'"))
print("2.", run_sql("WITH x AS (SELECT 1) DELETE FROM orders WHERE channel = 'wholesale'"))
print("3.", run_sql("SELECT COUNT(*) AS orders FROM orders"))
