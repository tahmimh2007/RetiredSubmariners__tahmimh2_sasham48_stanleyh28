from flask import Flask, render_template, flash, request, redirect, url_for, session
from db_functions import register_user, login_user, create_tables
import os
from os.path import join, dirname, abspath
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(32)

# Set the upload folder relative to the app root
app.config['UPLOAD_FOLDER'] = "uploads"

###FROM FLASK DOCUMENTATION
#https://flask.palletsprojects.com/en/stable/patterns/fileuploads/
# Ensure the upload directory exists
upload_folder_path = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
os.makedirs(upload_folder_path, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'csv', 'json'}

@app.route("/")
def home():
    if "username" in session:
        return render_template("home.html", username=session['username'])
    return render_template("home.html")

# Handles user login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        login_user()
        if "username" in session:
            return redirect(url_for("home"))
        return redirect(url_for("login"))
    return render_template("login.html")

# Logs out user and redirects to home
@app.route("/logout", methods=["GET", "POST"])
def logout():
    if "username" in session:
        user = session.pop("username")
        flash(f"{user}, you have been logged out.", "success")
    return redirect(url_for("home"))

# Handles user registration
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        result = register_user()
        print(result)
        if result == "success":
            flash("Registration successful! Please log in.", "success")
            return redirect(url_for("login"))
        else:
            flash("Registration failed. Username may already exist.", "error")
            return redirect(url_for("register"))
    return render_template("register.html")

@app.route("/visual")
def visual():
    return render_template("visual.html")

@app.route("/upload", methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash("Please upload a file.", "error")
            return redirect(url_for("upload"))
        file = request.files['file']
        if file.filename == '':
            flash("No file selected.", "error")
            return redirect(url_for("upload"))
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            save_path = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], filename)
            file.save(save_path)
            flash("File uploaded successfully.", "success")
            return redirect(url_for('upload'))
    return render_template("upload.html")

@app.route("/ml")
def ml():
    return render_template("ml.html")

if __name__ == "__main__":
    create_tables()  # Initialize database tables before starting the app
    app.run(host='0.0.0.0')
