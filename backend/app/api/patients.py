from datetime import datetime, timezone
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException

from app.database.dependencies import get_database
from app.models.patient import Patient
from app.repositories.patient_repository import PatientRepository
from app.schemas.patient import PatientCreate, PatientResponse


router = APIRouter(
    prefix="/api/v1/patients",
    tags=["Patients"]
)


def get_patient_repository(
    database=Depends(get_database),
):
    return PatientRepository(database)


@router.post(
    "",
    response_model=PatientResponse,
    status_code=201
)
def create_patient(
    patient_data: PatientCreate,
    repository: PatientRepository = Depends(
        get_patient_repository
    ),
):

    patient = Patient(
        patient_id=str(uuid4()),
        name=patient_data.name,
        age=patient_data.age,
        gender=patient_data.gender,
        phone=patient_data.phone,
        email=patient_data.email,
        created_at=datetime.now(timezone.utc),
    )

    return repository.create(patient)


@router.get(
    "/{patient_id}",
    response_model=PatientResponse
)
def get_patient(
    patient_id: str,
    repository: PatientRepository = Depends(
        get_patient_repository
    ),
):

    patient = repository.find_by_id(patient_id)

    if patient is None:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    return patient


@router.get(
    "",
    response_model=list[PatientResponse]
)
def get_patients(
    repository: PatientRepository = Depends(
        get_patient_repository
    ),
):

    return repository.find_all()