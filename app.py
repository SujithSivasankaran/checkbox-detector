from azure.storage.blob import BlobClient
import requests,uuid
import json
from flask import Flask, flash, request, redirect, url_for, render_template


app = Flask(__name__)


#UPLOAD_FOLDER = 'static/uploads/'

app.secret_key = "secret key"
#app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['png','jpg'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/', methods=['POST','GET'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        id = str(uuid.uuid1())
        blob = BlobClient.from_connection_string(
            conn_str="DefaultEndpointsProtocol=https;AccountName=imgclass;AccountKey=jwli+rbvjB2Y2VB8jRfuR0ZknUiPJYuxFBDLl6hC1GawM47zJqSFebJr+7P4s6o023GPDfLSMcB9pZmY4i643Q==;EndpointSuffix=core.windows.net",
            container_name="image", blob_name=id)
        blob.upload_blob(file)
        url = 'https://imgclass.blob.core.windows.net/image/' + str(id)
        test = json.dumps({"data": url})
        headers = {'Content-Type': 'application/json'}
        service = 'http://2763883e-5e97-4519-a45c-3d770aa1cec0.centralus.azurecontainer.io/score'
        resp = requests.post(service, test, headers=headers)
        m = resp.text
        flash(m)
        return render_template('index.html')
    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)



if __name__ == '__main__':
    app.run(debug=True)


