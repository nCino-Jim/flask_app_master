from crypt import methods
from app import app
from flask import render_template, request, redirect, jsonify,  make_response
import os
from werkzeug.utils import secure_filename



app.config['ITUNES_UPLOADS'] = "/Users/jburris/Documents/projects/flask_app_master/app/static/client/uploads"
app.config['ALLOWED_ITUNES_EXTENTIONS'] = ["XML"]

def allowed_image(filename):

    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in app.config['ALLOWED_ITUNES_EXTENTIONS']:
        return True
    else:
        return False

@app.route("/itunes/upload_library", methods=["GET", "POST"])
def upload_library():

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
                image.save(os.path.join(app.config['ITUNES_UPLOADS'], filename))
            
            print("File saved")

    return render_template("public/itunes_conv.html")




# @app.route("/jinja")
# def jinja():
#     my_name = 'Jim'
#     age = 30
#     langs = ['python', 'javascript', 'VB']
#     friends = {
#         "Tom": 30,
#         "Bill": 40,
#         "Steve": 50
#     }
#     colors = ("Red", "Green")

#     class GitRemote:
#         def __init__(self, name, description, url):
#             self.name = name
#             self.description = description    
#             self.url = url

#         def pull(self):
#             return f'Pulling repo {self.name}'

#         def clone(self):
#             return f'Cloning into {self.url}'


#     my_remote = GitRemote(
#         name = 'Flash Jinja',
#         description = 'Template tutorial',
#         url='https://google.com'
#     )
#     def repeat(x, qty):
#         return x * qty


#     return render_template('public/jinja.html', 
#         my_name=my_name,
#         age=age,
#         langs=langs,
#         friends=friends,
#         colors=colors,
#         GitRemote=GitRemote,
#         repeat=repeat,
#         my_remote=my_remote
#         )

# @app.route("/about")
# def about():
#     return render_template("public/about.html")

# @app.route("/sign-up", methods=["GET", "POST"])
# def sign_up():

#     if request.method == "POST":

#         req = request.form
        
#         username = req['username']
#         email = req['email']
#         password = req['password']

#         return redirect(request.url)

#     return render_template("public/sign_up.html")

# users = {
#     'bsmith':{
#         'name': 'Bob Smith',
#         'bio': 'blah blah blah',
#         'twiter_handle': '@bsmith'
#     },
#     'jburris':{
#         'name': 'Jim Burris',
#         'bio': 'blah blah blah',
#         'twiter_handle': '@jburris'
#     },
#     'tmartinez':{
#         'name': 'Tom Martinez',
#         'bio': 'blah blah blah',
#         'twiter_handle': '@tmartinez'        
#     }
# }


# @app.route("/profile/<username>")
# def profile(username):

#     user = None

#     if username in users:
#         user = users[username]

#     return render_template("public/profile.html", username=username, user=user)


# @app.route("/guestbook")
# def guestbook():
#     return render_template("public/guestbook.html")


# @app.route('/guestbook/create-entry', methods=['POST'])
# def create_entry():

#     req = request.get_json()

#     print(req)

#     res = make_response(jsonify({"message": "JSON recieved"}), 200)

#     return res


# @app.route("/query")
# def query():

#     # ?foo=foo&bar=bar&baz=baz&title=quert+strings+with+Flask
#     args = request.args
#     print(args)
#     for k,v in args.items():
#         print(f"{k}: {v}")

#     print(args['title'])

#     return "Query received", 200


