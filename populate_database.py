import sqlite3
import random
from datetime import datetime, timedelta

# Iranian names in English
first_names_male = [
    'Ali', 'Mohammad', 'Hossein', 'Reza', 'Ahmad', 'Mahdi', 'Hassan', 'Amir', 'Saeed', 'Majid',
    'Mohsen', 'Javad', 'Ebrahim', 'Asghar', 'Akbar', 'Karim', 'Rahim', 'Sadegh', 'Bagher', 'Jafar',
    'Hamid', 'Mehran', 'Behzad', 'Farhad', 'Omid', 'Vahid', 'Nima', 'Arash', 'Babak', 'Siavash'
]

first_names_female = [
    'Fatemeh', 'Zahra', 'Maryam', 'Zeinab', 'Somayeh', 'Narges', 'Mahsa', 'Sara', 'Nazanin', 'Elham',
    'Shima', 'Nasrin', 'Parisa', 'Mina', 'Samaneh', 'Leila', 'Negar', 'Reyhaneh', 'Sahar', 'Mahnaz',
    'Farzaneh', 'Niloofar', 'Atefeh', 'Mitra', 'Sepideh', 'Golnaz', 'Yasaman', 'Shadi', 'Azadeh', 'Elnaz'
]

last_names = [
    'Ahmadi', 'Mohammadi', 'Hosseini', 'Rezaei', 'Alavi', 'Mousavi', 'Karimi', 'Jafari', 'Noori', 'Sadeghi',
    'Hassani', 'Rahimi', 'Ebrahimi', 'Akbari', 'Asghari', 'Bagheri', 'Saeedi', 'Majidi', 'Amiri', 'Mahdavi',
    'Kazemi', 'Hashemi', 'Rostami', 'Fatemi', 'Zareei', 'Najafi', 'Ghasemi', 'Yousefi', 'Sharifi', 'Taheri',
    'Moradi', 'Rahmani', 'Azizi', 'Abbasi', 'Zamani', 'Asadi', 'Ghorbani', 'Safari', 'Soltani', 'Mirzaei'
]

cities = [
    'Tehran', 'Mashhad', 'Isfahan', 'Shiraz', 'Tabriz', 'Karaj', 'Ahvaz', 'Qom', 'Kermanshah', 'Urmia',
    'Rasht', 'Zahedan', 'Hamedan', 'Kerman', 'Yazd', 'Ardabil', 'Bandar Abbas', 'Qazvin', 'Zanjan', 'Sanandaj'
]

streets = [
    'Valiasr St', 'Azadi St', 'Enghelab St', 'Shariati St', 'Motahari St',
    'Ferdowsi St', 'Hafez St', 'Saadi St', 'Imam Khomeini St', 'Taleghani St',
    'Beheshti St', 'Kargar St', 'Resalat St', 'Sattar Khan St', 'Mirdamad Blvd'
]

specializations = [
    'Cardiology', 'General Surgery', 'Internal Medicine', 'Pediatrics', 'Obstetrics and Gynecology', 'Orthopedics',
    'Ophthalmology', 'ENT', 'Dermatology', 'Psychiatry', 'Neurology',
    'Urology', 'Gastroenterology', 'Endocrinology', 'Pulmonology', 'Hematology and Oncology'
]

diagnoses = [
    'Common Cold', 'Hypertension', 'Type 2 Diabetes', 'Asthma', 'Migraine', 'Osteoarthritis',
    'Gastritis', 'Lower Back Pain', 'Influenza', 'Allergic Rhinitis', 'Headache', 'Anemia', 'Depression',
    'Anxiety Disorder', 'Kidney Stone', 'Hyperlipidemia', 'Thyroid Disorder', 'Sinusitis', 'Bronchitis', 'Joint Pain'
]

prescriptions = [
    'Acetaminophen 500mg - 3 times daily', 'Ibuprofen 400mg - 2 times daily',
    'Amoxicillin 500mg - 3 times daily', 'Cetirizine 10mg - at bedtime',
    'Omeprazole 20mg - morning before meal', 'Metformin 500mg - 2 times daily',
    'Losartan 50mg - once daily', 'Atorvastatin 20mg - at bedtime',
    'Salbutamol Inhaler - as needed', 'Diclofenac 50mg - 2 times daily'
]

def create_database(db_name):
    """Create database and tables"""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # Patients table
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
    
    # Doctors table
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
    
    # Appointments table
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

