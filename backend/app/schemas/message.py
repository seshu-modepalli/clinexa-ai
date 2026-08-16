from pydantic import BaseModel, Field


class MessageCreate(BaseModel):
    content: str = Field(
        ...,
        min_length=1,
        max_length=5000
    )


class MessageResponse(BaseModel):
    message_id: str
    conversation_id: str
    role: str
    content: str
    created_at: str