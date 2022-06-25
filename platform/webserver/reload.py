import os
from flask import request, Flask
app = Flask(__name__)
@app.route('/reload')
def reload():
    if request.args.get('password') == 'stuffdude':
        try:
            os.system('git pull origin master')
            return 'success'
        except:
            return 'fail'
    else:
        return 'wrong password'
