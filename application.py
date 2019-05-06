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
        list = {}
        for file in files:
            tmp = file.filename
            fname = ""
            if tmp.find(' ') != -1:
                i = 0
                while i < len(tmp):
                    if tmp[i] == ' ':
                        i += 1
                    else:
                        fname += tmp[i]
                        i += 1
            else:
                fname = tmp
            fname1 = fname.lower()
            print(fname)
            if file and allowed_file(fname1):
                file.save(secure_filename(fname1))
                f = {'file': open(fname1,'rb')}
                r = requests.post("https://predictapp.azurewebsites.net/predict", files=f)
                print(r.text)
                ##list[file.filename] = r.json()
                dic_tmp = r.json()
                if dic_tmp.get('predictionHealthy') > 0.1:
                    list[file.filename] = str(dic_tmp) + ' Healthy'
                else:
                    list[file.filename] = str(dic_tmp) + ' Unhealthy'
            else:
                list[file.filename] = 'file not supported'
        print(list)
        return str(list)


if __name__ == '__main__':
    app.run(debug = True)
