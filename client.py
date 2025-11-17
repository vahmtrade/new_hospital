import requests
import json

class HospitalClient:
    def __init__(self, base_url):
        self.base_url = base_url
    
    def check_health(self):
        try:
            response = requests.get(f'{self.base_url}/health', timeout=2)
            return response.json() if response.status_code == 200 else None
        except:
            return None
    
    def get_patients(self, search_term=''):
        try:
            response = requests.get(f'{self.base_url}/patients', 
                                  params={'search': search_term}, timeout=5)
            return response.json() if response.status_code == 200 else []
        except:
            return []
    
    def add_patient(self, patient_data):
        try:
            response = requests.post(f'{self.base_url}/patients', 
                                   json=patient_data, timeout=5)
            return response.json() if response.status_code == 200 else None
        except:
            return None
    
    def get_doctors(self, search_term=''):
        try:
            response = requests.get(f'{self.base_url}/doctors', 
                                  params={'search': search_term}, timeout=5)
            return response.json() if response.status_code == 200 else []
        except:
            return []
    
    def add_doctor(self, doctor_data):
        try:
            response = requests.post(f'{self.base_url}/doctors', 
                                   json=doctor_data, timeout=5)
            return response.json() if response.status_code == 200 else None
        except:
            return None
    
    def get_appointments(self):
        try:
            response = requests.get(f'{self.base_url}/appointments', timeout=5)
            return response.json() if response.status_code == 200 else []
        except:
            return []
    
    def add_appointment(self, appointment_data):
        try:
            response = requests.post(f'{self.base_url}/appointments', 
                                   json=appointment_data, timeout=5)
            return response.json() if response.status_code == 200 else None
        except:
            return None
    
    def get_medical_records(self):
        try:
            response = requests.get(f'{self.base_url}/medical_records', timeout=5)
            return response.json() if response.status_code == 200 else []
        except:
            return []
    
    def add_medical_record(self, record_data):
        try:
            response = requests.post(f'{self.base_url}/medical_records', 
                                   json=record_data, timeout=5)
            return response.json() if response.status_code == 200 else None
        except:
            return None
