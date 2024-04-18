from dotenv import load_dotenv
import streamlit as st
import os
import psycopg2
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Google API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Google gemini model and provide query as response
def get_gemini_response(question, prompt, table_name):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([prompt[0], question])
    # Replace table name placeholder in the response
    response_text = response.text.replace("<TABLE_NAME>", table_name)
    return response_text

# Function to retrieve query from a PostgreSQL database
def read_sql_query(question, prompt, dbname, user, password, host, port):
    # Connect to PostgreSQL
    connection = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )
    cursor = connection.cursor()

    # Perform queries or interact with the existing database
    cursor.execute("SELECT * FROM school")
    
    # Generate SQL query using Gemini
    response = get_gemini_response(question, prompt, "school")
    
    # Check if the response contains a SELECT statement
    if "SELECT" in response.upper():
        # Execute the SQL query
        cursor.execute(response)
        rows = cursor.fetchall()

        # Get column names
        column_names = [desc[0] for desc in cursor.description]
        
        # Print column names
        print("Column Names:", column_names)
        
    else:
        st.error("Gemini did not generate a valid SQL query.")
        rows = None
    
    # Close cursor and connection
    cursor.close()
    connection.close()
    
    # Return the rows
    return rows

## Define Your Prompt
prompt = [
    """
    You are an expert in converting English questions to SQL query!
    The SQL database has the name school and has the following columns - id, gender, 
    ParentMaritalStatus, MathScore, ReadingScore, and WritingScore \n\nFor example,\nExample 1 - How many entries of records are present?, 
    the SQL command will be something like this SELECT COUNT(*) FROM school ;
    \nExample 2 - Tell me all the male students?, 
    the SQL command will be something like this SELECT * FROM school 
    where gender="male";
    \nExample 3 - What is the average MathScore of female students?
    the SQL command will be something like this SELECT AVG(MathScore) FROM school WHERE gender="female"; 
    \nExample 4 - Tell me all the students whose parents are married?, 
    the SQL command will be something like this SELECT * FROM school WHERE ParentMaritalStatus='married';
    also the sql code should not have ``` in beginning or end and sql word in output
    """
]







