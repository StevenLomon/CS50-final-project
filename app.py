from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from werkzeug.utils import secure_filename
from PIL import Image
import os, imghdr
from helpers import apology

# Configure application
app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['DEBUG'] = True
# Set maximum file size (e.g., 5 MB)
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024
Session(app)

# Code by ChatGPT
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
        
        # If we've reached this point of the code, save and process the file securely
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # Redirect user to result page
        return redirect(url_for('result', result_id=result.id))
    
    # User reached route via GET (as by clicking the Upload Image Button in Index)
    else:
        return render_template("image.html")
    
@app.route("/result/<result_id>")
def result(result_id):
    # Fetch result using result_id
    return render_template("result.html", result=result)

@app.route("/camera")
def camera():
    return render_template("camera.html")



if __name__ == '__main__':
    app.run(debug=True)