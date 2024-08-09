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