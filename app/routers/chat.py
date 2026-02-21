from fastapi import APIRouter
from app.schemas.chat import ChatRequest
from app.services.llm_router import call_with_rotation_stream
from app.services.llm_router import call_with_rotation
from app.core.providers import PROVIDERS
from fastapi.responses import StreamingResponse

router = APIRouter()


@router.post("/chat")
async def chat(payload: ChatRequest):
    providers_list = list(PROVIDERS.keys())
    return await call_with_rotation(payload.model_dump(), providers_list)


@router.post("/chat/stream")
async def chat_stream(payload: ChatRequest):
    return StreamingResponse(
        call_with_rotation_stream(payload.model_dump(), providers_list=PROVIDERS.keys()),
        media_type="text/event-stream"
    )
@router.get("/usage")
def usage():
    return PROVIDERS

