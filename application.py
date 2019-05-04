from flask import Flask, render_template, request
from werkzeug import secure_filename
from flask import jsonify
import sys
import requests

app = Flask(__name__)

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
            file.save(secure_filename(file.filename))
            f = {'file': open(file.filename,'rb')}
            r = requests.post("https://predictapp.azurewebsites.net/predict", files=f)
            print(r.text)
            list.append(r.json())
        print(list)
        return str(list)


if __name__ == '__main__':
    app.run(debug = True)
