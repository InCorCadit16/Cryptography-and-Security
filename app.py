from flask import Flask, render_template, request, send_file
from core import data, write_export, TEMP_FILE, check_policies, enforce


app = Flask('Audit')
app.secret_key = 'secret'

@app.route('/')
def get_policies():
    return render_template('index.html', data=data)


@app.route('/export', methods=["GET", 'POST'])
def export():
    ids = [int(request.args.get('index'))] if request.method == 'GET' else request.json
    write_export(ids)
    return send_file(TEMP_FILE)


@app.route('/search', methods=["GET"])
def search():
    result = list(filter(lambda d: d['reg_key'] == request.args.get('value'), data))
    return render_template('index.html', data=data, search=result)


@app.route('/test', methods=['POST'])
def test():
    check_result = check_policies(request.json)
    return render_template('check.html', result=check_result)

@app.route('/enforce', methods=['POST'])
def enforce():
    enforce_result = enforce(request.json)
    return enforce_result



if __name__ == '__main__':
    app.run()