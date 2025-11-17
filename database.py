import sqlite3
import json
from datetime import datetime

class HospitalDatabase:
    def __init__(self, db_name, hospital_name):
        self.db_name = db_name
        self.hospital_name = hospital_name
        self.init_database()
    
    def init_database(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Patient table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS patients (
                patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER,
                gender TEXT,
                phone TEXT,
                address TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Doctor table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS doctors (
                doctor_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                specialization TEXT,
                phone TEXT,
                email TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Appointment table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS appointments (
                appointment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id INTEGER,
                doctor_id INTEGER,
                appointment_date TEXT,
                appointment_time TEXT,
                status TEXT DEFAULT 'Scheduled',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
                FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id)
            )
        ''')
        
        # Medical records table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS medical_records (
                record_id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id INTEGER,
                doctor_id INTEGER,
                diagnosis TEXT,
                prescription TEXT,
                notes TEXT,
                record_date TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
                FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def execute_query(self, query, params=()):
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        result = cursor.fetchall()
        conn.close()
        return [dict(row) for row in result]
    
    def insert(self, table, data):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?' for _ in data])
        query = f'INSERT INTO {table} ({columns}) VALUES ({placeholders})'
        cursor.execute(query, list(data.values()))
        conn.commit()
        last_id = cursor.lastrowid
        conn.close()
        return last_id
    
    def search(self, table, search_term='', column='name'):
        query = f'SELECT * FROM {table}'
        if search_term:
            query += f' WHERE {column} LIKE ?'
            return self.execute_query(query, (f'%{search_term}%',))
        return self.execute_query(query)
    
    def get_all(self, table):
        return self.execute_query(f'SELECT * FROM {table}')
    
    def delete(self, table, id_column, id_value):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(f'DELETE FROM {table} WHERE {id_column} = ?', (id_value,))
        conn.commit()
        conn.close()
