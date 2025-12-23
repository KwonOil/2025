from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from datetime import datetime

import secrets

app = Flask(__name__)
# app.config['SECRET_KEY'] = secrets.token_hex(16)

@app.route('/', methods=['GET', 'POST'])
@app.route('/<path:filename>', methods=['GET', 'POST'])
def home(filename='index.html'):
    return render_template(filename, template_name=filename, current_time=datetime.now())

@app.route('/images/<path:filename>')
def images(filename):
    return send_from_directory("static/images", filename)

@app.route('/css/<path:filename>')
def css(filename):
    return send_from_directory("static/css", filename)

@app.route('/js/<path:filename>')
def js(filename):
    return send_from_directory("static/js", filename)

if __name__ == '__main__':
    app.run(debug=True)