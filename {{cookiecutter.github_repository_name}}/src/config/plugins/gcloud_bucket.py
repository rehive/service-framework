import os


# TOML file storage
if os.environ.get('GCLOUD_MEDIA_BUCKET', False):
    DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
    GS_BUCKET_NAME = os.environ.get('GCLOUD_MEDIA_BUCKET')
    GS_FILE_OVERWRITE = True
    GS_CACHE_CONTROL = None
    GS_DEFAULT_ACL = None
