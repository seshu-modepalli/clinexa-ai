from datetime import datetime, timezone
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException

from app.database.dependencies import get_database
from app.repositories.patient_repository import (
    MongoPatientRepository
)
from app.schemas.patient import PatientCreate, PatientResponse
from app.services.patient_service import PatientService
from app.schemas.patient import (
    PatientCreate,
    PatientResponse
)

router = APIRouter(
    prefix="/api/v1/patients",
    tags=["Patients"]
)


def get_patient_service(
    database=Depends(get_database)
) -> PatientService:

    repository = MongoPatientRepository(database)

    return PatientService(repository)


@router.post(
    "",
    response_model=PatientResponse,
    status_code=201
)
def create_patient(
    patient_data: PatientCreate,
    service: PatientService = Depends(
        get_patient_service
    ),
):

    return service.create_patient(patient_data)


@router.get(
    "/{patient_id}",
    response_model=PatientResponse
)
def get_patient(
    patient_id: str,
    service: PatientService = Depends(
        get_patient_service
    ),
):

    return service.get_patient(patient_id)

    return patient


@router.get(
    "",
    response_model=list[PatientResponse]
)
def get_patients(
    service: PatientService = Depends(
        get_patient_service
    ),
):

    return service.get_all_patients()