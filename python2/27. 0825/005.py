from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/sub')
def sub():
    return render_template("sub.html")

@app.route('/form')
def form():
    return render_template("form.html")

@app.route('/user2/<username>', methods=['GET','POST'])
def subname(username):
    #method = request.method
    if request.method == 'GET':
        userid = request.args.get('userid')
        #userid = request.args['userid']

        if userid:
            return f'<h1>어서오세요 {username}({userid})님!</h1>'
        else:
            return f'<h1>어서오세요 {username}님!</h1>'

    #return f'<h1>어서오세요 {username}님!</h1>'
    #return username + userid
    #return request.args

@app.route('/user', methods=['GET'])
def user():
    username = request.args.get('username')
    userid = request.args.get('userid')
    if username:
        return redirect(url_for('subname', username=username, userid=userid))
    return '사용자 이름이 제공되지 않았습니다.'

if __name__ == '__main__':
    app.run(debug=True)