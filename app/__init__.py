from flask import Flask, render_template, flash, request, redirect, url_for, send_from_directory
from db_functions import register_user, login_user
import os
from os.path import join, dirname, abspath

app = Flask(__name__)

###FROM FLASK DOCUMENTATION
#https://flask.palletsprojects.com/en/stable/patterns/fileuploads/
from werkzeug.utils import secure_filename

app.config['UPLOAD_FOLDER'] = '/uploads'


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'csv', 'json'}

@app.route("/")
def home():
    return render_template("home.html")

# handles user login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        login_user()
        if "username" in session:
            return redirect(url_for("home"))
        return redirect(url_for("login"))

# logs out user and redirects to home
@app.route("/logout", methods=["GET", "POST"])
def logout():
    if "username" in session:
        user = session.pop("username")
        flash(f"{user}, you have been logged out.", "success")
    return redirect(url_for("home"))

# handles user registration 
@app.route("/register", methods=["GET", "POST"])
def register():
    if "username" in session:
        return redirect(url_for("home"))
    elif request.method == "POST":
        status = register_user()
        if status == 'success':
            return redirect(url_for("login"))
        else:
            return redirect(url_for("register"))

@app.route("/visual")
def visual():
    return render_template("visual.html")

@app.route("/upload", methods=['GET', 'POST'])
def upload():
    ###DIRECTLY FROM FLASK DOCUMENTATION
    #https://flask.palletsprojects.com/en/stable/patterns/fileuploads/
    if request.method == 'POST':
        if 'file' not in request.files:
            print("upload a file") ###for flash message later
            return redirect(url_for("upload"))
        file = request.files['file']
        if file.filename == '':
            print("upload a file") ###for flash message later
            return redirect(url_for("upload"))
        if file and allowed_file(file.filename):
            print(f"filename {file.filename}")
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('upload')) ##redirect to where we need it
    return render_template("upload.html")

@app.route("/ml")
def ml():
    return render_template("ml.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0')
