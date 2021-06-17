import json

from flask import Flask, render_template, request
app = Flask(__name__)


@app.route('/', methods = ['POST', 'GET'])
def hello_world():
    if(request.method == 'GET'):
        with open("users.json",'r') as file:
            data = json.load(file)
            return render_template("index.html",content=data)

    elif(request.method == 'POST'):
        print(str(request.data,'utf-8'))
        json_data = json.loads(str(request.data,'utf-8'))
        print(json_data)
        with open("users.json",'r+') as file:
            data = json.load(file)
            data.append(json_data)
            file.seek(0)
            json.dump(data,file, sort_keys=True, indent='\t', separators=(',', ': '))
            return "JSON posted"

@app.route('/get-data', methods = ['GET'])
def get_data():
    with open("users.json", 'r+') as file:
        data = json.load(file)
        return json.dumps(data)


if __name__ == '__main__':
    app.run(host="192.168.0.108",port=5000)