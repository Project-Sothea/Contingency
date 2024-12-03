import uuid
from datetime import datetime
from flask import send_from_directory
from flask import Flask, render_template, request
import os

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Allowed file extensions
ALLOWED_EXTENSIONS = {'xlsx'}

# Directory for downloads
DOWNLOAD_FOLDER = os.path.join(os.getcwd(), 'downloads')
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    # Check if the file extension is allowed and if the name matches "DataSheet.xlsx"
    return ('.' in filename and filename.rsplit('.', 1)[
        1].lower() in ALLOWED_EXTENSIONS and filename == "DataSheet.xlsx")


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part", 400
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400
    if file and allowed_file(file.filename):
        # Generate a unique filename
        original_filename = file.filename
        unique_suffix = datetime.now().strftime("%Y%m%d%H%M%S")  # Timestamp
        unique_filename = f"{uuid.uuid4().hex}_{unique_suffix}_{original_filename}"

        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(filepath)

        # Include the upload timestamp in the response
        upload_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Human-readable timestamp
        return f"File uploaded successfully: {file.filename} at {upload_time}", 200
    else:
        return "Invalid file type. Only DataSheet.xlsx files are allowed.", 400


@app.route('/download-datasheet', methods=['GET'])
def download_datasheet():
    filename = "DataSheet.xlsx"
    file_path = os.path.join(DOWNLOAD_FOLDER, filename)

    if not os.path.exists(file_path):
        # Return an error response if the file doesn't exist
        return f"File is unavailable!", 404
    return send_from_directory(DOWNLOAD_FOLDER, filename, as_attachment=True)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)
