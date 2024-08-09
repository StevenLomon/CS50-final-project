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
    MinConfidence = 10
)

labels = response['Labels']
# print(labels)

# Initialize all confidence values as None
duck_conf = toy_conf = rubber_duck_conf = None

# Get duck confidence and toy confidence
duck_dict = [dict for dict in labels if dict.get('Name') == 'Duck']
if duck_dict:
    duck_conf = duck_dict[0].get('Confidence')

toy_dict = [dict for dict in labels if dict.get('Name') == 'Toy']
if toy_dict:
    toy_conf = toy_dict[0].get('Confidence')

# Calculate rubber duck confidence
if duck_conf and toy_conf:
    rubber_duck_conf = (duck_conf + toy_conf) / 2

if rubber_duck_conf:
    print(f"Rubber duck detected with {rubber_duck_conf}% certainty! :)")
else:
    print("No rubber duck detected :(")

# duck_conf = duck_dict.get('Confidence')
# print(duck_dict)

# duck_dict = [label for label in labels if label['Name'.lower() == "duck"]]
# duck_conf = duck_dict.get('Confidence')

# toy_dict = [label for label in labels if label['Name'].lower() == "Toy"]
# toy_conf = toy_dict.get('Confidence')

# print(duck_conf)
# print(toy_conf)

# Filter labels to only include those who include the word "duck"
# rubber_labels = [label for label in labels if "duck" in label['Name'].lower()]


# print(labels)