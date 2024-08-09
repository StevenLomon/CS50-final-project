import boto3
from rich import print

# Create an S3 object
s3 = boto3.client('s3')

# # Test to upload an image PASSED
# s3.upload_file('rubber-duck.jpeg', 'cs50-final-project-rubber-duck-bucket', 'rubber-duck.jpeg')

# Create an AWS Rekognition object
rekognition = boto3.client('rekognition', region_name='eu-central-1')

response = rekognition.detect_labels(
    Image = {
        'S3Object': {
            'Bucket': 'cs50-final-project-rubber-duck-bucket',
            'Name': 'rubber-duck.jpeg'
        },
    },
    MaxLabels = 10,
    MinConfidence = 80
)

labels = response['Labels']
print(labels)