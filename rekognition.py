import boto3

# Create an S3 object
s3 = boto3.client('s3')

# # Test to upload an image PASSED
# s3.upload_file('rubber-duck.jpeg', 'cs50-final-project-rubber-duck-rekognition-bucket', 'rubber-duck.jpeg')