def populate_patients(db_name, count=50):
    """Add patients"""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    for i in range(count):
        gender = random.choice(['Male', 'Female'])
        if gender == 'Male':
            first_name = random.choice(first_names_male)
        else:
            first_name = random.choice(first_names_female)
        
        last_name = random.choice(last_names)
        name = f"{first_name} {last_name}"
        age = random.randint(1, 85)
        phone = f"+98-9{random.randint(10, 99)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}"
        city = random.choice(cities)
        street = random.choice(streets)
        address = f"{random.randint(1, 500)} {street}, {city}, Iran"
        
        cursor.execute('''
            INSERT INTO patients (name, age, gender, phone, address)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, age, gender, phone, address))
    
    conn.commit()
    conn.close()
    print(f"✓ {count} patients added")

def populate_doctors(db_name, count=20):
    """Add doctors"""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    for i in range(count):
        gender = random.choice(['Male', 'Female'])
        if gender == 'Male':
            first_name = random.choice(first_names_male)
        else:
            first_name = random.choice(first_names_female)
        
        last_name = random.choice(last_names)
        name = f"Dr. {first_name} {last_name}"
        specialization = random.choice(specializations)
        phone = f"+98-21-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}"
        email = f"dr.{last_name.lower()}{random.randint(1, 99)}@hospital.ir"
        
        cursor.execute('''
            INSERT INTO doctors (name, specialization, phone, email)
            VALUES (?, ?, ?, ?)
        ''', (name, specialization, phone, email))
    
    conn.commit()
    conn.close()
    print(f"✓ {count} doctors added")

def populate_appointments(db_name, count=50):
    """Add appointments"""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # Get patient and doctor counts
    cursor.execute('SELECT COUNT(*) FROM patients')
    patient_count = cursor.fetchone()[0]
    cursor.execute('SELECT COUNT(*) FROM doctors')
    doctor_count = cursor.fetchone()[0]
    
    if patient_count == 0 or doctor_count == 0:
        print("Please add patients and doctors first")
        conn.close()
        return
    
    statuses = ['Scheduled', 'Confirmed', 'Completed', 'Cancelled']
    times = ['08:00', '09:00', '10:00', '11:00', '12:00', '14:00', '15:00', '16:00', '17:00']
    
    for i in range(count):
        patient_id = random.randint(1, patient_count)
        doctor_id = random.randint(1, doctor_count)
        
        # Random date within 60 days (past or future)
        days_offset = random.randint(-30, 30)
        appointment_date = (datetime.now() + timedelta(days=days_offset)).strftime('%Y-%m-%d')
        appointment_time = random.choice(times)
        status = random.choice(statuses)
        
        cursor.execute('''
            INSERT INTO appointments (patient_id, doctor_id, appointment_date, appointment_time, status)
            VALUES (?, ?, ?, ?, ?)
        ''', (patient_id, doctor_id, appointment_date, appointment_time, status))
    
    conn.commit()
    conn.close()
    print(f"✓ {count} appointments added")

def populate_medical_records(db_name, count=50):
    """Add medical records"""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # Get patient and doctor counts
    cursor.execute('SELECT COUNT(*) FROM patients')
    patient_count = cursor.fetchone()[0]
    cursor.execute('SELECT COUNT(*) FROM doctors')
    doctor_count = cursor.fetchone()[0]
    
    if patient_count == 0 or doctor_count == 0:
        print("Please add patients and doctors first")
        conn.close()
        return
    
    notes_templates = [
        'Patient is in good condition',
        'Follow-up required',
        'Complete rest recommended',
        'Appropriate diet prescribed',
        'Additional tests requested',
        'Patient referred to specialist',
        'Patient condition improving',
        'No hospitalization needed',
        'Vital signs stable',
        'Continue current medication'
    ]
    
    for i in range(count):
        patient_id = random.randint(1, patient_count)
        doctor_id = random.randint(1, doctor_count)
        diagnosis = random.choice(diagnoses)
        prescription = random.choice(prescriptions)
        notes = random.choice(notes_templates)
        
        # Random date within past 90 days
        days_offset = random.randint(-90, 0)
        record_date = (datetime.now() + timedelta(days=days_offset)).strftime('%Y-%m-%d')
        
        cursor.execute('''
            INSERT INTO medical_records (patient_id, doctor_id, diagnosis, prescription, notes, record_date)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (patient_id, doctor_id, diagnosis, prescription, notes, record_date))
    
    conn.commit()
    conn.close()
    print(f"✓ {count} medical records added")

def main():
    """Main execution"""
    databases = [
        'central_hospital.db',
        'city_hospital.db',
        'general_hospital.db'
    ]
    
    print("Starting to populate databases with Iranian names...\n")
    
    for db_name in databases:
        print(f"Processing: {db_name}")
        create_database(db_name)
        populate_patients(db_name, 50)
        populate_doctors(db_name, 20)
        populate_appointments(db_name, 50)
        populate_medical_records(db_name, 50)
        print(f"✓ {db_name} successfully populated\n")
    
    print("✓✓✓ All databases successfully populated!")
    print("\nTotal Statistics:")
    print("- 50 patients per hospital")
    print("- 20 doctors per hospital")
    print("- 50 appointments per hospital")
    print("- 50 medical records per hospital")

if __name__ == '__main__':
    main()
