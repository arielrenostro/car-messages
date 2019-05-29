from flask import Flask, request, json

from query import make_query

app = Flask(__name__)


@app.route('/')
def health_check():
    return '', 200


@app.route('/query', methods=['POST'])
def query():

    payload = json.loads(request.data)
    return make_query(payload)


if __name__ == '__main__':
    app.run(host="0.0.0.0")
