import boto3
from rich import print

# Create an S3 object
s3 = boto3.client('s3')
bucket_name = 'cs50-final-project-rubber-duck-bucket'

# # Test to upload an image PASSED
# s3.upload_file('rubber-duck-2.jpg', 'cs50-final-project-rubber-duck-bucket', 'rubber-duck-2.jpg')

# rubber_duck_labels = ['Toy', 'Bird', 'Duck'] #Previous version that gave somewhat mixed results
rubber_duck_labels = ['Toy', 'Bird', 'Duck', 'Inflatable']
boundinx_box_labels = rubber_duck_labels + ['Helmet']

def get_rekognition_data(filename, rek_object, bucket_name):
    # Response object to fetch labels from image
    try:
        # Response object to fetch labels from image
        response = rek_object.detect_labels(
            Image={
                'S3Object': {
                    'Bucket': bucket_name,
                    'Name': filename
                },
            },
            MaxLabels=320,
            MinConfidence=35
        )
        print("Response:", response)
    except Exception as e:
        print("Error:", e)

    labels = response['Labels']
    filtered_labels = [label for label in labels if label.get('Confidence') > 10 and label.get('Name') in rubber_duck_labels]
    print(f"Labels: {labels}")
    print(f"Filtered labels: {filtered_labels}")

    # Extract toy_inflatable_confidences
    toy_inflatable_confidences = [
        (label['Name'], label['Confidence']) 
        for label in filtered_labels 
        if label['Name'] in ['Toy', 'Inflatable']
    ]

    # Extract duck_bird_confidences
    duck_bird_confidences = [
        (label['Name'], label['Confidence']) 
        for label in filtered_labels 
        if label['Name'] in ['Duck', 'Bird']
    ]

    # Find the label with maximum confidence for 'Toy' and 'Inflatable'
    max_toy_inflatable_label = max(
        toy_inflatable_confidences, 
        key=lambda x: x[1], 
        default=(None, 0)
    )[0]

    # Find the label with maximum confidence for 'Duck' and 'Bird'
    max_duck_bird_label = max(
        duck_bird_confidences, 
        key=lambda x: x[1], 
        default=(None, 0)
    )[0]

    # Construct the confidence_values list
    confidence_values = [
        label['Confidence'] 
        for label in filtered_labels 
        if label['Name'] not in ['Toy', 'Inflatable', 'Duck', 'Bird']
    ]

    # Add the highest confidence values for 'Toy/Inflatable' and 'Duck/Bird'
    if max_toy_inflatable_label:
        max_toy_inflatable_value = next(
            (label['Confidence'] for label in filtered_labels if label['Name'] == max_toy_inflatable_label),
            None
        )
        if max_toy_inflatable_value is not None:
            confidence_values.append(max_toy_inflatable_value)

    if max_duck_bird_label:
        max_duck_bird_value = next(
            (label['Confidence'] for label in filtered_labels if label['Name'] == max_duck_bird_label),
            None
        )
        if max_duck_bird_value is not None:
            confidence_values.append(max_duck_bird_value)

    # Check if 'Rubber Duck' should be considered based on the combination criteria
    rubber_duck_label = None
    if max_toy_inflatable_label and max_duck_bird_label:
        rubber_duck_label = f"{max_duck_bird_label} + {max_toy_inflatable_label}"

    print(f"Confidence values: {confidence_values}")
    print(f"Rubber Duck Label: {rubber_duck_label}")

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
        print(f"Rubber Duck Confidence Level: {rubber_duck_conf}")

        # Return rubber duck confidence score and bounding box data as a dictionary
        return {'rubber_duck_conf': rubber_duck_conf, 'bounding_box': bounding_box}
        # print(f"Rubber duck detected with {rubber_duck_conf:.2f}% certainty! :)")
    else:
        # print("No rubber duck detected :(")
        return {}