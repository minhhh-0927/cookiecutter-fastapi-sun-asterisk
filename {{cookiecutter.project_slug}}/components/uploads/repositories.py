from components.core.repositories import BaseRepositories
from components.uploads.models import LocalUpload


class UploadRepositories(BaseRepositories):

    async def create_local_file(self, filename: str,
                                filesize: float,
                                filepath: str):
        file_upload = LocalUpload(filename=filename,
                                  filesize=filesize,
                                  filepath=filepath)
        self.db.add(file_upload)
        self.db.commit()
        self.db.refresh(file_upload)
        return file_upload
