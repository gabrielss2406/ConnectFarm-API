from datetime import datetime
from fastapi import HTTPException
import requests
from api.services.db import connect_mongo
from api.models.CattleModels import WeightIn


async def create_weight_balance(balanceData: WeightIn):
    collection, client = connect_mongo("cattles")
    try:
        now = datetime.now().strftime("%Y-%m-%d")

        cattle = collection.find_one({"identifier": balanceData.identifier})

        if not cattle:
            raise HTTPException(status_code=404, detail="Cattle not found")

        # Obtém o número da vaca
        cattle_number = cattle.get("number")

        print(cattle_number)

        requests.post(
            "https://connectfarm-localizationsystem-production.up.railway.app/webhook",
            # "http://localhost:3000/webhook",
            json={"weight": round(balanceData.weight, 2), "number": cattle_number},
        )

        result = collection.update_one(
            {"identifier": balanceData.identifier},
            {
                "$push": {
                    "weights": {
                        "date": now,
                        "weight": round(10 * balanceData.weight, 2),
                    }
                }
            },
        )
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Cattle not found")
        return {"message": "Weight added successfully"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f"Error adding weight: {e}")
