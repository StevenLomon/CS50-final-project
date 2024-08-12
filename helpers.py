import csv
import datetime
import pytz
import requests
import urllib
import uuid

from flask import redirect, render_template, request, session
from functools import wraps

# For drawing bounding boxes
from PIL import Image
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
def draw_bounding_boxes(image_path, bounding_boxes, output_path):
    # Load image
    image = Image.open(image_path)
    image = image.convert('RGB')

    # Image dimensions
    image_width, image_height = image.size

    # Create a matplotlib figure and axis
    fig, ax = plt.subplots(1)

    # Display the image
    ax.imshow(image)

    # Draw bounding boxes
    for label, boxes in bounding_boxes.items():
        for box in boxes:
            # Calculate bounding box coordinates in pixels
            left = box['Left'] * image_width
            top = box['Top'] * image_height
            width = box['Width'] * image_width
            height = box['Height'] * image_height

            # Create a rectangle patch
            rect = patches.Rectangle(
                (left, top), width, height,
                linewidth=2, edgecolor='red', facecolor='none'
            )

            # Add the rectangle patch to the axis
            ax.add_patch(rect)

    # Save the plot as an image file
    plt.axis('off')  # Hide the axis
    plt.savefig(output_path, bbox_inches='tight', pad_inches=0)
    plt.close()