# Database
from PyQt6.QtSql import QSqlDatabase, QSqlQuery

def init_db(db_name):
    """
    Initializes the SQLite database connection and creates the expenses table if it doesn't exist.
    """
    # Initialize SQLite database connection
    database = QSqlDatabase.addDatabase("QSQLITE")
    database.setDatabaseName(db_name)

    # Open the database connection
    if not database.open():
        return False
    
    # Create a table if it doesn't exist
    query = QSqlQuery()
    query.exec("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            category TEXT,
            amount REAL,
            description TEXT
        )
    """)
    
    return True

def fetch_expenses():
    """
    Fetches all expenses from the database, ordered by date in descending order.
    Returns a list of expenses.
    """
    query = QSqlQuery("SELECT * FROM expenses ORDER BY date DESC")
    expenses = []

    # Iterate through the results and add them to the list
    while query.next():
        expenses.append([query.value(i) for i in range(5)])  # Fetches all columns for each row
    
    return expenses

def add_expenses(date, category, amount, description):
    """
    Adds a new expense record to the database.
    """
    query = QSqlQuery()
    query.prepare("""
        INSERT INTO expenses (date, category, amount, description)
        VALUES (?, ?, ?, ?)
    """)
    
    # Bind the values to the query
    query.addBindValue(date)
    query.addBindValue(category)
    query.addBindValue(amount)
    query.addBindValue(description)

    # Execute the query
    return query.exec()

def delete_expenses(expense_id):
    """
    Deletes an expense record from the database based on the given expense ID.
    """
    query = QSqlQuery()
    query.prepare("DELETE FROM expenses WHERE id = ?")
    query.addBindValue(expense_id)

    # Execute the query
    return query.exec()
