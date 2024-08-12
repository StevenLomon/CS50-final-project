import os, sqlite3
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session

# For image validation
from werkzeug.utils import secure_filename
from PIL import Image
import imghdr 

import uuid # For unique identifiers keeping result pages unique
import boto3 # For S3 integration
from helpers import apology
from rekognition import get_rubber_duck_confidence_score

# Configure application
app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['DEBUG'] = True

# App config code by ChatGPT
# Set maximum file size (e.g., 5 MB)
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024

Session(app)

# Set up database
conn = sqlite3.connect("rubber_duck.db")
cur = conn.cursor()

results_table_query = """
            CREATE TABLE IF NOT EXISTS
            duck_results (id INTEGER PRIMARY KEY, time TEXT, confidence_score FLOAT, s3_path TEXT)
            """

cur.execute(results_table_query)
conn.commit()

# Create an S3 object for file programmatic image upload to the bucket
s3 = boto3.client('s3')
bucket_name = 'cs50-final-project-rubber-duck-bucket'

# Code by ChatGPT for file validation
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/image", methods=['GET', 'POST'])
def image():
    if request.method == "POST":
        file = request.files['image']

        # Ensure valid image was uploaded. All validation code by ChatGPT

        # If the user does not select a file, the browser may submit an empty file without a filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        # Validate file extension
        if not file or not allowed_file(file.filename):
            return apology("Invalid file type", 400)
        
        # Validate MIME type
        mime_type = file.content_type
        if mime_type not in ['image/jpg','image/jpeg', 'image/png']:
            return apology("Invalid file type", 400)
        
        # Validate file content using imghdr
        if imghdr.what(file) not in ALLOWED_EXTENSIONS:
            return apology("Invalid image content", 400)
        
        # Validating file size server-side
        if len(file.read()) > app.config['MAX_CONTENT_LENGTH']:
            return apology("File too large", 400)
        
        # Image content validation using PIL
        try:
            img = Image.open(file.stream)
            img.verify()  # Validate the image
        except (IOError, SyntaxError) as e:
            return apology("Invalid image file", 400)
        
        # Ensure the file pointer is at the beginning of the file before upload
        file.seek(0)

        # If we've reached this point of the code, save and process the file securely
        filename = secure_filename(file.filename)
        # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # Upload the image to our S3 bucket
        try:
            s3.upload_fileobj(file, bucket_name, filename)
            flash('File uploaded successfully!')
        except Exception as e:
            flash(f'An error occurred: {str(e)}')
            return redirect(request.url)
        
        # Get rubber duck confidence score via interaction with Rekognition
        rubber_duck_conf = get_rubber_duck_confidence_score(filename)
        if not rubber_duck_conf:
            return apology("Could not fetch rubber duck confidence. Please try again later", 400)

        # Store results (in database?)

        # Generate unique result ID
        result_id = str(uuid.uuid4())

        # Redirect user to result page
        return redirect(url_for('result', result_id=result_id))
    
    # User reached route via GET (as by clicking the Upload Image Button in Index)
    else:
        return render_template("image.html")
    
@app.route("/result/<result_id>")
def result(result_id):
    def fetch_result():
        return True
    
    # Fetch result using result_id
    result_data = fetch_result(result_id)  # Implement this function

    if not result_data:
        return apology("Result not found", 404)

    return render_template("result.html", result=result)

@app.route("/camera")
def camera():
    return render_template("camera.html")



if __name__ == '__main__':
    app.run(debug=True)