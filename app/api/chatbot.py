from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from app.core.state_machine import StateMachine
from app.api.knowledge_base import query_knowledge_base, Query
from app.services.conversation_logger import ConversationLogger
from datetime import datetime
import re

router = APIRouter()
state_machine = StateMachine()
conversation_logger = ConversationLogger()

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    phone_number: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    state: str
    session_id: str

@router.post("/message")
async def handle_message(request: ChatRequest) -> ChatResponse:
    try:
        new_state, response = state_machine.transition(request.message)
        
        if new_state == "faq":
            kb_response = await query_knowledge_base(
                Query(text=request.message)
            )
            response = kb_response.content
        
        state_machine.add_to_history("user", request.message)
        state_machine.add_to_history("assistant", response)
        
        if "booking" in request.message.lower() or "confirm" in request.message.lower():
            await log_conversation(
                modality="Chatbot",
                phone_number=request.phone_number,
                message=request.message,
                response=response
            )
        
        return ChatResponse(
            response=response,
            state=new_state,
            session_id=request.session_id or "new_session"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history/{session_id}")
async def get_chat_history(session_id: str) -> List[ChatMessage]:
    return [
        ChatMessage(role="system", content="Welcome to Barbeque Nation!"),
        ChatMessage(role="user", content="Hello"),
        ChatMessage(role="assistant", content="How can I help you today?")
    ]

async def log_conversation(
    modality: str,
    phone_number: Optional[str],
    message: str,
    response: str
) -> None:
    try:
        booking_info = extract_booking_info(message, response)
        
        conversation_logger.log_conversation(
            modality=modality,
            phone_number=phone_number,
            call_outcome=determine_call_outcome(message),
            room_name=booking_info.get('room_name'),
            booking_date=booking_info.get('booking_date'),
            booking_time=booking_info.get('booking_time'),
            number_of_guests=booking_info.get('number_of_guests'),
            call_summary=generate_call_summary(message, response)
        )
    except Exception as e:
        print(f"Error logging conversation: {str(e)}")

def extract_booking_info(message: str, response: str) -> Dict[str, Any]:
    info = {
        'room_name': None,
        'booking_date': None,
        'booking_time': None,
        'number_of_guests': None
    }
    
    date_pattern = r'\d{4}-\d{2}-\d{2}'
    date_match = re.search(date_pattern, message) or re.search(date_pattern, response)
    if date_match:
        info['booking_date'] = date_match.group()
    
    time_pattern = r'\d{2}:\d{2}'
    time_match = re.search(time_pattern, message) or re.search(time_pattern, response)
    if time_match:
        info['booking_time'] = time_match.group()
    
    guest_pattern = r'(\d+)\s*(?:people|guests|persons|pax)'
    guest_match = re.search(guest_pattern, message.lower()) or re.search(guest_pattern, response.lower())
    if guest_match:
        info['number_of_guests'] = int(guest_match.group(1))
    
    room_pattern = r'(?:book|reserve|want)\s+(?:a|an|the)?\s+([A-Za-z\s]+)(?:\s+room)?'
    room_match = re.search(room_pattern, message.lower()) or re.search(room_pattern, response.lower())
    if room_match:
        info['room_name'] = room_match.group(1).strip().title()
    
    return info

def determine_call_outcome(message: str) -> str:
    message = message.lower()
    if "book" in message or "reservation" in message:
        return "Availability"
    elif "change" in message or "modify" in message:
        return "Post-Booking"
    elif "?" in message or "what" in message or "how" in message:
        return "Enquiry"
    else:
        return "Misc"

def generate_call_summary(message: str, response: str) -> str:
    summary = []
    
    if "book" in message.lower():
        summary.append("User requested to make a booking")
    elif "change" in message.lower() or "modify" in message.lower():
        summary.append("User requested to modify a booking")
    elif "cancel" in message.lower():
        summary.append("User requested to cancel a booking")
    else:
        summary.append("User made an enquiry")
    
    if "confirm" in response.lower():
        summary.append("Booking was confirmed")
    elif "sorry" in response.lower() or "unable" in response.lower():
        summary.append("Request could not be fulfilled")
    else:
        summary.append("Information was provided")
    
    return " | ".join(summary)