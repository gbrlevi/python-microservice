from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.middleware.cors import CORSMiddleware     
from config import collection
from database.schema import *
from database.models import *
from bson import ObjectId

app = FastAPI()
router = APIRouter()

@app.get("/planos")
async def get_planos():
    data = collection.find()
    return all_planos(data)

@app.get("/planos/{plano_id}")
async def get_plano(plano_id: str):
    try:
        obj_id = ObjectId(plano_id) 
    except Exception as e:
        return {"error": "Invalid plano ID format"}
    
    plano = collection.find_one({"_id": obj_id})
    if plano:
        return individual_plano(plano)
    return {"error": "Plano not found"}

@app.post("/planos")
async def create_plano(plano_data: Plano):
    plano = plano_data.model_dump()

    try:
        result = collection.insert_one(plano)
        new_plano = collection.find_one({"_id": result.inserted_id})
        return individual_plano(new_plano)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating plano: {str(e)}")

@app.put("/planos/{plano_id}")
async def update_plano(plano_id: str, plano: Plano):
    plano = plano.model_dump()

    try:
        obj_id = ObjectId(plano_id) 
    except Exception as e:
        return {"error": "Invalid plano ID format"}

    try:
        result = collection.update_one({"_id": obj_id}, {"$set": plano})
        if result.modified_count:
            return {"message": "Plano updated successfully"}
        return {"error": "Plano not found or no changes made"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating plano: {str(e)}")

@app.delete("/planos/{plano_id}")
async def delete_plano(plano_id: str):

    try:
        obj_id = ObjectId(plano_id) 
    except Exception as e:
        return {"error": "Invalid plano ID format"}
    
    result = collection.delete_one({"_id": obj_id})

    if result.deleted_count:
        return {"message": "Plano deleted successfully"}
    return {"error": "Plano not found"}

app.include_router(router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)