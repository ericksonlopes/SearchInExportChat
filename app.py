from werkzeug.utils import secure_filename
from flask import Flask, request, jsonify, send_file
from searc_in_export_chat import SearchInExportChat
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'file_folder/'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1

files = 'conversa'
sec = SearchInExportChat(files)


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


@app.route('/list-numbers', methods=['GET'])
def extract_list_numbers():
    return jsonify(sec.list_phones()), 201


@app.route("/filter", methods=['POST'])
def extract_message_number():
    # **request.args.to_dict()
    return jsonify(sec.filter_data(
        phone=request.json['phone'],
        date=request.json['date'],
        message=request.json['message'])), 201


@app.route("/list-links", methods=['POST'])
def extract_links():
    return jsonify(sec.extract_links(phone=request.json['phone'])), 201


@app.route("/word-occurence", methods=['POST'])
def word_occurrence_counter():
    return jsonify(sec.word_occurrence_counter(
        phone=request.json['phone'],
        remove_punctuation=request.json['punctuation'])
    ), 201


@app.route("/word-cloud", methods=['POST'])
def word_cloud():
    file_path = sec.word_cloud(phone=request.json['phone'], date=request.json['date'])
    return send_file(file_path)


if __name__ == '__main__':
    app.run(debug=True)
