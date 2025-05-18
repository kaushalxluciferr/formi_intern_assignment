from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import knowledge_base, chatbot, post_call

app = FastAPI(
    title="Barbeque Nation Chatbot API",
    description="API for Barbeque Nation's conversational AI agent",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(knowledge_base.router, prefix="/api/kb", tags=["Knowledge Base"])
app.include_router(chatbot.router, prefix="/api/chat", tags=["Chatbot"])
app.include_router(post_call.router, prefix="/api/analysis", tags=["Post-Call Analysis"])

@app.get("/")
async def root():
    return {"message": "Welcome to Barbeque Nation Chatbot API"}