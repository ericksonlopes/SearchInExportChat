import uuid

from flask import Flask, request, jsonify, send_file
from searc_in_export_chat import SearchInExportChat
from werkzeug.utils import secure_filename
from connect_db import ConnectDB
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'file_folder/'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1

files = 'conversa_cortada'
sec = SearchInExportChat(files)


@app.route('/')
def index():
    return 'Ok'


@app.route('/uploader', methods=['POST'])
def upload_file():
    db = ConnectDB()

    if request.method == 'POST':
        file = request.files['file']
        id_uuid = str(uuid.uuid4())
        # Caminho para salvar o arquivo
        path = os.path.join(app.config['UPLOAD_FOLDER'], id_uuid)
        # salva o arquivo
        file.save(path)
        # abre uma conxão com o banco
        connect = db.connect()
        cursor = connect.cursor()

        sql = "insert into files (uuid, path_name, name_file) values (?, ?, ?)"
        datas = (id_uuid, path, secure_filename(file.filename))

        cursor.execute(sql, datas)
        connect.commit()
        cursor.close()
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
