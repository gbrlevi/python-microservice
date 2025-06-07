import os
from pymongo import MongoClient

MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://gablevi:[PASSWORD]@cluster0.rd6h9an.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

client = MongoClient(MONGO_URI)

db = client.nutri_db

planos_mestre_collection = db["planos_mestre"]
itens_plano_collection = db["itens_plano"]