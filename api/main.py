from dotenv import load_dotenv
import os

load_dotenv()

print("KEY", os.getenv("OPENAI_API_KEY"))
from model import kanoni

from fastapi import FastAPI


app = FastAPI()


@app.get("/")
async def root(query: str):
    # Call the RAG model with the query
    ans = kanoni.rag_chain.invoke(query)
    # Return the answer as a JSON response
    return {"answer": ans}
