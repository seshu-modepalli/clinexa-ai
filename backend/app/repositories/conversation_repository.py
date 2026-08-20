from datetime import datetime, timezone

from pymongo.database import Database

from app.models.conversation import Conversation
from app.models.message import Message
from app.repositories.conversation_repository_interface import (
    ConversationRepositoryInterface
)


class MongoConversationRepository(
    ConversationRepositoryInterface
):

    CONVERSATIONS_COLLECTION = "conversations"
    MESSAGES_COLLECTION = "messages"

    def __init__(self, database: Database):

        self.conversations = database[
            self.CONVERSATIONS_COLLECTION
        ]

        self.messages = database[
            self.MESSAGES_COLLECTION
        ]

    def create_conversation(
        self,
        conversation: Conversation
    ) -> Conversation:

        document = {
            "conversation_id": conversation.conversation_id,
            "patient_id": conversation.patient_id,
            "title": conversation.title,
            "created_at": conversation.created_at,
            "updated_at": conversation.updated_at,
        }

        self.conversations.insert_one(document)

        return conversation

    def find_conversation_by_id(
        self,
        conversation_id: str
    ) -> Conversation | None:

        document = self.conversations.find_one(
            {
                "conversation_id": conversation_id
            }
        )

        if document is None:
            return None

        return self._to_conversation(document)

    def find_conversations_by_patient(
        self,
        patient_id: str
    ) -> list[Conversation]:

        documents = self.conversations.find(
            {
                "patient_id": patient_id
            }
        ).sort(
            "updated_at",
            -1
        )

        return [
            self._to_conversation(document)
            for document in documents
        ]

    def save_message(
        self,
        message: Message
    ) -> Message:

        document = {
            "message_id": message.message_id,
            "conversation_id": message.conversation_id,
            "role": message.role,
            "content": message.content,
            "created_at": message.created_at,
        }

        self.messages.insert_one(document)
        self.conversations.update_one(
            {
                "conversation_id": message.conversation_id
            },
            {
                "$set": {
                    "updated_at": datetime.now(timezone.utc)
                }
            }
        )
        return message

    def find_messages_by_conversation(
        self,
        conversation_id: str
    ) -> list[Message]:

        documents = self.messages.find(
            {
                "conversation_id": conversation_id
            }
        ).sort(
            "created_at",
            1
        )

        return [
            self._to_message(document)
            for document in documents
        ]

    @staticmethod
    def _to_conversation(
        document: dict
    ) -> Conversation:

        return Conversation(
            conversation_id=document[
                "conversation_id"
            ],
            patient_id=document[
                "patient_id"
            ],
            title=document["title"],
            created_at=document["created_at"],
            updated_at=document["updated_at"],
        )

    @staticmethod
    def _to_message(
        document: dict
    ) -> Message:

        return Message(
            message_id=document[
                "message_id"
            ],
            conversation_id=document[
                "conversation_id"
            ],
            role=document["role"],
            content=document["content"],
            created_at=document["created_at"],
        )