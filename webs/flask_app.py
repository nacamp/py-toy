from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/post_json', methods=['POST'])
def post():
    in_data = request.json
    return jsonify(in_data)

# run in pycharm
if __name__ == '__main__':
    app.run()

'''
https://flask.palletsprojects.com/en/1.1.x/

#run in linux
$ export FLASK_APP=flask_app.py
$ flask run
'''
