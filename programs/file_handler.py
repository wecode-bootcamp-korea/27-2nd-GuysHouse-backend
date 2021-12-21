import uuid

class FileHanlder:
    def __init__(self, client, Bucket, region):
        self.client     = client
        self.aws_bucket = Bucket
        self.aws_region = region
    
    def upload_file(self, file):
        unique_key = str(uuid.uuid4())
        self.client.put_object(
            Bucket      = self.aws_bucket,
            Key         = unique_key,
            Body        = file.file.read(),
            ContentType = file.content_type
        )
        return '%s.s3.%s.amazonaws.com/%s' % (self.aws_bucket, self.aws_region, unique_key)

    def upload_files(self, files):
        return [self.upload_file(file) for file in files]
