import json
import time
from flask import Flask, request

app = Flask(__name__, static_folder='../build', static_url_path='/')


# Health Check
@app.route('/time')
def get_current_time():
    return {'time': time.time()}


# Format of how to send in data using JSON, and then send it back in JSON
@app.route('/train-model', methods=['POST'])
def train_model():
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        json_input = request.get_json(force=True)
        print(json_input['graph'])
        graph = json_input['graph']
        return json.dumps({'agent': "agent"})
    else:
        return json.dumps({'error_message': 'Content-Type not supported!'})

# Add your APIs below
