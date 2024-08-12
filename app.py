import os, sqlite3
from datetime import datetime
from flask import Flask, g, flash, redirect, render_template, request, session, url_for
from flask_session import Session

# For image validation
from werkzeug.utils import secure_filename
from PIL import Image
import imghdr 

import uuid # For unique identifiers keeping result pages unique
import boto3 # For S3 integration
# import threading # For database thread safety
from helpers import apology, conf
from rekognition import get_rubber_duck_confidence_score

# Configure application
app = Flask(__name__)

# Custom confidence decimal filter
app.jinja_env.filters["conf"] = conf

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['DEBUG'] = True
app.config['DATABASE'] = 'rubber_duck.db'
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024 # Set maximum file size (e.g., 5 MB)

Session(app)

# Set up SQLite database

# Thread-local storage for the database connection
def get_db():
    if not hasattr(g, '_database'):
        g._database = sqlite3.connect(app.config['DATABASE'])
    return g._database

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


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
            return apology("Invalid file type. Please use jpg, jpeg or png", 400)
        
        # Validate MIME type
        mime_type = file.content_type
        if mime_type not in ['image/jpg','image/jpeg', 'image/png']:
            return apology("Invalid file type. Please use jpg, jpeg or png", 400)
        
        # Validate file content using imghdr
        if imghdr.what(file) not in ALLOWED_EXTENSIONS:
            return apology("Invalid image content. Please try another image", 400)
        
        # Validating file size server-side
        if len(file.read()) > app.config['MAX_CONTENT_LENGTH']:
            return apology("File too large: Please upload a picture no more than 5MB", 400)
        
        # Image content validation using PIL
        try:
            img = Image.open(file.stream)
            img.verify()  # Validate the image
        except (IOError, SyntaxError) as e:
            return apology("Invalid image file. Please try another image", 400)
        
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
        
        # Boolean to store whether a duck is found in the picture or not. Defaults to 0
        duck_found = 0

        # Get rubber duck confidence score via interaction with Rekognition
        rubber_duck_conf = get_rubber_duck_confidence_score(filename)
        print(f"Rubber duck confidence score: {rubber_duck_conf}")
        if rubber_duck_conf is not None:
            duck_found = 1
        
        # Generate unique result ID
        result_id = str(uuid.uuid4())

        # Store results in our database
        db = get_db()
        cur = db.cursor()

        s3_url = f"https://{bucket_name}.s3.eu-central-1.amazonaws.com/{filename}"
        cur.execute("INSERT INTO duck_results (id, duck_found, confidence_score, s3_key, s3_url) VALUES (?, ?, ?, ?, ?)", (result_id, duck_found, rubber_duck_conf, filename, s3_url))
        db.commit()

        # Redirect user to result page
        return redirect(url_for('result', result_id=result_id))
    
    # User reached route via GET (as by clicking the Upload Image Button in Index)
    else:
        return render_template("image.html")
    
@app.route("/result/<result_id>")
def result(result_id):    
    # Fetch result data from datbase using result_id
    db = get_db()
    cur = db.cursor()

    cur.execute("SELECT * FROM duck_results WHERE id=?", (result_id,))
    query_data = cur.fetchone()

    if not query_data:
        return apology("Result not found", 404)

    result_data = {'duck_found': query_data[1], 'conf_score': query_data[2], 's3_url': query_data[4]}

    return render_template("result.html", result=result_data)

@app.route("/camera")
def camera():
    return render_template("camera.html")



if __name__ == '__main__':
    app.run(debug=True)