# IntelliQuery
# IntelliQuery: AI-Powered Chatbot for Real-Time Database Insights

## Overview
IntelliQuery is an AI-powered chatbot designed to provide real-time insights into databases using natural language queries. Built on top of OpenAI's GPT-4 and leveraging a Microsoft SQL Server database, IntelliQuery allows users to interact with their data using simple, conversational language. The system translates user queries into SQL, executes them against the database, and returns the results in a user-friendly format.

## Features
- **Natural Language Querying**: Users can ask questions in plain English, and IntelliQuery will interpret the query, generate the appropriate SQL, and return the results.
- **Real-Time Database Access**: Execute SQL queries in real-time against a Microsoft SQL Server database.
- **Embeddings for Accurate Mapping**: Uses embeddings to accurately map natural language queries to the appropriate database columns.
- **Error Handling**: Includes mechanisms for correcting common SQL errors, such as incorrect table or column names.
- **Continuous Learning**: A planned feature that will allow the chatbot to learn from user feedback and improve over time.

## Getting Started

### Prerequisites
- Python 3.7+
- Microsoft SQL Server
- Git
- An OpenAI API key
- A GitHub account

### Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/your-username/IntelliQuery.git
    cd IntelliQuery
    ```

2. **Create and activate a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install the dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up environment variables**:
    - Create a `.env` file in the project root and add your OpenAI API key:
    ```
    OPENAI_API_KEY=your_openai_api_key
    ```

5. **Set up the SQL Server database**:
    - Execute the provided SQL script to create the necessary tables and views.
    - Update your database connection settings in the project’s configuration.

### Usage

1. **Run the application**:
    ```bash
    uvicorn main:app --reload
    ```

2. **Interact with the chatbot**:
    - Access the chatbot through the provided UI.
    - Ask questions like "How many properties are commercial?" or "Show me the total tax paid in 2023."

3. **Continuous Learning (Future Feature)**:
    - In future versions, IntelliQuery will learn from user feedback to improve its query generation over time.

### Project Structure

- **`main.py`**: The entry point for the FastAPI application.
- **`chatbot.py`**: Contains the logic for handling user queries, generating SQL, and interacting with the database.
- **`openai_client.py`**: Manages communication with the OpenAI API and handles embeddings.
- **`database.py`**: Manages database connections and interactions.
- **`requirements.txt`**: Lists the Python dependencies required for the project.

### Contributing

If you'd like to contribute to IntelliQuery, please fork the repository and use a feature branch. Pull requests are welcome.


