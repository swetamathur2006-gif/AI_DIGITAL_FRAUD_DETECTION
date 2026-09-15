import joblib
import sqlite3

print("===================================")
print("     AI DIGITAL FRAUD DETECTION")
print("===================================")

# Load trained AI model
model = joblib.load("model/fraud_model.pkl")

print("AI Model loaded successfully!")
print()

# Connect to SQLite database
conn = sqlite3.connect("fraud_detection.db")
cursor = conn.cursor()

# Create transactions table
cursor.execute("""
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    amount REAL,
    hour INTEGER,
    new_device INTEGER,
    international INTEGER,
    location_changed INTEGER,
    prediction INTEGER
)
""")

conn.commit()

# User Input
amount = float(input("Enter transaction amount: "))
hour = int(input("Enter transaction hour (0-23): "))
new_device = int(input("New device? (1 = Yes, 0 = No): "))
international = int(input("International transaction? (1 = Yes, 0 = No): "))
location_changed = int(input("Location changed? (1 = Yes, 0 = No): "))

# Prepare input for AI model
user_input = [[
    amount,
    hour,
    new_device,
    international,
    location_changed
]]

# AI Prediction
prediction = model.predict(user_input)

# Save transaction in SQLite database
cursor.execute("""
INSERT INTO transactions
(amount, hour, new_device, international, location_changed, prediction)
VALUES (?, ?, ?, ?, ?, ?)
""", (
    amount,
    hour,
    new_device,
    international,
    location_changed,
    int(prediction[0])
))

conn.commit()

# Display result
print()
print("===================================")
print("             AI RESULT")
print("===================================")

if prediction[0] == 1:
    print("FRAUDULENT TRANSACTION DETECTED!")
else:
    print("TRANSACTION IS LEGITIMATE")

print("Transaction saved to SQLite database.")
print("===================================")

# Close database connection
conn.close()