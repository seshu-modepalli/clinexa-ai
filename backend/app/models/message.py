from dataclasses import dataclass
from datetime import datetime

@dataclass
class Message:
    message_id: int
    conversation_id: str
    role: str
    content: str
    created_at: datetime