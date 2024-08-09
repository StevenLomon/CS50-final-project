import boto3
from rich import print

# Create an S3 object
s3 = boto3.client('s3')

# # Test to upload an image PASSED
# s3.upload_file('rubber-duck-2.jpg', 'cs50-final-project-rubber-duck-bucket', 'rubber-duck-2.jpg')

# Create an AWS Rekognition object
rekognition = boto3.client('rekognition', region_name='eu-central-1')

# Response object to fetch labels from image
response = rekognition.detect_labels(
    Image = {
        'S3Object': {
            'Bucket': 'cs50-final-project-rubber-duck-bucket',
            'Name': 'rubber-duck-2.jpg'
        },
    },
    MaxLabels = 10,
    MinConfidence = 50
)

labels = response['Labels']
# print(labels)

# Extract confidence values from labels
confidence_values = {label['Name']: label.get('Confidence') for label in labels}

# Get the confidence values for 'Duck' and 'Toy', defaulting to None if not present
duck_conf = confidence_values.get('Duck')
toy_conf = confidence_values.get('Toy')

# Calculate rubber duck confidence if both 'Duck' and 'Toy' are found
if duck_conf is not None and toy_conf is not None:
    rubber_duck_conf = (duck_conf + toy_conf) / 2
    print(f"Rubber duck detected with {rubber_duck_conf:.2f}% certainty! :)")
else:
    print("No rubber duck detected :(")