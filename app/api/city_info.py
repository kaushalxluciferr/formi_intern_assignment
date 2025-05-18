from fastapi import APIRouter, HTTPException
from app.models.city_models import CityData
import os
import json

router = APIRouter()

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(CURRENT_DIR)), "data", "knowledge_base")

@router.get("/cities/{city_name}", response_model=CityData)
async def get_city_data(city_name: str):
    normalized_city = city_name.lower().replace(" ", "_")
    matched_files = [
        f for f in os.listdir(DATA_PATH)
        if f.lower().startswith(normalized_city) and f.endswith(".json")
    ]
    if not matched_files:
        raise HTTPException(status_code=404, detail=f"No data found for city '{city_name}'.")

    branches = []
    city_value = city_name.title()

    for file_name in matched_files:
        file_path = os.path.join(DATA_PATH, file_name)
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if "branches" in data:
                branches.extend(data["branches"])
            if "city" in data:
                city_value = data["city"]  # Override with actual name

    return CityData(city=city_value, branches=branches)