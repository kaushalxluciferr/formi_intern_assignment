from enum import Enum
from typing import Dict, Any, Optional
from pydantic import BaseModel
import jinja2
import os

class State(str, Enum):
    GREETING = "greeting"
    FAQ = "faq"
    NEW_BOOKING = "new_booking"
    MODIFY_BOOKING = "modify_booking"
    CANCEL_BOOKING = "cancel_booking"
    CONFIRMATION = "confirmation"
    GOODBYE = "goodbye"

class StateContext(BaseModel):
    current_state: State
    previous_state: Optional[State] = None
    entities: Dict[str, Any] = {}
    conversation_history: list[Dict[str, str]] = []

class StateMachine:
    def _init_(self):
        self.template_loader = jinja2.FileSystemLoader(searchpath="./templates")
        self.template_env = jinja2.Environment(loader=self.template_loader)
        self.current_context = StateContext(current_state=State.GREETING)

    def get_state_prompt(self, state: State, context: Dict[str, Any]) -> str:
        template = self.template_env.get_template(f"{state.value}.j2")
        return template.render(**context)

    def transition(self, user_input: str) -> tuple[State, str]:
        current_state = self.current_context.current_state
        response = ""

        if current_state == State.GREETING:
            if "booking" in user_input.lower():
                self.current_context.current_state = State.NEW_BOOKING
                response = self.get_state_prompt(State.NEW_BOOKING, self.current_context.dict())
            elif "faq" in user_input.lower():
                self.current_context.current_state = State.FAQ
                response = self.get_state_prompt(State.FAQ, self.current_context.dict())
            else:
                response = "I can help you with bookings or answer questions about Barbeque Nation. What would you like to do?"

        elif current_state == State.FAQ:
            response = "Here's the information you requested..."
            self.current_context.current_state = State.GREETING

        elif current_state == State.NEW_BOOKING:
            if "confirm" in user_input.lower():
                self.current_context.current_state = State.CONFIRMATION
                response = self.get_state_prompt(State.CONFIRMATION, self.current_context.dict())
            else:
                response = "Please provide the following details for your booking..."

        elif current_state == State.CONFIRMATION:
            self.current_context.current_state = State.GOODBYE
            response = self.get_state_prompt(State.GOODBYE, self.current_context.dict())

        return self.current_context.current_state, response

    def update_context(self, key: str, value: Any):
        self.current_context.entities[key] = value

    def add_to_history(self, role: str, content: str):
        self.current_context.conversation_history.append({
            "role": role,
            "content": content
        })