from langchain_community.agent_toolkits import create_sql_agent
import getpass
import os
from sqlalchemy import create_engine
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_openai import ChatOpenAI
from langchain.chains import create_sql_query_chain
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate

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

examples = [
    {"input": "List upcoming flu vaccination appointments", "query": "EXEC CalculateVaccinationStats_1;"},
   
]
example_prompt = PromptTemplate.from_template("User input: {input}\nSQL query: {query}")
prompt = FewShotPromptTemplate(
    examples=examples[:5],
    example_prompt=example_prompt,
    prefix="You are a SQLite expert. Given an input question, create a syntactically correct SQLite query to run. Unless otherwise specificed, do not return more than {top_k} rows.\n\nHere is the relevant table info: {table_info}\n\nBelow are a number of examples of questions and their corresponding SQL queries.",
    suffix="User input: {input}\nSQL query: ",
    input_variables=["input", "top_k", "table_info"],
)
response = agent_executor.invoke(
    {
        "input": "Explain why there are two upcoming vaccinations for patients over 65"
    }
)
print(response)
