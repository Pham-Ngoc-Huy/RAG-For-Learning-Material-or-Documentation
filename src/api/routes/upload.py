from datetime import datetime

from fastapi import APIRouter, HTTPException

from config.config_loader import OmegaConfigLoader
from src.api.schemas.upload import UploadFileResponse, UploadFileSchema
from src.api.services import UploadServiceImpl
from src.api.services.config import SelectionModel

router = APIRouter(
    prefix="/api/uploader",
    tags=["Uploader"],
)

_config = OmegaConfigLoader(config_path="config/config.yml").load()

upload = UploadServiceImpl(config=_config)


@router.post("/upload", response_model=UploadFileResponse)
async def upload_file(requests: UploadFileSchema):
    model = await SelectionModel(model_selection=requests.model).load_model()
    if model is None:
        raise HTTPException(
            status_code=400,
            detail=f"Model '{requests.model}' is not available.",
        )

    try:
        result = await upload.upload_file(
            user_id=requests.user_id,
            user_name=requests.user_name,
            collection_name=requests.collection_name,
            file_path=requests.file_path,
            model=model,
        )
    except (FileNotFoundError, ValueError) as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Upload failed: {str(e)}",
        )

    return UploadFileResponse(
        user_id=requests.user_id,
        user_name=requests.user_name,
        collection_name=requests.collection_name,
        file_path=requests.file_path,
        model=model,
        total_chunks=result["total_chunks"],
        upload_date=datetime.now(),
    )
