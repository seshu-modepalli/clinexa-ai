from fastapi import APIRouter, HTTPException

from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_service import ChatService
from fastapi.responses import StreamingResponse


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
@router.post("/stream")
async def stream_chat(request: ChatRequest):

    async def generate():

        async for chunk in chat_service.chat_stream(
            request.message
        ):
            if chunk:
                yield chunk

    return StreamingResponse(
        generate(),
        media_type="text/plain"
    )