from operator import itemgetter

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
import getpass
import os
from sqlalchemy import create_engine
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_openai import ChatOpenAI
from langchain.chains import create_sql_query_chain
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool

os.environ["OPENAI_API_KEY"]

connection_uri = r"mssql+pyodbc://ARHAM\SQLEXPRESS/5055_DB?driver=ODBC+Driver+18+for+SQL+Server&Trusted_Connection=yes&TrustServerCertificate=yes"

# Initialize the SQLDatabase instance from LangChain
db = SQLDatabase.from_uri(connection_uri)

# If you're using SQLAlchemy directly for some operations, you can also create an engine with the same URI
engine = create_engine(connection_uri)

print(db.dialect)
print(db.get_usable_table_names())
db.run("SELECT * FROM Orders")
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

answer_prompt = PromptTemplate.from_template(
    """Given the following user question, corresponding SQL query, and SQL result, answer the user question.

Question: {question}
SQL Query: {query}
SQL Result: {result}
Answer: """
)

answer = answer_prompt | llm | StrOutputParser()
write_query = create_sql_query_chain(llm, db)
execute_query = QuerySQLDataBaseTool(db=db)
chain = (
    RunnablePassthrough.assign(query=write_query).assign(
        result=itemgetter("query") | execute_query
    )
    | answer
)

response=chain.invoke({"question": "How many orders are there"})
print(response)