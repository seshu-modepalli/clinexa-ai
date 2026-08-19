from datetime import datetime, timezone
from uuid import uuid4

from app.core.constants import USER_ROLE
from app.core.exceptions import ResourceNotFoundException
from app.models.conversation import Conversation
from app.models.message import Message
from app.repositories.conversation_repository_interface import (
    ConversationRepositoryInterface
)
from app.schemas.conversation import ConversationCreate
from app.schemas.message import MessageCreate


class ConversationService:

    def __init__(
        self,
        repository: ConversationRepositoryInterface
    ):
        self.repository = repository

    def create_conversation(
        self,
        conversation_data: ConversationCreate
    ) -> Conversation:

        now = datetime.now(timezone.utc)

        conversation = Conversation(
            conversation_id=str(uuid4()),
            patient_id=conversation_data.patient_id,
            title=conversation_data.title,
            created_at=now,
            updated_at=now
        )

        return self.repository.create_conversation(
            conversation
        )

    def get_conversation(
        self,
        conversation_id: str
    ) -> Conversation:

        conversation = (
            self.repository.find_conversation_by_id(
                conversation_id
            )
        )

        if conversation is None:
            raise ResourceNotFoundException(
                f"Conversation '{conversation_id}' not found"
            )

        return conversation

    def get_patient_conversations(
        self,
        patient_id: str
    ) -> list[Conversation]:

        return (
            self.repository.find_conversations_by_patient(
                patient_id
            )
        )

    def add_message(
        self,
        conversation_id: str,
        message_data: MessageCreate
    ) -> Message:

        conversation = (
            self.repository.find_conversation_by_id(
                conversation_id
            )
        )

        if conversation is None:
            raise ResourceNotFoundException(
                f"Conversation '{conversation_id}' not found"
            )

        message = Message(
            message_id=str(uuid4()),
            conversation_id=conversation_id,
            role=USER_ROLE,
            content=message_data.content,
            created_at=datetime.now(timezone.utc)
        )

        saved_message = self.repository.save_message(
            message
        )

        return saved_message

    def get_messages(
        self,
        conversation_id: str
    ) -> list[Message]:

        conversation = (
            self.repository.find_conversation_by_id(
                conversation_id
            )
        )

        if conversation is None:
            raise ResourceNotFoundException(
                f"Conversation '{conversation_id}' not found"
            )

        return (
            self.repository.find_messages_by_conversation(
                conversation_id
            )
        )