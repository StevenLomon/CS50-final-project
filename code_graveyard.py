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