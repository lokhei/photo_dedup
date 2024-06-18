import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
from duplicates import find_duplicates

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


@app.route('/upload', methods=['POST'])
def upload_image():
    files = request.files.getlist('images')
    for file in files:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return jsonify({"message": "Images uploaded successfully"}), 200

@app.route('/get_duplicates', methods=['GET'])
def get_duplicates():
    groups = find_duplicates(app.config['UPLOAD_FOLDER'])
    # print(groups)
    return groups, 200


@app.route('/images/<path:filename>', methods=['GET'])
def serve_image(filename):
    print("FILE")
    print(filename)
    return send_from_directory("", filename)


# Endpoint to set the image directory
@app.route('/set_directory', methods=['POST'])
def set_directory():
    data = request.get_json()
    app.config['UPLOAD_FOLDER'] = data.get('directory_path')
    return jsonify({'status': 'success', 'directory_path': app.config['UPLOAD_FOLDER']}), 200


@app.route('/delete', methods=['POST'])
def delete_images():
    image_paths = request.json.get('image_paths', [])
    print(image_paths)
    for path in image_paths:
        print(path)
        if os.path.exists(path):
            os.remove(path)
    return jsonify({"message": "Selected images deleted successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True)
