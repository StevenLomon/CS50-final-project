import os, sqlite3, json
from datetime import datetime
from flask import Flask, g, flash, redirect, render_template, request, session, url_for
from flask_session import Session

# For image validation
from werkzeug.utils import secure_filename
from PIL import Image # Will also be used for bounding box operations
import imghdr 

import uuid # For unique identifiers keeping result pages unique
import boto3 # For S3 integration

from helpers import apology, conf, draw_bounding_boxes
from rekognition import get_rekognition_data

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
        
        # Default values
        duck_found = bounding_box_available = 0
        rubber_duck_conf = bounding_box = bounding_box_data_json = s3_url_bb = None

        # Get rubber duck confidence score via interaction with Rekognition
        rek_data = get_rekognition_data(filename)
        if not isinstance(rek_data, dict):
            return apology("Unexpected exception when getting data from Rekognition. Please try again", 400)
        
        if rek_data: # If it's not an empty dictionary
            rubber_duck_conf = rek_data.get('rubber_duck_conf')
            bounding_box = rek_data.get('bounding_box')

        print(f"Rubber duck confidence score: {rubber_duck_conf}")
        print(f"Bounding box: {bounding_box}")
        if rubber_duck_conf is not None:
            duck_found = 1
        if bounding_box is not None:
            bounding_box_available = 1
        s3_url = f"https://{bucket_name}.s3.eu-central-1.amazonaws.com/{filename}"

        # If bounding box data is available, convert  bounding_box to JSON string if it's not a primitive 
        # type and create an S3 url. Then draw the bounding boxes
        if bounding_box_available:
            bounding_box_data_json = json.dumps(bounding_box)
            s3_url_bb = f"https://{bucket_name}.s3.eu-central-1.amazonaws.com/{filename}-bb"
            filename_bb = f"{filename}-bb"

            # Save the uploaded file locally
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            draw_bounding_boxes(file_path, bounding_box, filename_bb)
            

            # Upload the image with bounding boxes to S3
            with open(file_path, 'rb') as data:
                try:
                    s3.upload_fileobj(data, bucket_name, filename_bb)
                except Exception as e:
                    return redirect(request.url)
            
            # Clean up local files
            os.remove(file_path)
            os.remove(filename_bb)
        
        # Generate unique result ID
        result_id = str(uuid.uuid4())

        # Store results in our database
        db = get_db()
        cur = db.cursor()

        cur.execute("INSERT INTO duck_results (id, duck_found, bounding_box_available, confidence_score, bounding_box_data, s3_key, s3_url, s3_url_bounding_box) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (result_id, duck_found, bounding_box_available, rubber_duck_conf, bounding_box_data_json, filename, s3_url, s3_url_bb))
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

    result_data = {'duck_found': query_data[1], 'bounding_box_available': query_data[2], 
                   'conf_score': query_data[3], 's3_url': query_data[6], 's3_url_bb': query_data[7]}

    return render_template("result.html", result=result_data)

@app.route("/camera")
def camera():
    return render_template("camera.html")



if __name__ == '__main__':
    app.run(debug=True)