
from app import app
from flask import render_template, request, redirect, send_from_directory, abort
import os
from werkzeug.utils import secure_filename



app.config['IMAGE_UPLOADS'] = "/Users/jamesburris/Documents/projects/flask_app_master/app/static/img/uploads"
app.config['ALLOWED_IMAGE_EXTENTIONS'] = ["PNG", "JPG", "JPEG", "GIF"]

def allowed_image(filename):

    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in app.config['ALLOWED_IMAGE_EXTENTIONS']:
        return True
    else:
        return False

@app.route("/upload-image", methods=["GET", "POST"])
def upload_image():

    if request.method == "POST":
        if request.files:
            image = request.files["image"]

            if image.filename == "":
                
                print("Image must have a filename")
                return redirect(request.url)

            if not allowed_image(filename=image.filename):
                print ("That image ext is not allowed")
                return redirect(request.url)
            else:
                filename = secure_filename(image.filename)
                image.save(os.path.join(app.config['IMAGE_UPLOADS'], filename))
            
            print("File saved")

    return render_template("public/upload_image.html")

'''
string:
int:
float:
path:
uuid:
'''

app.config['CLIENT_IMAGES'] = '/Users/jamesburris/Documents/projects/flask_app_master/app/static/client/img'
app.config['CLIENT_CSV'] = '/Users/jamesburris/Documents/projects/flask_app_master/app/static/client/csv'
app.config['CLIENT_REPORTS'] = '/Users/jamesburris/Documents/projects/flask_app_master/app/static/client/reports'

@app.route('/get-image/<image_name>')
def get_image(image_name):
    try:
        return send_from_directory(
            directory=app.config['CLIENT_IMAGES'], 
            path = image_name, 
            as_attachment=True)

    except FileNotFoundError:
        abort(404)


@app.route('/get-image/<path:path>')
def get_report(path):
    try:
        return send_from_directory(
            directory=app.config['CLIENT_REPORTS'], 
            path = path, 
            as_attachment=True)

    except FileNotFoundError:
        abort(404)

