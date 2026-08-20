from fastapi import APIRouter, HTTPException

from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_service import ChatService


router = APIRouter(
    prefix="/api/v1/chat",
    tags=["Chat"]
)

chat_service = ChatService()


@router.post("", response_model=ChatResponse)
async def chat(request: ChatRequest):

    try:

        response = await chat_service.chat(
            request.message
        )

        return ChatResponse(
            response=response,
            model="llama3.2"
        )

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=f"AI service error: {str(exc)}"
        )