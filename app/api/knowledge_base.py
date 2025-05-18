from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict
import json
from pathlib import Path
from datetime import datetime
import os
from app.utils.token_manager import TokenManager
from app.core.config import settings

router = APIRouter()
token_manager = TokenManager()

# Models
class Query(BaseModel):
    text: str
    property: Optional[str] = None
    category: Optional[str] = None

class KnowledgeResponse(BaseModel):
    content: str
    source: str
    confidence: float
    tokens: int

class TimingSlot(BaseModel):
    opening_time: str
    last_entry_time: str
    closing_time: str

class DayTimings(BaseModel):
    lunch: TimingSlot
    dinner: TimingSlot

class BranchInfo(BaseModel):
    address: str
    bar_availability: str
    valet_parking: str
    baby_chair: str
    lift_availability: str
    pdr_availability: str
    pdr_capacity: int
    pdr_minimum_pax_required: int
    outlet_numbers: List[str]

class NearestOutlet(BaseModel):
    name: str
    distance: str
    address: str

class Offers(BaseModel):
    early_bird: str
    kitty_party: str
    student_offer: str
    five_plus_one_buffet: str
    army_offer: str
    drinks_offer: str

class AdditionalInfo(BaseModel):
    complimentary_drinks: str
    food_festival: str

class Branch(BaseModel):
    name: str
    modified_on: str
    booking_instructions: Dict[str, Dict[str, Dict[str, str]]]
    branch_info: BranchInfo
    branch_timings: Dict[str, DayTimings]
    additional_info: AdditionalInfo
    nearest_outlets: List[NearestOutlet]
    offers: Offers

class CityResponse(BaseModel):
    city: str
    branches: List[Branch]

# Data loading
def load_city_data():
    city_data = {}
    knowledge_base_path = Path(settings.KNOWLEDGE_BASE_PATH)
    
    for file in knowledge_base_path.glob("*.json"):
        try:
            with open(file, "r", encoding="utf-8") as f:
                data = json.load(f)
                
                # Handle both city files and branch files
                if "city" in data:
                    city_name = data["city"]
                    if city_name not in city_data:
                        city_data[city_name] = []
                    city_data[city_name].extend(data["branches"])
                else:
                    # Assume it's a branch file
                    branch_name = file.stem.replace("_", " ")
                    if "Delhi" in branch_name or "delhi" in branch_name.lower():
                        city_name = "Delhi"
                    elif "Bangalore" in branch_name or "bangalore" in branch_name.lower():
                        city_name = "Bangalore"
                    else:
                        continue
                        
                    if city_name not in city_data:
                        city_data[city_name] = []
                    city_data[city_name].append(data)
                    
        except Exception as e:
            print(f"Error loading {file}: {str(e)}")
    
    return city_data

# Load data at startup
city_data = load_city_data()

# API Endpoints
@router.get("/properties")
async def get_properties():
    return {
        "properties": [
            {"id": "Delhi", "name": "BBQ Nation Delhi"},
            {"id": "Bangalore", "name": "BBQ Nation Bangalore"}
        ]
    }

@router.get("/cities/{city_name}", response_model=CityResponse)
async def get_city_info(city_name: str):
    normalized_name = city_name.replace("_", " ").title()
    
    if normalized_name not in city_data:
        raise HTTPException(status_code=404, detail="City not found")
    
    return {"city": normalized_name, "branches": city_data[normalized_name]}

@router.get("/branches/{branch_name}", response_model=Branch)
async def get_branch_info(branch_name: str):
    normalized_name = branch_name.replace("_", " ").title()
    
    for city, branches in city_data.items():
        for branch in branches:
            if branch["name"].lower() == normalized_name.lower():
                return branch
    
    raise HTTPException(status_code=404, detail="Branch not found")

@router.post("/query", response_model=KnowledgeResponse)
async def query_knowledge_base(query: Query):
    try:
        response_content = ""
        source = "knowledge_base"
        confidence = 0.9
        tokens = 0
        
        # Handle menu queries
        if query.category and query.category.lower() == "menu":
            menu_data = {}
            menu_path = Path(settings.KNOWLEDGE_BASE_PATH) / "menu_list.json"
            drink_path = Path(settings.KNOWLEDGE_BASE_PATH) / "menu_drink.json"
            
            if menu_path.exists():
                with open(menu_path, "r") as f:
                    menu_data = json.load(f)
            
            if drink_path.exists():
                with open(drink_path, "r") as f:
                    menu_data.update(json.load(f))
            
            if query.property:
                response_content = menu_data.get(query.property, "No menu found for this location")
            else:
                response_content = "Available menus: " + ", ".join(menu_data.keys())
            
            tokens = len(response_content.split())
        
        # Handle location-specific queries
        elif query.property:
            if query.property.lower() in ["delhi", "bangalore"]:
                city_info = city_data.get(query.property.title(), [])
                response_content = f"Information for {query.property}: {len(city_info)} branches available"
            else:
                branch = next(
                    (b for branches in city_data.values() 
                     for b in branches 
                     if b["name"].lower() == query.property.lower()),
                    None
                )
                response_content = branch if branch else "Branch not found"
            
            tokens = len(str(response_content).split())
        
        else:
            response_content = "Please specify a property or category"
            tokens = len(response_content.split())
        
        # Token limit check
        if tokens > 800:
            response_content = token_manager.truncate_response(response_content)
            tokens = len(response_content.split())
        
        return KnowledgeResponse(
            content=response_content,
            source=source,
            confidence=confidence,
            tokens=tokens
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/categories")
async def get_categories():
    return {
        "categories": [
            "menu",
            "pricing",
            "location",
            "hours",
            "booking",
            "faq"
        ]
    }