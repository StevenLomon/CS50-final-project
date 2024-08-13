# # Initialize all confidence values as None
# duck_conf = toy_conf = rubber_duck_conf = None

# # Get duck confidence and toy confidence
# duck_dict = [dict for dict in labels if dict.get('Name') == 'Duck']
# if duck_dict:
#     duck_conf = duck_dict[0].get('Confidence')

# toy_dict = [dict for dict in labels if dict.get('Name') == 'Toy']
# if toy_dict:
#     toy_conf = toy_dict[0].get('Confidence')

# # Calculate rubber duck confidence
# if duck_conf and toy_conf:
#     rubber_duck_conf = (duck_conf + toy_conf) / 2

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

# print("Files to be inserted\n")
# print(f":{result_id}, Type: {type(result_id)}")
# print(f":{rubber_duck_conf}, Type: {type(rubber_duck_conf)}")
# print(f":{filename}, Type: {type(filename)}")
# print(f":{s3_url}, Type: {type(s3_url)}")

# # Get the confidence values from relevant labels
# confidence_values = [label.get('Confidence') for label in filtered_labels]
# print(f"Confidence values: {confidence_values}")

# # Find the maximum confidence for 'Toy' and 'Inflatable' and get the name of that label. Do the same thing with and same with 'Duck' and 'Bird'. This is written by ChatGPT
# toy_inflatable_confidences = [(label['Name'], label['Confidence']) for label in filtered_labels if label['Name'] in ['Toy', 'Inflatable']]
# max_confidence_label = max(toy_inflatable_confidences, key=lambda x: x[1], default=(None, None))[0]

# # Construct the confidence_values list based on the highest confidence label
# confidence_values = [
#     label['Confidence'] for label in filtered_labels
#     if label['Name'] not in ['Toy', 'Inflatable']
# ]

# # Add the confidence of either 'Toy' or 'Inflatable' based on which has the highest confidence. We only use one
# if max_confidence_label:
#     max_confidence_value = next(
#         (label['Confidence'] for label in filtered_labels if label['Name'] == max_confidence_label),
#         None
#     )
#     if max_confidence_value is not None:
#         confidence_values.append(max_confidence_value)