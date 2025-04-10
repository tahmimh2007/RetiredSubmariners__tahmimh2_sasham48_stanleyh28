from flask import Flask, render_template, flash, request, redirect, url_for, session
from db_functions import register_user, login_user, create_tables, save_data, add_file_table, add_file, get_files, get_file_id
import os
from os.path import join, dirname, abspath
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(32)

def file_type(filename):
    extension = filename.rsplit('.', 1)[1].lower()
    if '.' in filename and extension in {'csv', 'json'}:
        return True, extension
    else:
        return False, extension

@app.route("/")
def home():
    if "username" in session:
        username = session['username']
        user_files = get_files(username)
        file_ids = [get_file_id(username, file) for file in user_files]
        files = zip(user_files, file_ids)
        return render_template("home.html", username=username, files=files)
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
        file = request.files['file']
        if file:
            allowed, extension = file_type(file.filename)
            if allowed:
                if 'username' in session:
                    user_files = get_files(session['username'])
                    if file.filename in user_files:
                        flash("You have already uploaded a file with the same name before. Would you like to override your old file?", 'warning')
                        return render_template("upload.html")
                # Reading the entire content of the file as bytes
                file_content = file.read()
                
                # If you need it as a string (for a text file), you can decode it:
                text_content = file_content.decode('utf-8')
                header, entries = save_data(text_content, extension)
                if header==None or entries==None:
                    return redirect(url_for('upload'))
                if 'username' in session:
                    add_file(session['username'], file.filename)
                    add_file_table(session['username'], file.filename, header, entries)
                flash("File uploaded successfully.", "success")
                return redirect(url_for('upload'))
            else:
                flash(f"You uploaded a .{extension} file which is currently not supported! Try again with a .json or .csv file!", 'error')
                return redirect(url_for('upload'))
    return render_template("upload.html")

@app.route("/ml")
def ml():
    return render_template("ml.html")

if __name__ == "__main__":
    create_tables()  # Initialize database tables before starting the app
    app.run(host='0.0.0.0')
