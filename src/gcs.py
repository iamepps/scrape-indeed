from google.cloud import storage

class Gcs:
    def __init__(self, bucket, **kwargs):
        storage_client = storage.Client()
        self.bucket = storage_client.bucket(bucket)

    def list_keys(self, prefix=None):
        return [f.name for f in self.bucket.list_blobs(prefix=prefix)]

    def read(self, path='/'):
        return self.bucket.get_blob(path).download_as_string()

    def write(self, path, file_body):
        blob = self.bucket.blob(path)
        blob.upload_from_string(file_body)

    def rewrite(self, target_path, source_path):
        target_blob = self.bucket.blob(target_path)
        source_blob = self.bucket.blob(source_path)
        target_blob.rewrite(source_blob)

    def delete(self, path):
        blob = self.bucket.blob(path)
        blob.delete()

    def compose(self, prefix, outfile_path):
        blobs = self.bucket.list_blobs(prefix=prefix)
        self.bucket.blob(outfile_path).compose(blobs)
