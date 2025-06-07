from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import planos

app = FastAPI(
    title="API de Planos Alimentares",
    description="Microserviço responsável por gerenciar planos alimentares e seus itens.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(planos.router, prefix="/planos", tags=["Planos Alimentares"])

@app.get("/", tags=["Root"])
def read_root():
    return {"status": "API de Planos Alimentares está online!"}