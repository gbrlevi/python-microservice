from pydantic import BaseModel

class Plano(BaseModel):  
    id: int
    refeicao: str
    qtd: int
    horario: str
    