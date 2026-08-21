from enum import Enum


class UserRole(str, Enum):
    PATIENT = "PATIENT"
    DOCTOR = "DOCTOR"
    HOSPITAL_ADMIN = "HOSPITAL_ADMIN"
    SYSTEM_ADMIN = "SYSTEM_ADMIN"