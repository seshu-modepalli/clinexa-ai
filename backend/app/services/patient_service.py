from datetime import datetime, timezone
from uuid import uuid4

from app.core.exceptions import (
    ResourceAlreadyExistsException,
    ResourceNotFoundException
)
from app.core.logging_core import logger
from app.models.patient import Patient
from app.repositories.patient_repository_interface import (
    PatientRepositoryInterface
)
from app.schemas.patient import PatientCreate, PatientUpdate


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

        existing_patient = self.repository.find_by_email(
            patient_data.email
        )

        if existing_patient is not None:
            raise ResourceAlreadyExistsException(
                f"Patient with email '{patient_data.email}' already exists"
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

    def update_patient(
        self,
        patient_id: str,
        patient_data: PatientUpdate
    ) -> Patient:

        logger.info(
            "Updating patient | patient_id=%s",
            patient_id
        )

        existing_patient = self.repository.find_by_id(
            patient_id
        )

        if existing_patient is None:
            raise ResourceNotFoundException(
                f"Patient with id '{patient_id}' not found"
            )

        # Check whether the new email belongs to another patient
        email_patient = self.repository.find_by_email(
            patient_data.email
        )

        if (
            email_patient is not None
            and email_patient.patient_id != patient_id
        ):
            raise ResourceAlreadyExistsException(
                f"Patient with email '{patient_data.email}' already exists"
            )

        updated_patient = Patient(
            patient_id=patient_id,
            name=patient_data.name,
            age=patient_data.age,
            gender=patient_data.gender,
            phone=patient_data.phone,
            email=patient_data.email,
            created_at=existing_patient.created_at,
        )

        return self.repository.update(
            updated_patient
        )

    def delete_patient(
        self,
        patient_id: str
    ) -> None:

        logger.info(
            "Deleting patient | patient_id=%s",
            patient_id
        )

        existing_patient = self.repository.find_by_id(
            patient_id
        )

        if existing_patient is None:
            raise ResourceNotFoundException(
                f"Patient with id '{patient_id}' not found"
            )

        self.repository.delete(patient_id)