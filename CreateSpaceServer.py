from flask import Flask, render_template, Markup, request, send_file, jsonify
import json
from werkzeug.serving import WSGIRequestHandler
import atlassian_api_handler

WSGIRequestHandler.protocol_version = "HTTP/1.1"

app = Flask(__name__, static_folder=r'D:\Softwares\Flutter\Projects\python_programming\new_background_idea\retry')


@app.route('/create-space', methods=['POST', 'GET'])
def create_space():
    if request.method == 'POST':
        user = request.form.get("user")
        password = request.form.get("password")
        name = request.form.get("name")
        key = request.form.get("key")
        admin = request.form.get("admin")
        status, error_str = atlassian_api_handler.start_confluence_api(user, password, name, key, admin)
        return render_template("createspace.html", error=error_str)



@app.route('/')
def loadPage():
    return render_template("createspace.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)