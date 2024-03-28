import getpass
import os
from sqlalchemy import create_engine, text
from langchain_community.utilities.sql_database import SQLDatabase

# Securely set the OPENAI_API_KEY environment variable
os.environ["OPENAI_API_KEY"] = "your_openai_api_key_here"  # Ensure to set this appropriately

# Define the connection URI for SQL Server using Windows Authentication
# Use a raw string to prevent issues with backslashes
connection_uri = r"mssql+pyodbc://ARHAM\SQLEXPRESS/5055_DB?driver=ODBC+Driver+18+for+SQL+Server&Trusted_Connection=yes&TrustServerCertificate=yes"

# Initialize the SQLDatabase instance from LangChain
db = SQLDatabase.from_uri(connection_uri)

# If you're using SQLAlchemy directly for some operations, you can also create an engine with the same URI
engine = create_engine(connection_uri)

# Execute a query to select all rows from the 'Orders' table
with engine.connect() as connection:
    result = connection.execute(text("SELECT * FROM Orders"))

    # Get the column headers
    column_headers = result.keys()

    # Fetch all rows
    rows = result.fetchall()

# Print column headers
print("Column headers for 'Orders' table:", column_headers)

# Print row data
for row in rows:
    print("Row data:", row)
