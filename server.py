from flask import Flask, request, jsonify
from database import HospitalDatabase
import sys

app = Flask(__name__)
db = None

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'hospital': db.hospital_name})

@app.route('/patients', methods=['GET', 'POST'])
def patients():
    if request.method == 'GET':
        search_term = request.args.get('search', '')
        return jsonify(db.search('patients', search_term))
    elif request.method == 'POST':
        data = request.json
        patient_id = db.insert('patients', data)
        return jsonify({'patient_id': patient_id, 'status': 'success'})

@app.route('/doctors', methods=['GET', 'POST'])
def doctors():
    if request.method == 'GET':
        search_term = request.args.get('search', '')
        return jsonify(db.search('doctors', search_term))
    elif request.method == 'POST':
        data = request.json
        doctor_id = db.insert('doctors', data)
        return jsonify({'doctor_id': doctor_id, 'status': 'success'})

@app.route('/appointments', methods=['GET', 'POST'])
def appointments():
    if request.method == 'GET':
        return jsonify(db.get_all('appointments'))
    elif request.method == 'POST':
        data = request.json
        appointment_id = db.insert('appointments', data)
        return jsonify({'appointment_id': appointment_id, 'status': 'success'})

@app.route('/medical_records', methods=['GET', 'POST'])
def medical_records():
    if request.method == 'GET':
        return jsonify(db.get_all('medical_records'))
    elif request.method == 'POST':
        data = request.json
        record_id = db.insert('medical_records', data)
        return jsonify({'record_id': record_id, 'status': 'success'})

@app.route('/patients/<int:patient_id>', methods=['DELETE'])
def delete_patient(patient_id):
    db.delete('patients', 'patient_id', patient_id)
    return jsonify({'status': 'success'})

@app.route('/doctors/<int:doctor_id>', methods=['DELETE'])
def delete_doctor(doctor_id):
    db.delete('doctors', 'doctor_id', doctor_id)
    return jsonify({'status': 'success'})

def start_server(hospital_name, port, db_name):
    global db
    db = HospitalDatabase(db_name, hospital_name)
    app.run(host='0.0.0.0', port=port, debug=False)

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("Usage: python server.py <hospital_name> <port> <db_name>")
        sys.exit(1)
    
    hospital_name = sys.argv[1]
    port = int(sys.argv[2])
    db_name = sys.argv[3]
    
    start_server(hospital_name, port, db_name)
