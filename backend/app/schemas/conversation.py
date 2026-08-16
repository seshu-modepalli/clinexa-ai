from pydantic import BaseModel, Field


class ConversationCreate(BaseModel):
    patient_id: str = Field(
        ...,
        min_length=1
    )

    title: str = Field(
        default="New Conversation",
        min_length=1,
        max_length=200
    )


class ConversationResponse(BaseModel):
    conversation_id: str
    patient_id: str
    title: str
    created_at: str
    updated_at: str