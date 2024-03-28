from langchain_community.agent_toolkits import create_sql_agent
import getpass
import os
from sqlalchemy import create_engine
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_openai import ChatOpenAI
from langchain.chains import create_sql_query_chain
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool

os.environ["OPENAI_API_KEY"]

connection_uri = r"mssql+pyodbc://ARHAM\SQLEXPRESS/AI_Test?driver=ODBC+Driver+18+for+SQL+Server&Trusted_Connection=yes&TrustServerCertificate=yes"

# Initialize the SQLDatabase instance from LangChain
db = SQLDatabase.from_uri(connection_uri)

# If you're using SQLAlchemy directly for some operations, you can also create an engine with the same URI
engine = create_engine(connection_uri)

print(db.dialect)
print(db.get_usable_table_names())
#db.run("SELECT * FROM Orders")
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
#chain = create_sql_query_chain(llm, db)
agent_executor = create_sql_agent(llm, db=db, agent_type="openai-tools", verbose=True)

response = agent_executor.invoke(
    {
        "input": "Debug why there are two patients in the CalculateVaccinationStats stored procedure for patients over 65?Note that there might be discrepany in the data. The patients table is the most accurate one"
    }
)
print(response)
