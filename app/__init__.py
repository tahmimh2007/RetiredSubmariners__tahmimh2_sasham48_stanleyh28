from flask import Flask, render_template, flash, request, redirect, url_for, send_from_directory
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

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/register")
def register():
    return render_template("register.html")

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
