import boto3
from rich import print

# Create an S3 object
s3 = boto3.client('s3')
bucket_name = 'cs50-final-project-rubber-duck-bucket'

# # Test to upload an image PASSED
# s3.upload_file('rubber-duck-2.jpg', 'cs50-final-project-rubber-duck-bucket', 'rubber-duck-2.jpg')

# rubber_duck_labels = ['Toy', 'Bird', 'Duck'] Previous version that gave somewhat mixed results
rubber_duck_labels = ['Toy', 'Bird']

def get_rekognition_data(filename):
    # Create an AWS Rekognition object
    rekognition = boto3.client('rekognition', region_name='eu-central-1')

    # Response object to fetch labels from image
    response = rekognition.detect_labels(
        Image = {
            'S3Object': {
                'Bucket': bucket_name,
                'Name': filename
            },
        },
        MaxLabels = 15,
        MinConfidence = 60
    )

    labels = response['Labels']
    filtered_labels = [label for label in labels if label.get('Name') in rubber_duck_labels]
    print(f"Filtered labels: {filtered_labels}")

    # Get the confidence values from relevant labels using list comprehension
    confidence_values = [label.get('Confidence') for label in filtered_labels]
    print(f"Confidence values: {confidence_values}")

    # Look through the labels for the one with name 'Toy' and extract bounding box data if there is 90%+ confidence 
    bounding_box = [
        instance['BoundingBox']
        for label in filtered_labels
        if label.get('Name') == 'Toy' and label.get('Confidence') > 80 and label.get('Instances')
        for instance in label['Instances']
    ]
    print(f"Bounding Box: {bounding_box}")

    # Calculate rubber duck confidence if both 'Duck' and 'Toy' are found
    if confidence_values:
        rubber_duck_conf = sum(confidence_values) / len(confidence_values)

        # Return rubber duck confidence score and bounding box data as a dictionary
        return {'rubber_duck_conf': rubber_duck_conf, 'bounding_box': bounding_box}
        # print(f"Rubber duck detected with {rubber_duck_conf:.2f}% certainty! :)")
    else:
        # print("No rubber duck detected :(")
        return {}