from google.cloud import storage
from uuid import uuid1
import os
import json

class Gcs:
    def __init__(self, bucket, **kwargs):
        storage_client = storage.Client()
        self.bucket = storage_client.bucket(bucket)

    def list_keys(self, prefix=None):
        return [f.name for f in self.bucket.list_blobs(prefix=prefix)]

    def read(self, path='/'):
        blob = self.bucket.get_blob(path)
        if blob:
            return blob.download_as_string()
        else:
            return None #Make this a warning? Or exception?

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

    def append(self, path, new_list):
        file_type = path.split('.')[-1]

        if file_type == 'jsonl':
            target = self.read(path).split('\n')

        if file_type == 'json':
            target = json.loads(self.read(path))

        if isinstance(target, list):
            target.extend(new_list)
            tmp_path = f'tmp/{uuid1()}'
            output = json.dumps(target) if file_type=='json' else '\n'.join([json.dumps(x) for x in target])
            self.write(tmp_path, output)
            if len(self.list_keys(tmp_path))>0:
                self.rewrite(path, tmp_path)
            self.delete(tmp_path)
