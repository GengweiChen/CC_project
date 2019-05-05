from flask import Flask, render_template, request
from werkzeug import secure_filename
from flask import jsonify
import sys
import requests

app = Flask(__name__)

app.config['ALLOWED_EXTENSIONS'] = set(['pdf', 'png', 'jpg', 'jpeg'])

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def upload():
    return render_template('Predict.html')

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        files = request.files.getlist("pic[]")
        print(files)
        list = []
        for file in files:
            if file and allowed_file(file.filename):
                print(file)
                file.save(secure_filename(file.filename))
                f = {'file': open(file.filename,'rb')}
                r = requests.post("https://predictapp.azurewebsites.net/predict", files=f)
                print(r.text)
                list.append(r.json())
            else:
                return 'file not supported'
        print(list)
        return str(list)


if __name__ == '__main__':
    app.run(debug = True)
