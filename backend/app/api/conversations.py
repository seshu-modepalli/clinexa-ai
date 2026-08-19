from fastapi import APIRouter, Depends, status

from app.database.dependencies import get_database
from app.repositories.conversation_repository import (
    MongoConversationRepository
)
from app.schemas.conversation import (
    ConversationCreate,
    ConversationResponse
)
from app.schemas.message import (
    MessageCreate,
    MessageResponse
)
from app.services.conversation_service import (
    ConversationService
)


router = APIRouter(
    prefix="/api/v1",
    tags=["Conversations"]
)


def get_conversation_service(
    database=Depends(get_database)
) -> ConversationService:

    repository = MongoConversationRepository(
        database
    )

    return ConversationService(repository)


@router.post(
    "/conversations",
    response_model=ConversationResponse,
    status_code=status.HTTP_201_CREATED
)
def create_conversation(
    conversation_data: ConversationCreate,
    service: ConversationService = Depends(
        get_conversation_service
    )
):

    return service.create_conversation(
        conversation_data
    )


@router.get(
    "/conversations/{conversation_id}",
    response_model=ConversationResponse
)
def get_conversation(
    conversation_id: str,
    service: ConversationService = Depends(
        get_conversation_service
    )
):

    return service.get_conversation(
        conversation_id
    )


@router.get(
    "/patients/{patient_id}/conversations",
    response_model=list[ConversationResponse]
)
def get_patient_conversations(
    patient_id: str,
    service: ConversationService = Depends(
        get_conversation_service
    )
):

    return service.get_patient_conversations(
        patient_id
    )


@router.post(
    "/conversations/{conversation_id}/messages",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED
)
def add_message(
    conversation_id: str,
    message_data: MessageCreate,
    service: ConversationService = Depends(
        get_conversation_service
    )
):

    return service.add_message(
        conversation_id,
        message_data
    )


@router.get(
    "/conversations/{conversation_id}/messages",
    response_model=list[MessageResponse]
)
def get_messages(
    conversation_id: str,
    service: ConversationService = Depends(
        get_conversation_service
    )
):

    return service.get_messages(
        conversation_id
    )