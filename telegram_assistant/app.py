import inspect
import src.rag_engine
print("📦 rag_engine path:", inspect.getfile(src.rag_engine))


from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src.rag_engine import answer_question

app = FastAPI()

# Разрешить фронтенду доступ
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

class QuestionRequest(BaseModel):
    question: str
    history: list[str]
    mode: str = "short"

import time

@app.post("/ask")
async def ask_question(req: QuestionRequest):
    start = time.time()

    print(f"🔥 Вопрос: {req.question} (mode: {req.mode})", end=" ", flush=True)

    answer = answer_question(req.question)

    elapsed = round(time.time() - start, 2)
    print(f"⏱️ за {elapsed} сек.")
    return {"answer": answer}
