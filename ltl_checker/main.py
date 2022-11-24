import os
from flask import Flask, request, render_template, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from datetime import datetime

ALLOWED_EXTENSIONS = set(['csv']) #here we can specify the file extensions that our application allows

#init global vars
filename = ''
savelocation = os.path.join(os.getcwd(), 'ltl_checker', 'uploads')


def allowed_file(filename): ## this function checks whether file is in right format
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS


app = Flask(__name__)
@app.route('/')
@app.route('/upload',methods = ['GET', 'POST'])



def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename): # check whether file has right format
            filename = secure_filename(file.filename)
            save_location = os.path.join(savelocation, filename) # event log should be saved in uploads file for later use
            file.save(save_location)
            return render_template('columns-selection.html')
        else:
            return ('error: wrong file format')

    return render_template('upload.html')







if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
