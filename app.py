import tkinter as tk
from tkinter import messagebox
import joblib
import sqlite3
from database import save_transaction, get_transactions

# Load trained model
model = joblib.load("model/fraud_model.pkl")


def check_transaction():
    try:
        amount = float(amount_entry.get())
        hour = int(hour_entry.get())
        new_device = int(new_device_entry.get())
        international = int(international_entry.get())
        location_changed = int(location_entry.get())

        # Validation
        if amount < 0:
            messagebox.showerror("Error", "Amount cannot be negative.")
            return

        if hour < 0 or hour > 23:
            messagebox.showerror("Error", "Hour must be between 0 and 23.")
            return

        if new_device not in [0, 1]:
            messagebox.showerror("Error", "New Device must be 0 or 1.")
            return

        if international not in [0, 1]:
            messagebox.showerror("Error", "International must be 0 or 1.")
            return

        if location_changed not in [0, 1]:
            messagebox.showerror("Error", "Location Changed must be 0 or 1.")
            return

        # Prediction
        prediction = model.predict([[
            amount,
            hour,
            new_device,
            international,
            location_changed
        ]])[0]

        if prediction == 1:
            result = "Fraudulent Transaction"
        else:
            result = "Legitimate Transaction"

        # Save transaction in SQLite
        save_transaction(
            amount,
            hour,
            new_device,
            international,
            location_changed,
            result
        )

        result_label.config(text=result)

    except ValueError:
        messagebox.showerror(
            "Error",
            "Please enter valid numbers in all fields."
        )


def view_transactions():
    transactions = get_transactions()

    window = tk.Toplevel(root)
    window.title("Transaction History")
    window.geometry("800x400")

    if not transactions:
        tk.Label(
            window,
            text="No transactions found."
        ).pack(pady=20)
        return

    headers = [
        "ID",
        "Amount",
        "Hour",
        "New Device",
        "International",
        "Location Changed",
        "Prediction"
    ]

    for col, header in enumerate(headers):
        tk.Label(
            window,
            text=header,
            font=("Arial", 10, "bold")
        ).grid(row=0, column=col, padx=5, pady=5)

    for row_index, transaction in enumerate(transactions, start=1):
        for col_index, value in enumerate(transaction):
            tk.Label(
                window,
                text=str(value)
            ).grid(
                row=row_index,
                column=col_index,
                padx=5,
                pady=5
            )


# Main window
root = tk.Tk()
root.title("AI Digital Fraud Detection")
root.geometry("500x550")


title_label = tk.Label(
    root,
    text="AI Digital Fraud Detection",
    font=("Arial", 20, "bold")
)
title_label.pack(pady=20)


# Amount
tk.Label(root, text="Transaction Amount").pack()
amount_entry = tk.Entry(root)
amount_entry.pack(pady=5)


# Hour
tk.Label(root, text="Transaction Hour (0-23)").pack()
hour_entry = tk.Entry(root)
hour_entry.pack(pady=5)


# New Device
tk.Label(root, text="New Device (0 = No, 1 = Yes)").pack()
new_device_entry = tk.Entry(root)
new_device_entry.pack(pady=5)


# International
tk.Label(root, text="International (0 = No, 1 = Yes)").pack()
international_entry = tk.Entry(root)
international_entry.pack(pady=5)


# Location Changed
tk.Label(root, text="Location Changed (0 = No, 1 = Yes)").pack()
location_entry = tk.Entry(root)
location_entry.pack(pady=5)


# Check button
check_button = tk.Button(
    root,
    text="Check Transaction",
    command=check_transaction
)
check_button.pack(pady=20)


# Result
result_label = tk.Label(
    root,
    text="",
    font=("Arial", 14, "bold")
)
result_label.pack(pady=10)


# View transactions button
view_button = tk.Button(
    root,
    text="View Transactions",
    command=view_transactions
)
view_button.pack(pady=10)


root.mainloop()