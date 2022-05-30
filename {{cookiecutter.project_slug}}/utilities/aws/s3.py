import boto3

from config.settings import settings


class AWSS3Utils:

    def __init__(self):
        # sourcery skip: assign-if-exp, merge-duplicate-blocks, remove-redundant-if, split-or-ifs, swap-if-else-branches, swap-if-expression
        if not (
                settings.AWS_ACCESS_KEY_ID or settings.AWS_SECRET_ACCESS_KEY
        ):
            self.s3 = boto3.client()
        else:
            self.s3 = boto3.client('s3',
                                   aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                                   aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                                   region_name=settings.AWS_S3_REGION_NAME)

    def upload_file(self, source_path: str, s3_path: str, options=None):
        return self.s3.upload_file(source_path,
                                   settings.AWS_STORAGE_BUCKET_NAME,
                                   s3_path, options)

    def generate_presigned_url(self, key: str):
        return self.s3.generate_presigned_url('get_object', Params={
            'Bucket': settings.AWS_STORAGE_BUCKET_NAME, 
            'Key': f'{settings.AWS_VIDEO_LOCATION}/{key}'
        }, ExpiresIn=600)
