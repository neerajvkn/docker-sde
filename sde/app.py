from flask import Flask, render_template, request, redirect
import requests
import json

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])

def index():
    if request.method == 'POST':
        data = request.form.to_dict(flat=False)
        req_body = {
            "action": data['action'][0],
            "instance_id": data['instanceID'][0],
            "schedule": data['schedule'][0]
        }
        data = api_call(req_body)
        # return redirect('/')
        return data
    if request.method == 'GET':
        return render_template('index.html')

@app.route('/api_call', methods=['POST'])
def api_call(req_body):

    api_url = 'https://8nofgv3pg0.execute-api.us-east-2.amazonaws.com/default/EC2Scheduler'

    req_body = json.dumps(req_body)
    req = requests.post(api_url, data = req_body)
    decoded_data = req.content.decode("utf-8") 
    return decoded_data

@app.route('/scheduled_instances', methods=['POST'])
def scheduled_instances():
    api_url = 'https://c8il739cx9.execute-api.us-east-2.amazonaws.com/default/ScheduledInstances'
    req = requests.post(api_url)
    parsed = json.loads(req.content)
    return json.dumps(parsed)

if __name__ == "__main__":
    app.run(debug=True)