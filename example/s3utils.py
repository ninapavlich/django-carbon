from django.conf import settings
from storages.backends.s3boto import S3BotoStorage

StaticS3BotoStorage = lambda: S3BotoStorage(
	location=settings.AWS_STATIC_FOLDER,
	bucket=settings.AWS_STORAGE_BUCKET_NAME, 
	custom_domain=settings.AWS_S3_CUSTOM_DOMAIN
)

MediaS3BotoStorage = lambda: S3BotoStorage(
	location=settings.AWS_MEDIA_FOLDER,
	bucket=settings.AWS_STORAGE_BUCKET_NAME_MEDIA, 
	custom_domain=settings.AWS_S3_CUSTOM_DOMAIN_MEDIA
)

SecureMediaS3BotoStorage = lambda: S3BotoStorage(
	location=settings.AWS_MEDIA_FOLDER,
	bucket=settings.AWS_STORAGE_BUCKET_NAME_MEDIA_SECURE, 
	custom_domain=settings.AWS_S3_CUSTOM_DOMAIN_MEDIA_SECURE
)