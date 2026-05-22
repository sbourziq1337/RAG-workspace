from .BaseController import BaseController
from fastapi import UploadFile
from .ProjectController import ProjectController
from models import ResponseSignal
import re
import os

class DataController(BaseController):
    def __init__(self):
        super().__init__()

    def validate_upload_file(self, file: UploadFile):
        # Check file type
        if file.content_type not in self.app_settings.FILE_ALLOW_EXTS:
            return False, ResponseSignal.FILE_TYPE_NOT_SUPPORTED

        # Check file size
        file_size = file.size
        max_size_bytes = self.app_settings.MAX_FILE_SIZE_MB * 1024 * 1024
        if file_size is not None and file_size > max_size_bytes:
            return False, ResponseSignal.FILE_SIZE_EXCEEDED

        return True, ResponseSignal.FILE_UPLOAD_SUCCESS
    
    def generate_unique_filepath(self, orig_filename: str, project_id: str):

        random_key = self.generate_random_string()
        project_path = ProjectController().get_project_path(project_id=project_id)
        clear_filename = self.get_clean_filename(orig_filename=orig_filename)
        new_file_path = os.path.join(project_path, random_key + "_" + clear_filename)
        while os.path.exists(new_file_path):
            random_key = self.generate_random_string()
            new_file_path = os.path.join(project_path, random_key + "_" + clear_filename)

        return new_file_path, random_key + "_" + clear_filename

    def get_clean_filename(self, orig_filename: str):
        clean_filename = re.sub(r'[<>:"/\\|?*]', '', orig_filename)
        clean_filename = clean_filename.replace(' ', '_')

        return clean_filename
