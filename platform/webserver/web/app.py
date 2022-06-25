from flask import request, Flask
import json
app = Flask(__name__)


@app.route('/plus_one')
def plus_one():
    x = int(request.args.get('x', 1))
    return json.dumps({'x': x + 1})


@app.route('/square')
def square():
    x = int(request.args.get('x', 1))
    return json.dumps({'x': x * x})
