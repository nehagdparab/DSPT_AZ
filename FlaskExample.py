from flask import Flask,request,render_template,redirect,url_for,jsonify
from pymongo import MongoClient

app = Flask(__name__)

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')

@app.route('/hello')
def hello():
    return render_template('hello.html')

def mongodb():
    client = MongoClient(port=27017)
    db=client.usertable
    data = db.userdata.find_one()
    print(data)
    username = data['username']
    password = data['password']
    return username,password

username,password = mongodb()

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != username or request.form['password'] != password:
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('welcome'))
    return render_template('login.html', error=error)


@app.route('/', methods=['GET'])
def index_page():
    response = jsonify({'username': username, 'password': password})
    response.status_code = 200

    return response


if __name__ == '__main__':
    app.run(host='https://dsptappmongo.azurewebsites.net', port=5000, debug=True)