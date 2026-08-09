from pydantic import BaseModel, EmailStr, Field


class PatientCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    age: int = Field(..., ge=0, le=120)
    gender: str = Field(..., min_length=1, max_length=20)
    phone: str = Field(..., min_length=7, max_length=20)
    email: EmailStr


class PatientResponse(BaseModel):
    patient_id: str
    name: str
    age: int
    gender: str
    phone: str
    email: EmailStr