import sqlite3

def create_database():
    conn = sqlite3.connect("transactions.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL,
            hour INTEGER,
            new_device INTEGER,
            international INTEGER,
            location_changed INTEGER,
            prediction TEXT
        )
    """)

    conn.commit()
    conn.close()


def save_transaction(amount, hour, new_device, international, location_changed, prediction):
    conn = sqlite3.connect("transactions.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO transactions
        (amount, hour, new_device, international, location_changed, prediction)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (amount, hour, new_device, international, location_changed, prediction))

    conn.commit()
    conn.close()


def get_transactions():
    conn = sqlite3.connect("transactions.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM transactions")
    data = cursor.fetchall()

    conn.close()
    return data


create_database()