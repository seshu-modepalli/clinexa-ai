from dataclasses import dataclass
import datetime


@dataclass
class Conversation:
    conversation_id: str
    patient_id: str
    title: str
    created_at: datetime
    updated_at: datetime
    
