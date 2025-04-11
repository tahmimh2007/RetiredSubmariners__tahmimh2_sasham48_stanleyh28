from flask import Flask, render_template, flash, request, redirect, url_for, session
from db_functions import register_user, login_user, create_tables, save_data, add_file_table, add_file, get_files, get_file_id, get_filename
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
        filenames = get_files(username)
        file_ids = [get_file_id(username, file) for file in filenames]
        files = zip(filenames, file_ids)
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
    if 'username' in session:
        username = session['username']
        filenames = get_files(username)
        file_ids = [get_file_id(username, file) for file in filenames]
        files = zip(filenames, file_ids)

        file_id = request.args.get('file_id')
        if file_id==None:
            return render_template("visual.html", username=username, files=files)
        else:
            selected = get_filename(file_id)
            selected=selected['filename']
            return render_template("visual.html", username=username, files=files, selected=selected)
    return render_template("visual.html")

@app.route("/upload", methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        override = request.form.get('override', 'false') == 'true'

        if file:
            allowed, extension = file_type(file.filename)
            if allowed:
                if 'username' in session:
                    username = session['username']
                    user_files = get_files(username)
                    filename = secure_filename(file.filename)

                    if filename in user_files and not override:
                        # Ask for confirmation
                        return render_template("upload.html", duplicate=True, filename=filename)

                    # Read content
                    file_content = file.read()
                    text_content = file_content.decode('utf-8')
                    header, entries = save_data(text_content, extension)
                    if header is None or entries is None:
                        flash("Error parsing file. Check file format.", 'error')
                        return redirect(url_for('upload'))

                    # Save or override
                    add_file(username, filename)
                    add_file_table(username, filename, header, entries)

                    flash("File uploaded successfully.", "success")
                    return redirect(url_for('upload'))
            else:
                flash(f"Unsupported file format '.{extension}'. Only .csv or .json allowed.", 'error')
                return redirect(url_for('upload'))

    if 'username' in session:
        return render_template("upload.html", username=session['username'])
    return render_template("upload.html")

@app.route("/ml")
def ml():
    if 'username' in session:
        return render_template("ml.html", username=session['username'])
    return render_template("ml.html")

if __name__ == "__main__":
    create_tables()  # Initialize database tables before starting the app
    app.run(host='0.0.0.0')
