from pydantic import BaseModel, Field
from typing import List, Optional, Dict

class MealTiming(BaseModel):
    opening_time: str
    last_entry_time: str
    closing_time: str

class DayTiming(BaseModel):
    Lunch: MealTiming
    Dinner: MealTiming

class BranchTimings(BaseModel):
    Monday_to_Friday: DayTiming
    Saturday: DayTiming
    Sunday: DayTiming

class BranchInfo(BaseModel):
    pdr_capacity: Optional[int]
    pdr_minimum_pax_required: Optional[int]

class Branch(BaseModel):
    name: str
    address: str
    booking_instructions: Dict[str, Dict[str, str]] # e.g., { "Monday": { "2+1": "Instruction" } }
    branch_timings: BranchTimings
    branch_info: BranchInfo

class CityData(BaseModel):
    city: str   
    branches: List[Branch]