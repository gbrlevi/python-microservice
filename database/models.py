from pydantic import BaseModel

class Plano(BaseModel):  
    refeicao: str
    qtd: int
    horario: str
    