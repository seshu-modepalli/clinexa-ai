from datetime import datetime, timezone
from uuid import uuid4

from app.core.exceptions import ResourceNotFoundException
from app.core.logging_core import logger
from app.models.patient import Patient
from app.repositories.patient_repository_interface import (
    PatientRepositoryInterface
)
from app.schemas.patient import PatientCreate


class PatientService:

    def __init__(
        self,
        repository: PatientRepositoryInterface
    ):
        self.repository = repository

    def create_patient(
        self,
        patient_data: PatientCreate
    ) -> Patient:

        logger.info(
            "Creating patient | name=%s",
            patient_data.name
        )

        patient = Patient(
            patient_id=str(uuid4()),
            name=patient_data.name,
            age=patient_data.age,
            gender=patient_data.gender,
            phone=patient_data.phone,
            email=patient_data.email,
            created_at=datetime.now(timezone.utc),
        )

        return self.repository.create(patient)

    def get_patient(
        self,
        patient_id: str
    ) -> Patient:

        logger.info(
            "Fetching patient | patient_id=%s",
            patient_id
        )

        patient = self.repository.find_by_id(
            patient_id
        )

        if patient is None:
            raise ResourceNotFoundException(
                f"Patient with id '{patient_id}' not found"
            )

        return patient

    def get_all_patients(self) -> list[Patient]:

        logger.info("Fetching all patients")

        return self.repository.find_all()