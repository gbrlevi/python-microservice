from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware     
from config import collection
from database.schema import *
from database.models import *

app = FastAPI()
router = APIRouter()

@app.get("/planos")
async def get_planos():
    data = collection.find()
    return all_planos(data)

@app.get("/planos/{plano_id}")
async def get_plano(plano_id: str):
    plano = collection.find_one({"_id": plano_id})
    if plano:
        return individual_plano(plano)
    return {"error": "Plano not found"}

@app.post("/planos")
async def create_plano(plano: Plano):
    result = collection.insert_one(plano)
    return {"status_code":200 ,"id": str(result.inserted_id)}

@app.put("/planos/{plano_id}")
async def update_plano(plano_id: str, plano: Plano):
    result = collection.update_one({"_id": plano_id}, {"$set": plano})
    if result.modified_count:
        return {"message": "Plano updated successfully"}
    return {"error": "Plano not found or no changes made"}

@app.delete("/planos/{plano_id}")
async def delete_plano(plano_id: str):
    result = collection.delete_one({"_id": plano_id})
    if result.deleted_count:
        return {"message": "Plano deleted successfully"}
    return {"error": "Plano not found"}

app.include_router(router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)