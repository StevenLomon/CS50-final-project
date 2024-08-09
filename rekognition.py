import boto3

# Create an S3 object
s3 = boto3.client('s3')

# Test to upload an image and make sure Bucket Policies are set and working
s3.upload_file('path_to_local_file', 'bucket_name', 'object_name')