import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_ngrok import run_with_ngrok
from get_heartrate import heartrate

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'wav', 'webm', 'mp4'])

app = Flask(__name__)
run_with_ngrok(app)   
app.config['UPLOAD_FOLDER'] = 'upload/'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    else:
            return render_template('upload.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    hr, video = heartrate(os.path.join(app.config['UPLOAD_FOLDER'],
                               filename))

    return render_template('results.html', heartrate=str(hr), video=video)

if __name__ == "__main__":
    app.run()
