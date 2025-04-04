from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/visual")
def visual():
    return render_template("visual.html")

@app.route("/upload")
def upload():
    return render_template("upload.html")

@app.route("/ml")
def ml():
    return render_template("ml.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0')
