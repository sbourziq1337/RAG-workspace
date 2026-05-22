from fastapi import APIRouter, Depends, UploadFile, status, Request
from fastapi.responses import JSONResponse
from helpers.config import get_settings, Settings
from controllers import DataController, ProjectController, ProcessController
from models import ResponseSignal, ProjectModel
import os
import aiofiles
import logging
from .schemes.data import ProcessRequest

logger = logging.getLogger(__name__)

data_router = APIRouter(prefix="/api/data", tags=["api_v1", "data"])

@data_router.post('/upload/{project_id}')
async def upload_file(
    request: Request,
    project_id: str,
    file: UploadFile,
    app_settings: Settings = Depends(get_settings)
):
    logger.info("Received upload request for file: '%s' in project: '%s'", file.filename, project_id)

    project_model = ProjectModel(db_client=request.app.db_client)

    project = await project_model.get_project_or_create_one(
        project_id=project_id
    )

    data_controller = DataController()
    project_controller = ProjectController()
    is_valid, response_signal = data_controller.validate_upload_file(file=file)

    if not is_valid:
        logger.warning("File validation failed for '%s': %s", file.filename, response_signal.value)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"signal": response_signal.value}
        )

    project_dir_path = project_controller.get_project_path(project_id=project_id)
    file_path, file_id = data_controller.generate_unique_filepath(orig_filename=file.filename, project_id=project_id)

    try:
        logger.info("Writing upload chunk(s) to: '%s'", file_path)
        async with aiofiles.open(file_path, "wb") as f:
            while chunk := await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):
                await f.write(chunk)
    
    except Exception as e:
        logger.error("Failed to write uploaded file '%s' to '%s'. Error: %s", file.filename, file_path, str(e), exc_info=True)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"signal": ResponseSignal.FILE_UPLOAD_FAILED.value,
                     "filename": file_path}
        )

    logger.info("File successfully uploaded and saved to: '%s'", file_path)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"signal": ResponseSignal.FILE_UPLOAD_SUCCESS.value,
                 "file id": file_id,
                 "project id": str(project.id)}
    )


@data_router.post('/process/{project_id}')
async def process_endpoint(project_id: str, process_request: ProcessRequest):
    logger.info("Received request to process file '%s' for project: '%s'", process_request.file_id, project_id)
    
    file_id = process_request.file_id
    chunk_size = process_request.chunk_size
    overlap_size = process_request.overlap_size
    process_controller = ProcessController(project_id=project_id)

    try:
        logger.info("Loading content of file: '%s'", file_id)
        file_content = process_controller.get_file_content(file_id=file_id)
        
        logger.info("Splitting content into chunks (size: %s, overlap: %s)", chunk_size, overlap_size)
        file_chunks = process_controller.process_file_content(
            file_content=file_content,
            file_id=file_id,
            chunk_size=chunk_size,
            overlap_size=overlap_size
        )
    except Exception as e:
        logger.error("Error occurred while processing file '%s' for project '%s'. Error: %s", file_id, project_id, str(e), exc_info=True)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"signal": ResponseSignal.PROCESS_FAILED.value}
        )

    if file_chunks is None or len(file_chunks) == 0:
        logger.warning("Processing produced no chunks for file '%s' under project '%s'", file_id, project_id)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"signal": ResponseSignal.PROCESS_FAILED.value}
        )
    
    logger.info("Successfully split file '%s' into %d chunks", file_id, len(file_chunks))
    return file_chunks



