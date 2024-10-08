from fastapi import HTTPException
from uuid import UUID
from api.services.db import connect_mongo


async def get_not_recovered_cows(farm_id: UUID):
    collection, client = connect_mongo("cattles")

    try:
        farm_id = str(farm_id)
        not_recovered_cows = []

        for cattle in collection.find({"farm_id": farm_id}):
            cattle_number = cattle.get("number")
            health_history = cattle.get("health_history", [])
            vaccines = cattle.get("vaccines", [])  # Obter a lista de vacinas
            diseases_not_recovered = []
            disease_vaccines = {}

            # Verifica se existe um registro de "Not Recovered" sem um subsequente "Recovered"
            for record in health_history:
                if record.get("status") == "Not Recovered":
                    disease = record.get("disease")
                    # Verifica se não há um "Recovered" para essa doença
                    if not any(
                        r.get("disease") == disease
                        and r.get("status") == "Recovered"
                        and r["date"] > record["date"]
                        for r in health_history
                    ):
                        diseases_not_recovered.append(disease)

            # Cria um dicionário para armazenar as vacinas relacionadas às doenças
            for disease in diseases_not_recovered:
                disease_vaccines[disease] = next(
                    (vaccine for vaccine in vaccines if vaccine["type"] == disease),
                    None,
                )

            formatted_vaccines = []
            for disease in diseases_not_recovered:
                vaccine = disease_vaccines[disease]
                if vaccine:
                    formatted_vaccines.append(
                        {"type": disease, "date": vaccine["date"]}
                    )
                else:
                    formatted_vaccines.append({"type": disease, "date": "Não tomou"})

            if diseases_not_recovered:
                not_recovered_cows.append(
                    {
                        "cattle_number": cattle_number,
                        "diseases": diseases_not_recovered,
                        "vaccines": formatted_vaccines,
                    }
                )

        return not_recovered_cows

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro ao obter vacas não recuperadas: {e}"
        )
