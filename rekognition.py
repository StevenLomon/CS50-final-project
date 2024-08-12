import boto3
# from rich import print

# Create an S3 object
s3 = boto3.client('s3')
bucket_name = 'cs50-final-project-rubber-duck-bucket'

# # Test to upload an image PASSED
# s3.upload_file('rubber-duck-2.jpg', 'cs50-final-project-rubber-duck-bucket', 'rubber-duck-2.jpg')

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
        MaxLabels = 6,
        MinConfidence = 60
    )

    labels = response['Labels']
    print(f"Rekognition labels: {labels}")

    # Extract confidence values using dictionary comprehension
    confidence_values = {label['Name']: label.get('Confidence') for label in labels}

    # Look through the labels for any with 95%+ confidence and extract bounding box data
    bounding_box = [
        instance['BoundingBox']
        for label in labels
        if label.get('Confidence') > 95 and label.get('Instances')
        for instance in label['Instances']
    ]

    # Get the confidence values for 'Toy' and 'Bird' (I've observerd that it often has larger confidence score than "Duck"), 
    # defaulting to None if not present
    toy_conf = confidence_values.get('Toy')
    bird_conf = confidence_values.get('Bird')

    # Calculate rubber duck confidence if both 'Duck' and 'Toy' are found
    if toy_conf is not None and bird_conf is not None:
        rubber_duck_conf = (toy_conf + bird_conf) / 2

        # Return rubber duck confidence score and bounding box data as a dictionary
        return {'rubber_duck_conf': rubber_duck_conf, 'bounding_box': bounding_box}
        # print(f"Rubber duck detected with {rubber_duck_conf:.2f}% certainty! :)")
    else:
        # print("No rubber duck detected :(")
        return {}