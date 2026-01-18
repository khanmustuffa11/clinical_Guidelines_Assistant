from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware


from app.rag.generator import ask_guidelines

app = FastAPI(
    title="Clinical Guidelines RAG",
    version="1.1"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    question: str

class AnswerResponse(BaseModel):
    question: str
    answer: str
    sources: List[str]
    
@app.get("/")
def root():
    return {"message": "Clinical Guidelines RAG is running"}

from fastapi import HTTPException
from fastapi.concurrency import run_in_threadpool

# @app.post("/ask", response_model=AnswerResponse)
# async def ask(query: Query):
#     try:
#         # 🔒 Run RAG outside the event loop (Windows-safe)
#         result = await run_in_threadpool(
#             ask_guidelines,
#             query.question
#         )
#         return result

#     except Exception as e:
#         # This will now ALWAYS catch failures
#         raise HTTPException(
#             status_code=500,
#             detail=str(e)
#         )

from fastapi import HTTPException
import traceback

@app.post("/ask")
async def ask(query: Query):
    try:
        result = await run_in_threadpool(
            ask_guidelines,
            query.question
        )
        return result

    except Exception as e:
        # 🔥 FORCE the traceback to appear in the terminal
        print("\n❌ EXCEPTION IN /ask ❌")
        traceback.print_exc()

        # Return the error text so Swagger shows it
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

