import sys
sys.path.insert(0, '.')

from database import HospitalDatabase
from flask import Flask, jsonify

print("Testing Flask app directly...")
print("=" * 50)

# Create a simple test app
app = Flask(__name__)
db = HospitalDatabase('test_direct.db', 'Test Hospital')

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'hospital': db.hospital_name})

@app.route('/test', methods=['GET'])
def test():
    return "Hello from Flask!"

print("Starting test server on port 5003...")
print("Open browser and go to: http://localhost:5003/health")
print("Or go to: http://localhost:5003/test")
print("=" * 50)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5003, debug=True)
