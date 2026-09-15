import sqlite3

# Connect to SQLite database
conn = sqlite3.connect("fraud_detection.db")
cursor = conn.cursor()

# Get all transactions
cursor.execute("SELECT * FROM transactions")

rows = cursor.fetchall()

print("===================================")
print("       TRANSACTION HISTORY")
print("===================================")

if len(rows) == 0:
    print("No transactions found.")
else:
    for row in rows:
        print(row)

print("===================================")

# Close database
conn.close()