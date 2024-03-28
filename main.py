import getpass
import os
from sqlalchemy import create_engine
from langchain_community.utilities.sql_database import SQLDatabase

# Securely set the OPENAI_API_KEY environment variable
os.environ["OPENAI_API_KEY"]
# Define the connection URI for SQL Server using Windows Authentication
# Use a raw string to prevent issues with backslashes
connection_uri = r"mssql+pyodbc://ARHAM\SQLEXPRESS/5055_DB?driver=ODBC+Driver+18+for+SQL+Server&Trusted_Connection=yes&TrustServerCertificate=yes"

# Initialize the SQLDatabase instance from LangChain
db = SQLDatabase.from_uri(connection_uri)

# If you're using SQLAlchemy directly for some operations, you can also create an engine with the same URI
engine = create_engine(connection_uri)
#print(db.Orders)
print(db.dialect)
print(db.get_usable_table_names())
db.run("SELECT * FROM Orders")
