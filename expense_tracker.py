import sqlite3
import pandas as pd

# Connect to database
conn = sqlite3.connect("expenses.db")
cursor = conn.cursor()

# Create expenses table
cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    category TEXT,
    amount REAL,
    description TEXT
)
""")
conn.commit()

def add_expense():
    date = input("Enter date (YYYY-MM-DD): ")
    category = input("Enter category (Food, Travel, Bills, etc.): ")
    amount = float(input("Enter amount: "))
    description = input("Enter description: ")
    
    cursor.execute("INSERT INTO expenses (date, category, amount, description) VALUES (?, ?, ?, ?)", 
                   (date, category, amount, description))
    conn.commit()
    print("✅ Expense added successfully!")

def view_expenses():
    cursor.execute("SELECT * FROM expenses")
    rows = cursor.fetchall()
    if not rows:
        print("No expenses found.")
    else:
        df = pd.DataFrame(rows, columns=["ID", "Date", "Category", "Amount", "Description"])
        print(df)

def monthly_summary():
    month = input("Enter month (YYYY-MM): ")
    cursor.execute("SELECT category, SUM(amount) FROM expenses WHERE date LIKE ? GROUP BY category", (month + "%",))
    summary = cursor.fetchall()
    
    if not summary:
        print("No expenses found for this month.")
    else:
        df = pd.DataFrame(summary, columns=["Category", "Total Amount"])
        print(df)

def delete_expense():
    expense_id = input("Enter the ID of the expense to delete: ")
    cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    conn.commit()
    print("🗑️ Expense deleted!")

def export_to_csv():
    cursor.execute("SELECT * FROM expenses")
    rows = cursor.fetchall()
    
    if not rows:
        print("No expenses found.")
    else:
        df = pd.DataFrame(rows, columns=["ID", "Date", "Category", "Amount", "Description"])
        df.to_csv("expenses.csv", index=False)
        print("📁 Expenses exported to expenses.csv!")

def main():
    while True:
        print("\n📊 Expense Tracker Menu:")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Monthly Summary")
        print("4. Delete Expense")
        print("5. Export to CSV")
        print("6. Exit")
        
        choice = input("Choose an option: ")
        
        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            monthly_summary()
        elif choice == "4":
            delete_expense()
        elif choice == "5":
            export_to_csv()
        elif choice == "6":
            print("Goodbye! 👋")
            break
        else:
            print("❌ Invalid choice, try again.")

if __name__ == "__main__":
    main()
