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
    
    def search(self, table, search_term=''):
        """Search across all fields in the table"""
        if not search_term:
            return self.execute_query(f'SELECT * FROM {table}')
        
        # Get column names for the table
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(f'PRAGMA table_info({table})')
        columns = [col[1] for col in cursor.fetchall()]
        conn.close()
        
        # Build WHERE clause to search all columns
        where_clauses = []
        params = []
        for column in columns:
            where_clauses.append(f'{column} LIKE ?')
            params.append(f'%{search_term}%')
        
        query = f'SELECT * FROM {table} WHERE {" OR ".join(where_clauses)}'
        return self.execute_query(query, tuple(params))
    
    def get_all(self, table):
        return self.execute_query(f'SELECT * FROM {table}')
    
    def delete(self, table, id_column, id_value):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(f'DELETE FROM {table} WHERE {id_column} = ?', (id_value,))
        conn.commit()
        conn.close()
