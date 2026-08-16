from abc import ABC, abstractmethod

from app.models.conversation import Conversation
from app.models.message import Message


class ConversationRepositoryInterface(ABC):

    @abstractmethod
    def create_conversation(
        self,
        conversation: Conversation
    ) -> Conversation:
        pass

    @abstractmethod
    def find_conversation_by_id(
        self,
        conversation_id: str
    ) -> Conversation | None:
        pass

    @abstractmethod
    def find_conversations_by_patient(
        self,
        patient_id: str
    ) -> list[Conversation]:
        pass

    @abstractmethod
    def save_message(
        self,
        message: Message
    ) -> Message:
        pass

    @abstractmethod
    def find_messages_by_conversation(
        self,
        conversation_id: str
    ) -> list[Message]:
        pass