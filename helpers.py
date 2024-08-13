import csv
import datetime
import pytz
import requests
import urllib
import uuid

from flask import redirect, render_template, request, session
from functools import wraps

# For drawing bounding boxes
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
import matplotlib.patches as patches 

# Taken straight from the Finance problem. Super useful and I wholeheartedly appreciate it!
def apology(message, code=400):
    """Render message as an apology to user."""

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''"),
        ]:
            s = s.replace(old, new)
        return s

    return render_template("apology.html", top=code, bottom=escape(message)), code

# Very similar to USD in the Finance problem
def conf(value):
    """Formats confidence score value to two decimals."""
    return f"{value:,.2f}%"

# Function to help draw bounding boxes using matplotlib. From ChatGPT
def draw_bounding_boxes(image_path, bounding_boxes, output_file):
    # Open the image file from the file path
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)
    
    # Debug: Print image dimensions
    print(f"Image dimensions: {image.width}x{image.height}")
    
    # Draw bounding boxes
    for i, box in enumerate(bounding_boxes):
        left = box['Left'] * image.width
        top = box['Top'] * image.height
        width = box['Width'] * image.width
        height = box['Height'] * image.height
        
        # Debug: Print bounding box dimensions
        print(f"Bounding Box {i}: left={left}, top={top}, width={width}, height={height}")
        
        # Draw rectangle on the image
        draw.rectangle([left, top, left + width, top + height], outline='red', width=10)
    
    # Save the image with bounding boxes
    try:
        image.save(output_file)
        print(f"Image with bounding boxes saved as: {output_file}")
    except Exception as e:
        print(f"Error saving image: {e}")