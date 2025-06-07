from fastapi import APIRouter, HTTPException, Body, status
from typing import List
from pymongo import ReturnDocument
from .. import models
from ..config import planos_mestre_collection, itens_plano_collection
from ..models import PyObjectId
from datetime import datetime, date

router = APIRouter()

@router.post("/", response_model=models.PlanoMestre, status_code=status.HTTP_201_CREATED)
async def create_plano_mestre(plano_data: models.PlanoMestreCreate):
    
    plano_dict = plano_data.model_dump()

    for key, value in plano_dict.items():
        if isinstance(value, date):
            plano_dict[key] = datetime.combine(value, datetime.min.time())

    result = planos_mestre_collection.insert_one(plano_dict)
    plano_criado = planos_mestre_collection.find_one({"_id": result.inserted_id})

    return plano_criado

@router.get("/", response_model=List[models.PlanoMestre])
async def get_all_planos_mestre():
    planos_cursor = planos_mestre_collection.find()
    return list(planos_cursor)

@router.get("/{plano_id}", response_model=models.PlanoMestreComItens)
async def get_plano_mestre(plano_id: PyObjectId):
    plano_mestre_db = planos_mestre_collection.find_one({"_id": plano_id})
    if not plano_mestre_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plano Mestre não encontrado")

    itens_db = itens_plano_collection.find({"plano_mestre_id": plano_id})
    
    resposta_completa = {
        **plano_mestre_db,
        "itens": list(itens_db)
    }
    return resposta_completa

@router.put("/{plano_id}", response_model=models.PlanoMestre)
async def update_plano_mestre(plano_id: PyObjectId, plano_data: models.PlanoMestreBase):
    update_dict = plano_data.model_dump(exclude_unset=True)

    for key, value in update_dict.items():
        if isinstance(value, date):
            update_dict[key] = datetime.combine(value, datetime.min.time())

    if not update_dict:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Nenhum dado fornecido para atualização")

    updated_plano = planos_mestre_collection.find_one_and_update(
        {"_id": plano_id},
        {"$set": update_dict},
        return_document=ReturnDocument.AFTER
    )
    if not updated_plano:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plano Mestre não encontrado")
    
    return updated_plano

@router.delete("/{plano_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_plano_mestre(plano_id: PyObjectId):
    itens_plano_collection.delete_many({"plano_mestre_id": plano_id})
    result = planos_mestre_collection.delete_one({"_id": plano_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plano Mestre não encontrado")
    return

@router.post("/itens/", response_model=models.ItemPlano, status_code=status.HTTP_201_CREATED)
async def create_item_plano(item_data: models.ItemPlanoCreate):
    if not planos_mestre_collection.find_one({"_id": item_data.plano_mestre_id}):
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Plano Mestre com ID '{item_data.plano_mestre_id}' não encontrado.")
    
    item_dict = {
        "plano_mestre_id": item_data.plano_mestre_id, 
        "horario": item_data.horario,
        "nome_refeicao": item_data.nome_refeicao,
        "descricao": item_data.descricao
    }

    result = itens_plano_collection.insert_one(item_dict)
    item_criado = itens_plano_collection.find_one({"_id": result.inserted_id})
    return item_criado

@router.get("/{plano_id}/itens", response_model=List[models.ItemPlano])
async def get_itens_for_plano(plano_id: PyObjectId):
    if not planos_mestre_collection.find_one({"_id": plano_id}):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plano Mestre não encontrado")

    itens_cursor = itens_plano_collection.find({"plano_mestre_id": plano_id})
    return list(itens_cursor)


@router.get("/itens/{item_id}", response_model=models.ItemPlano)
async def get_item_plano(item_id: PyObjectId):
    item_db = itens_plano_collection.find_one({"_id": item_id})
    if not item_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Item de Plano com ID '{item_id}' não encontrado.")
    return item_db

@router.put("/itens/{item_id}", response_model=models.ItemPlano)
async def update_item_plano(item_id: PyObjectId, item_data: models.ItemPlanoBase):
    update_dict = item_data.model_dump()
    updated_item = itens_plano_collection.find_one_and_update(
        {"_id": item_id},
        {"$set": update_dict},
        return_document=ReturnDocument.AFTER
    )
    if not updated_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Item de Plano com ID '{item_id}' não encontrado.")
    return updated_item

@router.delete("/itens/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item_plano(item_id: PyObjectId):
    result = itens_plano_collection.delete_one({"_id": item_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Item de Plano com ID '{item_id}' não encontrado.")
    return