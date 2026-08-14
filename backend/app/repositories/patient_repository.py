from datetime import datetime, timezone
from uuid import uuid4

from pymongo.database import Database

from app.models.patient import Patient
from app.repositories.patient_repository_interface import (
    PatientRepositoryInterface
)

class MongoPatientRepository(PatientRepositoryInterface):

    COLLECTION_NAME = "patients"

    def __init__(self, database: Database):
        self.collection = database[self.COLLECTION_NAME]

    def create(self, patient: Patient) -> Patient:

        document = {
            "patient_id": patient.patient_id,   
            "name": patient.name,
            "age": patient.age,
            "gender": patient.gender,
            "phone": patient.phone,
            "email": patient.email,
            "created_at": patient.created_at,
        }

        self.collection.insert_one(document)

        return patient

    def find_by_id(self, patient_id: str) -> Patient | None:

        document = self.collection.find_one(
            {"patient_id": patient_id}
        )

        if document is None:
            return None

        return Patient(
            patient_id=document["patient_id"],
            name=document["name"],
            age=document["age"],
            gender=document["gender"],
            phone=document["phone"],
            email=document["email"],
            created_at=document["created_at"],
        )

    def find_all(self) -> list[Patient]:

        patients = []

        for document in self.collection.find():
            patients.append(
                Patient(
            patient_id=document["patient_id"],
            name=document["name"],
            age=document["age"],
            gender=document["gender"],
            phone=document["phone"],
            email=document["email"],
            created_at=document["created_at"],
        )
            )

        return patients
    def find_by_email(
        self,
        email: str
    ) -> Patient | None:

        document = self.collection.find_one(
            {"email": email}
        )

        if document is None:
            return None

        return self._to_patient(document)
    def update(
        self,
        patient: Patient
    ) -> Patient:

        self.collection.update_one(
            {"patient_id": patient.patient_id},
            {
                "$set": {
                    "name": patient.name,
                    "age": patient.age,
                    "gender": patient.gender,
                    "phone": patient.phone,
                    "email": patient.email,
                }
            }
        )

        return patient

    def delete(
        self,
        patient_id: str
    ) -> bool:

        result = self.collection.delete_one(
            {"patient_id": patient_id}
        )

        return result.deleted_count > 0

    @staticmethod
    def _to_patient(document: dict) -> Patient:

        return Patient(
            patient_id=document["patient_id"],
            name=document["name"],
            age=document["age"],
            gender=document["gender"],
            phone=document["phone"],
            email=document["email"],
            created_at=document["created_at"],
        )