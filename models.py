from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date
from bson import ObjectId
from typing import Any
from pydantic_core import core_schema

class PyObjectId(ObjectId):
    """
    Classe customizada para funcionar como um tipo nos modelos Pydantic,
    garantindo validação e serialização corretas para ObjectIds do MongoDB.
    """
    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: Any
    ) -> core_schema.CoreSchema:
        def validate_from_str(value: str) -> ObjectId:
            if not ObjectId.is_valid(value):
                raise ValueError("Invalid ObjectId")
            return ObjectId(value)

        python_schema = core_schema.union_schema(
            [
                core_schema.is_instance_schema(ObjectId),
                core_schema.no_info_plain_validator_function(validate_from_str),
            ]
        )

        serialization_schema = core_schema.plain_serializer_function_ser_schema(
            lambda x: str(x)
        )

        return core_schema.json_or_python_schema(
            json_schema=core_schema.str_schema(),
            python_schema=python_schema,
            serialization=serialization_schema,
        )

class ItemPlanoBase(BaseModel):
    horario: str
    nome_refeicao: str
    descricao: str

class ItemPlanoCreate(ItemPlanoBase):
    plano_mestre_id: PyObjectId

class ItemPlano(ItemPlanoBase):
    id: PyObjectId = Field(alias="_id")
    plano_mestre_id: PyObjectId

    class Config:
        populate_by_name = True

class PlanoMestreBase(BaseModel):
    paciente_id: str
    nutricionista_id: str
    titulo: str
    data_inicio: Optional[date] = None
    data_fim: Optional[date] = None
    
    class Config:
        json_encoders = {date: lambda d: d.isoformat()}


class PlanoMestreCreate(PlanoMestreBase):
    pass

class PlanoMestre(PlanoMestreBase):
    id: PyObjectId = Field(alias="_id")

    class Config:
        populate_by_name = True

class PlanoMestreComItens(PlanoMestre):
    itens: List[ItemPlano] = []