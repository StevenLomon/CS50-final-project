import boto3
from rich import print

# Create an S3 object
s3 = boto3.client('s3')
bucket_name = 'cs50-final-project-rubber-duck-bucket'

# # Test to upload an image PASSED
# s3.upload_file('rubber-duck-2.jpg', 'cs50-final-project-rubber-duck-bucket', 'rubber-duck-2.jpg')

# rubber_duck_labels = ['Toy', 'Bird', 'Duck'] #Previous version that gave somewhat mixed results
rubber_duck_labels = ['Toy', 'Bird', 'Inflatable']
boundinx_box_labels = rubber_duck_labels + ['Helmet']

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
        MaxLabels = 50,
        MinConfidence = 50
    )

    labels = response['Labels']
    filtered_labels = [label for label in labels if label.get('Confidence') > 52 and label.get('Name') in rubber_duck_labels]
    print(f"Labels: {labels}")
    print(f"Filtered labels: {filtered_labels}")

    # Find the maximum confidence for 'Toy' and 'Inflatable' and get the name of that label. This is written by ChatGPT
    toy_inflatable_confidences = [(label['Name'], label['Confidence']) for label in filtered_labels if label['Name'] in ['Toy', 'Inflatable']]
    max_confidence_label = max(toy_inflatable_confidences, key=lambda x: x[1], default=(None, None))[0]

    # Construct the confidence_values list based on the highest confidence label
    confidence_values = [
        label['Confidence'] for label in filtered_labels
        if label['Name'] not in ['Toy', 'Inflatable']
    ]

    # Add the confidence of either 'Toy' or 'Inflatable' based on which has the highest confidence. We only use one
    if max_confidence_label:
        max_confidence_value = next(
            (label['Confidence'] for label in filtered_labels if label['Name'] == max_confidence_label),
            None
        )
        if max_confidence_value is not None:
            confidence_values.append(max_confidence_value)

    # Look through the labels and extract BoundingBox data if there is any
    bounding_box = [
        instance['BoundingBox']
        for label in labels
        if label.get('Confidence') > 50 and label.get('Instances') and label.get('Name') in boundinx_box_labels #"and label.get('Name') == 'Toy'" was previously used but now the code is much more general
        for instance in label['Instances']
    ]
    print(f"Bounding Box: {bounding_box}")

    # Calculate rubber duck confidence if the list contains at least 2 values
    if confidence_values and len(confidence_values) > 1:
        rubber_duck_conf = sum(confidence_values) / len(confidence_values)

        # Return rubber duck confidence score and bounding box data as a dictionary
        return {'rubber_duck_conf': rubber_duck_conf, 'bounding_box': bounding_box}
        # print(f"Rubber duck detected with {rubber_duck_conf:.2f}% certainty! :)")
    else:
        # print("No rubber duck detected :(")
        return {}