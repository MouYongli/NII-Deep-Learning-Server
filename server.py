from flask import Flask, url_for, send_from_directory, request, render_template
import logging, os
from werkzeug import secure_filename
import os


app = Flask(__name__, static_url_path='', static_folder = "uploads")
file_handler = logging.FileHandler('server.log')
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)

PROJECT_HOME = os.path.dirname(os.path.realpath(__file__))
UPLOAD_FOLDER = '{}/uploads/'.format(PROJECT_HOME)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def create_new_folder(local_dir):
    newpath = local_dir
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    return newpath

@app.route('/', methods = ['POST'])
def api_root():
    app.logger.info(PROJECT_HOME)
    if request.method == 'POST' and request.files['bridge']:
        app.logger.info(app.config['UPLOAD_FOLDER'])
        img = request.files['bridge']
        img_name = secure_filename(img.filename)
        create_new_folder(app.config['UPLOAD_FOLDER'])
        saved_path = os.path.join(app.config['UPLOAD_FOLDER'], img_name)
        app.logger.info("saving {}".format(saved_path))
        img.save(saved_path)








        return send_from_directory(app.config['UPLOAD_FOLDER'],img_name, as_attachment=True)
    else:
        return "Where is the image?"


@app.route('/show', methods = ['GET'])
def show():
    images = os.listdir('/home/yongli/Documents/flask-api-upload-image-master/uploads')
    return render_template('images.html', images=images)

if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=False)