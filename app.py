from flask import Flask, render_template, request, redirect, send_file
from core import parse
import json
import os

TEMP_FILE = 'temp.json'

app = Flask('Audit')

data = parse()

@app.route('/')
def get_policies():
    return render_template('index.html', data=data)

@app.route('/export', methods=["GET", 'POST'])
def export():
    if os.path.exists(TEMP_FILE):
        os.remove(TEMP_FILE)

    if request.method == 'GET':
        index = int(request.args.get('index'))
        policy = list(filter(lambda p: p['index'] == index, data))[0]
        with open(TEMP_FILE, 'w') as output:
            json.dump(policy, output)
    else:
        ids = list(map(lambda val: int(val), json.loads(list(request.form.keys())[0])['value'].split(',')))
        result = list(filter(lambda p: p['index'] in ids, data))
        with open(TEMP_FILE, 'w') as output:
            json.dump(result, output)

    return send_file(TEMP_FILE)

@app.route('/search', methods=["GET"])
def search():
    result = list(filter(lambda d: d['reg_key'] == request.args.get('value'), data))
    return render_template('index.html', data=data, search=result)

if __name__ == '__main__':
    app.run()