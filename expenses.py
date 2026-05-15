import sqlite3
import matplotlib.pyplot as plt

# --- DATABASE SETUP ---
conn = sqlite3.connect("expenses.db")
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        category TEXT,
        description TEXT,
        amount REAL
    )
''')
conn.commit()

# --- SAMPLE DATA ---
sample_data = [
    ("2024-01-05", "Food", "Lunch", 150),
    ("2024-01-10", "Transport", "Bus pass", 500),
    ("2024-01-15", "Shopping", "Clothes", 1200),
    ("2024-01-20", "Food", "Dinner", 300),
    ("2024-02-02", "Bills", "Electricity", 800),
    ("2024-02-10", "Food", "Groceries", 600),
    ("2024-02-15", "Transport", "Auto", 200),
    ("2024-02-20", "Shopping", "Books", 400),
    ("2024-03-01", "Bills", "Internet", 500),
    ("2024-03-10", "Food", "Lunch", 250),
    ("2024-03-15", "Transport", "Train", 350),
    ("2024-03-20", "Shopping", "Electronics", 2000),
]

cursor.executemany(
    "INSERT INTO expenses (date, category, description, amount) VALUES (?, ?, ?, ?)",
    sample_data
)
conn.commit()

# --- ANALYSIS ---

# 1. Total expenses
cursor.execute("SELECT SUM(amount) FROM expenses")
total = cursor.fetchone()[0]
print(f"Total Expenses: Rs. {total}")

# 2. Category-wise expenses
cursor.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category ORDER BY SUM(amount) DESC")
category_data = cursor.fetchall()
print("\nCategory-wise Expenses:")
for row in category_data:
    print(f"  {row[0]}: Rs. {row[1]}")

# 3. Monthly expenses
cursor.execute("SELECT strftime('%Y-%m', date) as month, SUM(amount) FROM expenses GROUP BY month ORDER BY month")
monthly_data = cursor.fetchall()
print("\nMonthly Expenses:")
for row in monthly_data:
    print(f"  {row[0]}: Rs. {row[1]}")

# 4. Highest single expense
cursor.execute("SELECT description, amount FROM expenses ORDER BY amount DESC LIMIT 1")
highest = cursor.fetchone()
print(f"\nHighest Expense: {highest[0]} - Rs. {highest[1]}")

# --- VISUALIZATION ---

# Pie chart - category wise
categories = [row[0] for row in category_data]
amounts = [row[1] for row in category_data]

plt.figure(figsize=(8, 6))
plt.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=140)
plt.title("Category-wise Expense Distribution")
plt.savefig("category_chart.png")
plt.show()

# Line chart - monthly trend
months = [row[0] for row in monthly_data]
monthly_amounts = [row[1] for row in monthly_data]

plt.figure(figsize=(8, 6))
plt.plot(months, monthly_amounts, marker='o', color='blue', linewidth=2)
plt.title("Monthly Expense Trend")
plt.xlabel("Month")
plt.ylabel("Amount (Rs.)")
plt.grid(True)
plt.savefig("monthly_chart.png")
plt.show()

conn.close()
print("\nDone! Charts saved.")