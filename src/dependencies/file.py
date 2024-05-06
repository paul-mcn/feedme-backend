import uuid
from .aws import s3_client
from ..dependencies.env import get_environment_settings

settings = get_environment_settings()


def upload_new_image():
    key = uuid.uuid4().hex
    try:
        response = s3_client.generate_presigned_post(
            settings.AWS_BUCKET_NAME,
            key,
            ExpiresIn=3600,
            # Conditions=[{"ContentType": "image/webp"}],
        )
        return response
    except Exception as e:
        print("Couldn't upload image to S3. Here's why: %s: %s" % (type(e).__name__, e))
