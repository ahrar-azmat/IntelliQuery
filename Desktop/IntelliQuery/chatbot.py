from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import get_db
from openai_client import ask_openai, get_embeddings, find_best_match
import logging
import re

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("chatbot")

# Define the correct table and column names
correct_table = "Property_Tax_Summary_View"
correct_columns = {
    "owner_name": "owner_name",
    "city": "city",
    "property_type": "property_type",
    "zip_code":"zip_code"
    # Add any other mappings if necessary
}

def correct_sql_query(sql_query: str) -> str:
    """
    Correct the SQL query by replacing incorrect table and column names with the correct ones.
    """
    logger.info(f"Original SQL query before correction: {sql_query}")

    # Correct the table name
    if "property_table" in sql_query or "properties" in sql_query:
        logger.info(f"Replacing table name in query: {sql_query}")
        sql_query = sql_query.replace("property_table", correct_table)
        sql_query = sql_query.replace("properties", correct_table)

    # Correct any incorrect column names
    for incorrect, correct in correct_columns.items():
        if incorrect in sql_query:
            logger.info(f"Replacing column name '{incorrect}' with '{correct}' in query.")
            sql_query = sql_query.replace(incorrect, correct)

    logger.info(f"Corrected SQL query: {sql_query}")
    return sql_query

def extract_contextual_information(query: str, column_names: list, sample_data: dict) -> str:
    """
    Use embeddings to extract contextual information from the query.
    """
    logger.info(f"Extracting contextual information for query: {query}")

    # Generate embeddings for column names
    column_embeddings = get_embeddings(column_names)
    query_embedding = get_embeddings([query])

    # Find the best matching column for the query
    best_match_index, best_match_score = find_best_match(query_embedding, column_embeddings)
    best_matching_column = column_names[best_match_index]

    logger.info(f"Best matching column for query '{query}': {best_matching_column} with score {best_match_score}")

    # Prepare the context based on the best matching column
    context = (
        f"The user is asking about '{best_matching_column}'. "
        f"Here is a sample data row from this column: {sample_data[best_matching_column]}. "
        f"Please generate an SQL query to fetch relevant data for the user's query: '{query}'."
    )
    return context

async def handle_chat(query: str):
    try:
        logger.info(f"Received query: {query}")
        
        with next(get_db()) as db:
            query = query.lower()

            # Fetch column names
            logger.info("Fetching column names from Property_Tax_Summary_View")
            column_names = []
            try:
                result = db.execute(text("SELECT TOP 1 * FROM Property_Tax_Summary_View"))
                column_names = list(result.keys())
                logger.info(f"Available columns in the view: {column_names}")
            except Exception as e:
                logger.error(f"Error fetching column names: {str(e)}")
                raise HTTPException(status_code=500, detail=f"Error fetching column names: {str(e)}")

        with next(get_db()) as db:
            logger.info("Fetching sample data for each column")
            sample_data_dict = {}
            try:
                sample_data_query = f"SELECT TOP 1 {', '.join(column_names)} FROM Property_Tax_Summary_View"
                sample_data_result = db.execute(text(sample_data_query))
                sample_data = sample_data_result.fetchone()
                if sample_data:
                    sample_data_dict = dict(zip(column_names, sample_data))
                    logger.info(f"Sample data fetched: {sample_data_dict}")
                else:
                    logger.warning("No sample data fetched; the result is empty.")
                sample_data_result.close()
            except Exception as e:
                logger.error(f"Error fetching sample data: {str(e)}")
                raise HTTPException(status_code=500, detail=f"Error fetching sample data: {str(e)}")

        # Extract context using embeddings
        logger.info("Preparing context for GPT-4")
        context = extract_contextual_information(query, column_names, sample_data_dict)

        logger.info("Sending context to GPT-4")
        raw_response = ask_openai(context)
        logger.info(f"GPT-4 raw response: {raw_response}")

        # Use regex to extract the SQL query from the raw response
        sql_query_match = re.search(r"(SELECT\s.+\sFROM\s.+;)", raw_response, re.IGNORECASE | re.DOTALL)
        if sql_query_match:
            sql_query = sql_query_match.group(1).strip()
            logger.info(f"Extracted SQL query: {sql_query}")
        else:
            logger.error("Failed to extract SQL query from GPT-4 response.")
            return {"response": "Failed to extract SQL query from the response."}

        # Correct the SQL query
        corrected_sql_query = correct_sql_query(sql_query)
        logger.info(f"Corrected SQL query: {corrected_sql_query}")

        with next(get_db()) as db:
            logger.info("Executing the corrected SQL query")
            try:
                result = db.execute(text(corrected_sql_query)).scalar()
                if result is None:
                    logger.info("No data found for the given query.")
                    return {"response": "No data found for the given query."}

                # Dynamically generate a response based on the query context and result
                response = f"The result for your query '{query}' is: {result}."
                logger.info(f"Query executed successfully, returning result: {response}")
                return {"response": response}
            except Exception as sql_error:
                logger.error(f"SQL Execution Error: {str(sql_error)}")
                return {"response": f"Error executing the SQL query: {str(sql_error)}"}

    except Exception as e:
        logger.error(f"Error handling query: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
