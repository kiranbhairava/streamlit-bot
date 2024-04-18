import streamlit as st
from app import read_sql_query, prompt
from dotenv import load_dotenv
import os

load_dotenv()

# Define CSS classes for styling
st.markdown("""
    <style>
        .chat-container {
            display: flex;
            flex-direction: column;
            align-items: flex-start;
            padding: 10px;
            width: 100%;
            max-width: 1000px;
            margin-bottom: 20px;
        }
        .user-message {
            background-color: #808080;
            color: #000000;
            border-radius: 10px;
            padding: 10px 15px;
            margin-bottom: 10px;
            max-width: 100%;
            align-self: flex-end;
            text-align: right;
        }
        .bot-message {
            background-color: #2E2E2E;
            color: #FFFFFF;
            border-radius: 10px;
            padding: 10px 15px;
            margin-bottom: 10px;
            max-width: 100%;
            align-self: flex-start;
            text-align: left;
        }
    </style>
""", unsafe_allow_html=True)

st.title("database bot: ")

# Define function to clear form fields
def clear_form():
    st.session_state.user_input = ""

# Initialize chat history if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = []


with st.form("myform"):
    # Text input for user
    user_input = st.text_input("YOU:", key="user_input")
    
    # Submit button
    submit_button = st.form_submit_button(label="Submit")
    
    # Clear button to clear text input
    clear_button = st.form_submit_button(label="Clear", on_click=clear_form)


if submit_button and user_input.strip():
    # Add user message to chat history
    st.session_state.messages.append({"role": "User", "content": user_input})

    try:
        # Execute SQL query
        db_config = {
            "dbname": os.getenv("DB_NAME"),
            "user": os.getenv("DB_USER"),
            "password": os.getenv("DB_PASSWORD"),
            "host": os.getenv("DB_HOST"),
            "port": os.getenv("DB_PORT")
        }
        query_result = read_sql_query(user_input, prompt, **db_config)

        # Display query result or apology if no result found
        if query_result:
            if len(query_result) == 1:
                # If only one value is returned, directly extract it
                response = str(query_result[0][0])
            else:
                # If multiple values are returned, format them
                response = "\n".join(str(row) for row in query_result)
        else:
            response = "I'm sorry, I couldn't find any information related to your query."

    except Exception as e:
        # Handle any exceptions that occur during execution
        response = f"I am sorry, I couldn't find any information related to your query: {str()}"

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "bot", "content": response})



# Display chat message history
for message in st.session_state.messages:
    if message["role"] == "User":
        st.markdown(f'<div class="user-message"> 🙋 {message["content"]}</div>', unsafe_allow_html=True) 
    else:
        st.markdown(f'<div class="bot-message">🤖 {message["content"]}</div>', unsafe_allow_html=True)







