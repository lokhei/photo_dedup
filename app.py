import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from tensorflow.keras.applications.vgg16 import VGG16
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
    print(groups)
    # result = {'images/20190725_195942.jpg': ['images/20190725_195944.jpg', 'images/20190725_195945.jpg', 'images/20190725_195946.jpg', 'images/20190725_195947.jpg', 'images/20190725_195949.jpg'], 'images/20190806_152610.jpg': ['images/20190806_152611.jpg'], 'images/20190806_153256.jpg': ['images/20190806_153259.jpg'], 'images/20190806_153445.jpg': ['images/20190806_153448.jpg', 'images/20190806_153449.jpg'], 'images/20190806_153531.jpg': ['images/20190806_153535.jpg'], 'images/20190806_153542.jpg': ['images/20190806_153543.jpg'], 'images/received_1238167046384879.jpeg': ['images/received_591336128061108.jpeg'], 'images/received_1446293368851368.jpeg': ['images/received_2248545758791910.jpeg', 'images/received_636852053391041.jpeg'], 'images/received_1669270329874592.jpeg': ['images/received_1860228334122433.jpeg', 'images/received_2455974407980752.jpeg', 'images/received_474708353362732.jpeg', 'images/received_700614207066273.jpeg'], 'images/received_2397690047169942.jpeg': ['images/received_853499358368703.jpeg'], 'images/received_2449826415245875.jpeg': ['images/received_358791084799482.jpeg'], 'images/received_2951191014943318.jpeg': ['images/received_880075679029306.jpeg'], 'images/received_329925327884101.jpeg': ['images/received_472849746881376.jpeg'], 'images/received_361478017814576.jpeg': ['images/received_971134336552092.jpeg'], 'images/received_375343243114685.jpeg': ['images/received_498372267605590.jpeg'], 'images/received_387161685151538.jpeg': ['images/received_469246037193848.jpeg', 'images/received_477885279656890.jpeg'], 'images/received_392299164820990.jpeg': ['images/received_923907671291694.jpeg'], 'images/received_501874913919241.jpeg': ['images/received_713087319141907.jpeg']}
    return groups, 200


@app.route('/images/<path:filename>', methods=['GET'])
def serve_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


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
