from flask import Flask, render_template, request, send_from_directory
from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from werkzeug.utils import secure_filename
import os
import subprocess


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OBJECT_DETECTION_FOLDER'] = 'runs/detect/exp'

app.config['SECRET_KEY'] = 'your_secret_key'  # Change this!
app.config['yolo_path']=r'yolov7/detect.py'
class UploadForm(FlaskForm):
    photo = FileField('Upload Photo')

@app.route('/', methods=['GET', 'POST'])
def upload_photo():
    form = UploadForm()
    if form.validate_on_submit():
        photo = form.photo.data
        filename = secure_filename(photo.filename)
        photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        image_path=r'uploads/'+ filename
        print(image_path)
        print(app.config['yolo_path'])
        subprocess.run(['python', app.config['yolo_path'], '--weights','yolov7/yolov7.pt', '--conf', '0.25','--img-size','640','--source',  image_path,'--exist-ok'])

        # return 'Photo uploaded successfully!'
    return render_template('upload.html', form=form, filenames=os.listdir(app.config['UPLOAD_FOLDER']),filenames_2=os.listdir(app.config['OBJECT_DETECTION_FOLDER']))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/objects/<filename_2>')
def objects(filename_2):
    return send_from_directory(app.config['OBJECT_DETECTION_FOLDER'], filename_2)


if __name__ == '__main__':
    app.run(debug=True)

