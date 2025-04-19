from flask import Flask, render_template, flash, request, redirect, url_for, session
from db_functions import register_user, login_user, create_tables, save_data, add_file_table, add_file, get_files, get_file_id, get_filename, update_file, get_headers, get_x, get_y, get_headers_float, get_headers_nonfloat
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
    
@app.route("/check_duplicate", methods=["POST"])
def check_duplicate():
    if "username" not in session:
        return {"error": "not logged in"}, 401

    data = request.get_json()
    filename = secure_filename(data.get("filename"))
    user_files = get_files(session["username"])
    return {"duplicate": filename in user_files}

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
            chartType = request.args.get('chartType')
            if chartType==None:
                selected = get_filename(file_id)
                selected=selected['filename']
                headers= get_headers(file_id)
                headers2 = get_headers_float(file_id)
                return render_template("visual.html", username=username, files=files, selected=selected, headers=headers, headers2=headers2)
            else:
                filename = get_filename(file_id)
                filename=filename['filename']
                xField = request.args.get('xField')
                fields = request.args.getlist('fields')
                graph = chartType
                x = get_x(file_id, xField)
                y_lists = get_y(file_id, fields)
                labels = [xField] + fields

                return render_template("visual.html", graph = graph, x=x, y_lists=y_lists, labels=labels)
        
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
                    # Read content
                    file_content = file.read()
                    text_content = file_content.decode('utf-8')
                    header, entries = save_data(text_content, extension)
                    # Bad data
                    if header is None or entries is None:
                        flash("""Error parsing file. Check file format. Be sure to label your actual data as 'data' if json file is in format '{'headers': {...}, 'data': {...}}'""", 'error')
                        return redirect(url_for('upload'))
                    # Override old file
                    elif filename in user_files and override:
                        update_file(username, filename, header, entries)
                        flash("File updated successfully.", "success")
                        return redirect(url_for('upload'))
                    elif filename in user_files and not override:
                        flash("Override cancelled, please upload another file.", "error")
                        return redirect(url_for('upload'))
                    # Save file
                    else:
                        add_file(username, filename)
                        add_file_table(username, filename, header, entries)

                        flash("File uploaded successfully.", "success")
                        return redirect(url_for('upload'))
            else:
                flash(f"Unsupported file format '.{extension}'. Only .csv or .json allowed.", 'error')
                return redirect(url_for('upload'))

    if 'username' in session:
        return render_template("upload.html", username=session['username'], duplicate=False)
    return render_template("upload.html")

@app.route("/ml")
def ml():
    if 'username' in session:
        username = session['username']
        filenames = get_files(username)
        file_ids = [get_file_id(username, file) for file in filenames]
        files = zip(filenames, file_ids)

        file_id = request.args.get('file_id')
        if file_id==None:
            return render_template("ml.html", username=username, files=files)
        else:
            chartType = request.args.get('chartType')
            if chartType==None:
                selected = get_filename(file_id)
                selected=selected['filename']
                headers= get_headers_nonfloat(file_id)
                headers2 = get_headers_float(file_id)
                return render_template("ml.html", username=username, files=files, selected=selected, headers=headers, headers2=headers2)
            else:
                filename = get_filename(file_id)
                filename=filename['filename']
                xField = request.args.get('xField')
                fields = request.args.getlist('fields')
                graph = chartType
                x = get_x(file_id, xField)
                y_lists = get_y(file_id, fields)
                labels = [xField] + fields
                import umap
                import numpy as np
                print('imported umap and numpy :3')
                y_lists = np.array(y_lists)
                y_lists = np.rot90(y_lists)
                reducer = umap.UMAP(n_components=2, random_state=42)
                transformed = reducer.fit_transform(y_lists)
                transformed = transformed.tolist()

                return render_template("ml.html", graph = graph, x=x, y_lists=transformed, labels=labels)
        
    return render_template("ml.html")

@app.route("/file_list")
def file_list():
    if 'username' in session:
        username  = session['username']
        filenames = get_files(username)
        file_ids  = [get_file_id(username, f) for f in filenames]
        return {"files": [
            {"name": fn, "url": url_for('visual', file_id=fid)}
            for fn, fid in zip(filenames, file_ids)
        ]}
    return {"files": []}



if __name__ == "__main__":
    create_tables()  # Initialize database tables before starting the app
    app.run(host='0.0.0.0')
