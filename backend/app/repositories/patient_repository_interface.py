from abc import ABC, abstractmethod

from app.models.patient import Patient


class PatientRepositoryInterface(ABC):

    @abstractmethod
    def create(self, patient: Patient) -> Patient:
        pass

    @abstractmethod
    def find_by_id(self, patient_id: str) -> Patient | None:
        pass

    @abstractmethod
    def find_all(self) -> list[Patient]:
        pass
    @abstractmethod
    def find_all(self) -> list[Patient]:
        pass

    @abstractmethod
    def update(self, patient: Patient) -> Patient:
        pass

    @abstractmethod
    def delete(self, patient_id: str) -> bool:
        pass