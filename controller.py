from flask import Flask, request, jsonify
from flask_cors import CORS
from service import forward_request

app = Flask(__name__)
CORS(app)

@app.route('/api/<service_name>/<path:endpoint>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def gateway(service_name, endpoint):
    response = forward_request(service_name, endpoint, request)
    return jsonify(response), response.get('status_code', 500)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
