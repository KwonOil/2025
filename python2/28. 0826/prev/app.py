from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from datetime import datetime
#import secrets

app = Flask(__name__)
#app.config['SECRET_KEY'] = secrets.token_hex(16)

@app.route('/', methods=['GET', 'POST'])
@app.route('/<string:filename>', methods=['GET', 'POST'])
def home(filename='index'):
    avail = ['index','myskills','Portfolio','Contact']
    if not filename in avail:
        return ''
    return render_template(filename+'.html', template_name=filename, current_time=datetime.now())

@app.route('/images/<path:filename>')
def images(filename):
    return send_from_directory("static/images", filename)

@app.route('/css/<path:filename>')
def css(filename):
    return send_from_directory("static/css", filename)

@app.route('/js/<path:filename>')
def js(filename):
    return send_from_directory("static/js", filename)

@app.route('/fonts/<path:filename>')
def fonts(filename):
    return send_from_directory("static/fonts", filename)

if __name__ == '__main__':
    app.run(debug=True, port=5001)