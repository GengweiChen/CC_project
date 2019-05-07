from flask import Flask, render_template, request
from werkzeug import secure_filename
from flask import jsonify
import sys
import requests
import os

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
            ##for f in files:
            ##f.replace(' ', '_')
        print(files)
        str1 = {}
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
            print(fname1)
            if file and allowed_file(fname1):
                ##file.filename.replace(' ', '-')
                ##print(file.filename)
                #dir_path = os.path.dirname(os.path.realpath(file.filename))
                #print(dir_path)
                #file.save(dir_path, name='Newname')
                file.save(secure_filename(fname1))
                f = {'file': open(fname1,'rb')}
                r = requests.post("https://predictapp.azurewebsites.net/predict", files=f)
                print(r.text)
                ##dic_tmp = {}
                dic_tmp = r.json()
                if dic_tmp.get('predictionHealthy') > dic_tmp.get('predictionUnhealthy'):
                    str1[file.filename] = str(dic_tmp) + '\n\n\n\nFinal result: The cow is healthy'
                else:
                    str1[file.filename] = str(dic_tmp) + '\n\n\n\nFinal result: The cow is unhealthy'
            else:
                str1[file.filename] = 'file not supported'
        print(str1)
        return render_template('Result.html', result = str1)


if __name__ == '__main__':
    app.run(debug = True)
