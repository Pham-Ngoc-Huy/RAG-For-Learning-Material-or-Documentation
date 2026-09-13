from fastapi import APIRouter, HTTPException

from config.config_loader import OmegaConfigLoader
from src.api.schemas.chat import ChatRequest, ChatResponse
from src.api.services import ChatWithRAGAssistance
from src.api.services.config import SelectionModel

router = APIRouter(
    prefix="/api/chat",
    tags=["Chat"],
)

_config = OmegaConfigLoader(config_path="config/config.yml").load()

chat = ChatWithRAGAssistance(config=_config)


@router.post("/query", response_model=ChatResponse)
async def chat_query(requests: ChatRequest):
    model = await SelectionModel(model_selection=requests.model).load_model()
    if model is None:
        raise HTTPException(
            status_code=400,
            detail=f"Model '{requests.model}' is not available.",
        )

    try:
        result = await chat.chat(
            user_id=requests.user_id,
            user_name=requests.user_name,
            collection_name=requests.collection_name,
            question=requests.question,
            model=model,
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Chat failed: {str(e)}",
        )

    return ChatResponse(
        user_id=requests.user_id,
        user_name=requests.user_name,
        collection_name=requests.collection_name,
        question=requests.question,
        answer=result["answer"],
    )
