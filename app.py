from Resources.searc_in_export_chat import ClearDataFiles
from Resources.connect_db import AddDataToDB, ConnectDB, SQLiteCursor
from werkzeug.utils import secure_filename
from flask import Flask, request, jsonify
from datetime import datetime
import uuid
import os


def first_request():
    ConnectDB()
    ClearDataFiles()


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.getenv('FOLDERS_FILES_CHAT')
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1
app.before_first_request(first_request)


@app.route('/')
def index():
    return 'Ok ola'


@app.route('/uploader', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        id_uuid = str(uuid.uuid4())
        # Caminho para salvar o arquivo
        path = os.path.join(app.config['UPLOAD_FOLDER'], id_uuid)
        # salva o arquivo
        file.save(path)

        try:
            # Chama função que adiciona novo arquivo e dados
            AddDataToDB().init_add_file(id_uuid=id_uuid, path=path, file=secure_filename(file.filename))
        except Exception as error:
            return f'error {error}', 500

        return 'ok', 201


@app.route('/list-numbers', methods=['GET'])
def extract_list_numbers():
    with SQLiteCursor() as cursor:
        cursor.execute('select distinct phone from messages')
        list_phones = [_[0] for _ in cursor.fetchall()]

    return jsonify({'phone': list_phones})


@app.route("/filter", methods=['POST'])
def extract_message_number():
    dicio = {}
    try:
        dicio["phone"] = request.json['phone']
        dicio['date'] = request.json['date']
        dicio['message'] = request.json['message']
    except Exception as error:
        return {'error': str(error)}

    with SQLiteCursor() as cursor:
        sql = "select * from messages"
        data = []

        where = []
        for key, value in dicio.items():
            if value:
                if key == 'phone':
                    where.append(f' {key}=?')
                    data.append(value)

                if key == 'date':
                    data.append(datetime.strptime(value, '%Y-%m-%dT%H:%M:%S'))
                    where.append(f' {key}=?')

                if key == 'message':
                    where.append(f" {key} like ?")
                    data.append('%'+value+'%')

        if data:
            cursor.execute(sql + ' where' + ' and '.join(where), tuple(data))
        else:
            cursor.execute(sql)

        result_filter = [{"phone": _[1], "date": _[2], "message": _[3]} for _ in cursor.fetchall()]

    return jsonify(result_filter), 200


# @app.route("/list-links", methods=['POST'])
# def extract_links():
#     return jsonify(sec.extract_links(phone=request.json['phone'])), 201
#
#
# @app.route("/word-occurence", methods=['POST'])
# def word_occurrence_counter():
#     return jsonify(sec.word_occurrence_counter(
#         phone=request.json['phone'],
#         remove_punctuation=request.json['punctuation'])
#     ), 201
#
#
# @app.route("/word-cloud", methods=['POST'])
# def word_cloud():
#     file_path = sec.word_cloud(phone=request.json['phone'], date=request.json['date'])
#     return send_file(file_path)


if __name__ == '__main__':
    app.run(debug=True)
