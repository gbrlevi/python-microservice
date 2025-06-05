def individual_plano(plano):
    return {
        "id": str(plano["_id"]),
        "refeicao": plano["refeicao"],
        "qtd": plano["qtd"],
        "horario": plano["horario"]
    }

def all_planos(planos):
    return [individual_plano(plano) for plano in planos]