from werkzeug.utils import secure_filename
from flask import Flask, request, jsonify
from searc_in_export_chat import SearchInExportChat
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'file_folder/'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1

files = 'file_folder/conversa.txt'


@app.route('/')
def index():
    return 'Ok'


@app.route('/uploader', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return 'ok', 201


@app.route('/eln', methods=['POST'])
def extract_list_numbers():
    sec = SearchInExportChat(files)
    return jsonify(sec.extract_list_numbers())


@app.route("/edn", methods=['POST'])
def extract_data_number():
    sec = SearchInExportChat(files)
    return jsonify(sec.extract_data_number(request.json['phone']))


@app.route("/emn", methods=['POST'])
def extract_message_number():
    sec = SearchInExportChat(files)
    return jsonify(sec.extract_message_number(request.json['phone']))


@app.route("/elm", methods=['POST'])
def extract_links_in_message():
    sec = SearchInExportChat(files)

    return jsonify(sec.extract_links_in_message(request.json['phone']))


@app.route("/woc", methods=['POST'])
def word_occurrence_counter():
    sec = SearchInExportChat(files)

    return jsonify(sec.word_occurrence_counter(request.json['phone'], request.json['punctuation']))


if __name__ == '__main__':
    app.run(debug=True)
