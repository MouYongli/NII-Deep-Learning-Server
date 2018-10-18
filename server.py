from flask import Flask, request, render_template, make_response, jsonify, send_file
import logging, os
from werkzeug import secure_filename
import os
import cv2 as cv

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

    app.logger.info('Get a request!')
    if request.method == 'POST' and request.files['bridge']:

        app.logger.info(app.config['UPLOAD_FOLDER'])
        img = request.files['bridge']
        img_name = secure_filename(img.filename)
        create_new_folder(app.config['UPLOAD_FOLDER'])
        saved_path = os.path.join(app.config['UPLOAD_FOLDER'], img_name)
        app.logger.info("saving {}".format(saved_path))
        img.save(saved_path)

        cv_img = cv.imread(saved_path)
        edges = cv.Canny(cv_img, 100, 200)
        cv.imwrite(saved_path, edges)

        #retval, buffer = cv.imencode('.png', edges)
        #response = make_response(buffer.tobytes())
        result = {'url': 'http://192.168.0.11:5000/uploads/'+img_name, 'status': 200}
        response = make_response(jsonify(result))
        response.headers['Content-Type'] = 'application/json'
        return response

        #return send_from_directory(app.config['UPLOAD_FOLDER'],img_name, as_attachment=True)
    else:
        return "Where is the image?"


@app.route('/show', methods = ['GET'])
def show():
    images = os.listdir('/home/yongli/Documents/flask-api-upload-image-master/uploads')
    return render_template('images.html', images=images)

@app.route('/uploads/<filename>', methods = ['GET'])
def get_image(filename):
    images = os.listdir('/home/yongli/Documents/flask-api-upload-image-master/uploads')
    if filename in images:
        return send_file('./uploads/'+filename, mimetype='image/jpeg')
    else:
        return 'No such a image named \"'+filename+'\"'


if __name__ == '__main__':
    app.run(host='192.168.0.11',debug=False)