from flask import Flask, jsonify
import datetime
import os

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        "service": "Flask K8s Demo",
        "status": "running",
        "timestamp": datetime.datetime.now().isoformat(),
        "hostname": os.environ.get('HOSTNAME', 'unknown')
    })

@app.route('/health')
def health():
    return jsonify({"status": "healthy"}), 200

@app.route('/info')
def info():
    return jsonify({
        "version": "1.0.0",
        "python_version": "3.9",
        "framework": "Flask"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)