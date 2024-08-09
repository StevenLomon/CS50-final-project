from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session

# Configure application
app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['DEBUG'] = True
Session(app)

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
        print("Handling POST request")
        # Ensure valid image was uploaded

        # Redirect user to result page
        return redirect(url_for('result', result_id=result.id))
    
    # User reached route via GET (as by clicking the Upload Image Button in Index)
    else:
        print("Handling GET request")
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