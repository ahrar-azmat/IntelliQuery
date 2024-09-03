from fastapi import FastAPI
from chatbot import handle_chat
from schemas import QueryRequest

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Welcome to PropertyTaxBot API!"}

@app.post("/chat/")
async def chat(query_request: QueryRequest):
    response = await handle_chat(query_request.query)
    return response
