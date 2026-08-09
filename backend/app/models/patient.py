from dataclasses import dataclass
from datetime import datetime
@dataclass
class Patient:
    patient_id: int
    name: str
    age: int
    gender: str
    phone: str
    email: str
    created_at: datetime





