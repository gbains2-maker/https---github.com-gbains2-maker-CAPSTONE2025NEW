import os
from flask import Flask, render_template, request, send_file, redirect, url_for, flash
from werkzeug.utils import secure_filename
from pydub import AudioSegment

UPLOAD_FOLDER = "uploads"
CONVERTED_FOLDER = "converted"
ALLOWED_EXTENSIONS = {"mp3"}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CONVERTED_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["CONVERTED_FOLDER"] = CONVERTED_FOLDER
app.secret_key = "dev-secret-key"  # for flash messages


def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "file" not in request.files:
            flash("No file part.")
            return redirect(request.url)

        file = request.files["file"]
        if file.filename == "":
            flash("No file selected.")
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            input_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(input_path)

            base_name = os.path.splitext(filename)[0]
            output_filename = base_name + ".wav"
            output_path = os.path.join(app.config["CONVERTED_FOLDER"], output_filename)

            # Convert using pydub
            audio = AudioSegment.from_mp3(input_path)
            audio.export(output_path, format="wav")

            return send_file(output_path, as_attachment=True, download_name=output_filename)
        else:
            flash("Please upload an .mp3 file.")
            return redirect(request.url)

    return render_template("index.html")


@app.route("/page1")
def page1():
    return render_template("page1.html")


@app.route("/page2")
def page2():
    return render_template("page2.html")


if __name__ == "__main__":
    app.run(debug=True)
