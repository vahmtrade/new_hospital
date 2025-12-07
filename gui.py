import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from tkcalendar import DateEntry
from client import HospitalClient
from database import HospitalDatabase
import threading
import json
import re
from datetime import datetime

class HospitalManagementGUI:
    def __init__(self, root, is_master=False, local_port=5000, local_db='hospital.db', hospital_name='Hospital'):
        self.root = root
        self.is_master = is_master
        self.local_port = local_port
        self.local_db = local_db
        self.hospital_name = hospital_name
        
        # Initialize local database
        self.local_db_instance = HospitalDatabase(local_db, hospital_name)
        
        # Initialize clients for remote hospitals (if master)
        self.remote_clients = []
        
        self.root.title(f"{hospital_name} Management System {'(MASTER)' if is_master else ''}")
        self.root.geometry("1200x700")
        self.root.configure(bg='#f0f0f0')
        
        self.setup_ui()
    
    def validate_name(self, name):
        """Validate name - minimum 3 characters"""
        if len(name.strip()) < 3:
            return False, "Name must be at least 3 characters"
        return True, ""
    
    def validate_age(self, age):
        """Validate age - positive integer"""
        try:
            age_int = int(age)
            if age_int <= 0:
                return False, "Age must be a positive number"
            if age_int > 150:
                return False, "Age must be less than 150"
            return True, ""
        except ValueError:
            return False, "Age must be a valid number"
    
    def validate_phone(self, phone):
        """Validate phone - Iranian format"""
        if not phone or len(phone.strip()) == 0:
            return False, "Phone number is required"
        
        phone = phone.strip()
        
        # Accept formats: +98-XXX-XXX-XXXX or 09XXXXXXXXX
        pattern1 = r'^\+98-\d{2,3}-\d{3,4}-\d{4}$'
        pattern2 = r'^09\d{9}$'
        
        if re.match(pattern1, phone) or re.match(pattern2, phone):
            return True, ""
        
        return False, "Phone format: +98-XX-XXX-XXXX or 09XXXXXXXXX"
    
    def validate_diagnosis(self, diagnosis):
        """Validate diagnosis - minimum 3 characters"""
        if len(diagnosis.strip()) < 3:
            return False, "Diagnosis must be at least 3 characters"
        return True, ""
    
    def validate_email(self, email):
        """Validate email format"""
        if not email or len(email.strip()) == 0:
            return False, "Email is required"
        
        email = email.strip()
        
        # Check length
        if len(email) < 5:
            return False, "Email too short"
        if len(email) > 100:
            return False, "Email too long (max 100 characters)"
        
        # Check format
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, email):
            return False, "Invalid email format (example@domain.com)"
        
        # Check for valid domain
        if email.count('@') != 1:
            return False, "Email must contain exactly one @"
        
        return True, ""
    
    def validate_specialization(self, specialization):
        """Validate doctor specialization"""
        if not specialization or len(specialization.strip()) == 0:
            return False, "Specialization is required"
        
        specialization = specialization.strip()
        
        # Check length
        if len(specialization) < 3:
            return False, "Specialization must be at least 3 characters"
        if len(specialization) > 50:
            return False, "Specialization too long (max 50 characters)"
        
        # Check for valid characters (letters, spaces, hyphens)
        if not re.match(r'^[a-zA-Z\s\-]+$', specialization):
            return False, "Specialization can only contain letters, spaces, and hyphens"
        
        return True, ""
    
    def validate_date(self, date_str):
        """Validate appointment date (YYYY-MM-DD format)"""
        if not date_str or len(date_str.strip()) == 0:
            return False, "Date is required"
        
        date_str = date_str.strip()
        
        # Check format
        if not re.match(r'^\d{4}-\d{2}-\d{2}$', date_str):
            return False, "Date format must be YYYY-MM-DD"
        
        # Validate actual date
        try:
            from datetime import datetime
            year, month, day = map(int, date_str.split('-'))
            
            if year < 2000 or year > 2100:
                return False, "Year must be between 2000 and 2100"
            
            if month < 1 or month > 12:
                return False, "Month must be between 01 and 12"
            
            if day < 1 or day > 31:
                return False, "Day must be between 01 and 31"
            
            # Check if date is valid
            datetime(year, month, day)
            
            return True, ""
        except ValueError:
            return False, "Invalid date (e.g., 2024-02-30 doesn't exist)"
    
    def validate_time(self, time_str):
        """Validate appointment time (HH:MM format)"""
        if not time_str or len(time_str.strip()) == 0:
            return False, "Time is required"
        
        time_str = time_str.strip()
        
        # Check format
        if not re.match(r'^\d{2}:\d{2}$', time_str):
            return False, "Time format must be HH:MM (e.g., 09:30)"
        
        # Validate actual time
        try:
            hour, minute = map(int, time_str.split(':'))
            
            if hour < 0 or hour > 23:
                return False, "Hour must be between 00 and 23"
            
            if minute < 0 or minute > 59:
                return False, "Minute must be between 00 and 59"
            
            return True, ""
        except ValueError:
            return False, "Invalid time format"
    
    def add_remote_hospital(self, url):
        """Add a remote hospital connection (for master laptop)"""
        client = HospitalClient(url)
        if client.check_health():
            self.remote_clients.append(client)
            return True
        return False
    
    def get_hospital_prefix(self, hospital_name=None):
        """Get unique prefix for hospital to avoid ID conflicts"""
        if hospital_name is None:
            hospital_name = self.hospital_name
        
        # Create short prefix from hospital name
        if 'Central' in hospital_name:
            return 'CEN'
        elif 'City' in hospital_name:
            return 'CTY'
        elif 'General' in hospital_name:
            return 'GEN'
        else:
            # Generate prefix from first 3 letters
            return hospital_name[:3].upper()
    
    def setup_ui(self):
        # Title
        title_frame = tk.Frame(self.root, bg='#2c3e50', height=60)
        title_frame.pack(fill='x')
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame, text=f"{self.hospital_name} Management System", 
                              font=('Arial', 20, 'bold'), fg='white', bg='#2c3e50')
        title_label.pack(pady=15)
        
        if self.is_master:
            master_label = tk.Label(title_frame, text="MASTER NODE", 
                                   font=('Arial', 10, 'bold'), fg='#f39c12', bg='#2c3e50')
            master_label.pack()
        
        # Main container
        main_container = tk.Frame(self.root, bg='#f0f0f0')
        main_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Notebook for tabs
        self.notebook = ttk.Notebook(main_container)
        self.notebook.pack(fill='both', expand=True)
        
        # Create tabs
        self.create_patients_tab()
        self.create_doctors_tab()
        self.create_appointments_tab()
        self.create_medical_records_tab()
        
        if self.is_master:
            self.create_master_control_tab()
    
    def create_patients_tab(self):
        patients_frame = tk.Frame(self.notebook, bg='white')
        self.notebook.add(patients_frame, text='Patients')
        
        # Search frame
        search_frame = tk.Frame(patients_frame, bg='white')
        search_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(search_frame, text="Search:", font=('Arial', 10), bg='white').pack(side='left', padx=5)
        self.patient_search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=self.patient_search_var, width=30)
        search_entry.pack(side='left', padx=5)
        
        tk.Button(search_frame, text="Search", command=self.search_patients, 
                 bg='#3498db', fg='white', font=('Arial', 10)).pack(side='left', padx=5)
        tk.Button(search_frame, text="Refresh", command=self.load_patients, 
                 bg='#2ecc71', fg='white', font=('Arial', 10)).pack(side='left', padx=5)
        tk.Button(search_frame, text="Add Patient", command=self.add_patient_dialog, 
                 bg='#e74c3c', fg='white', font=('Arial', 10)).pack(side='left', padx=5)
        tk.Button(search_frame, text="Delete Selected", command=self.delete_patient, 
                 bg='#c0392b', fg='white', font=('Arial', 10)).pack(side='left', padx=5)
        
        # Table frame
        table_frame = tk.Frame(patients_frame, bg='white')
        table_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Scrollbars
        v_scrollbar = tk.Scrollbar(table_frame)
        v_scrollbar.pack(side='right', fill='y')
        h_scrollbar = tk.Scrollbar(table_frame, orient='horizontal')
        h_scrollbar.pack(side='bottom', fill='x')
        
        # Treeview
        columns = ('ID', 'Name', 'Age', 'Gender', 'Phone', 'Address', 'Hospital')
        self.patients_tree = ttk.Treeview(table_frame, columns=columns, show='headings',
                                         yscrollcommand=v_scrollbar.set,
                                         xscrollcommand=h_scrollbar.set)
        
        for col in columns:
            self.patients_tree.heading(col, text=col)
            self.patients_tree.column(col, width=120)
        
        self.patients_tree.pack(fill='both', expand=True)
        v_scrollbar.config(command=self.patients_tree.yview)
        h_scrollbar.config(command=self.patients_tree.xview)
        
        # Bind double-click event
        self.patients_tree.bind('<Double-1>', self.update_patient_dialog)
        
        self.load_patients()
    
    def create_doctors_tab(self):
        doctors_frame = tk.Frame(self.notebook, bg='white')
        self.notebook.add(doctors_frame, text='Doctors')
        
        # Search frame
        search_frame = tk.Frame(doctors_frame, bg='white')
        search_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(search_frame, text="Search:", font=('Arial', 10), bg='white').pack(side='left', padx=5)
        self.doctor_search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=self.doctor_search_var, width=30)
        search_entry.pack(side='left', padx=5)
        
        tk.Button(search_frame, text="Search", command=self.search_doctors, 
                 bg='#3498db', fg='white', font=('Arial', 10)).pack(side='left', padx=5)
        tk.Button(search_frame, text="Refresh", command=self.load_doctors, 
                 bg='#2ecc71', fg='white', font=('Arial', 10)).pack(side='left', padx=5)
        tk.Button(search_frame, text="Add Doctor", command=self.add_doctor_dialog, 
                 bg='#e74c3c', fg='white', font=('Arial', 10)).pack(side='left', padx=5)
        tk.Button(search_frame, text="Delete Selected", command=self.delete_doctor, 
                 bg='#c0392b', fg='white', font=('Arial', 10)).pack(side='left', padx=5)
        
        # Table frame
        table_frame = tk.Frame(doctors_frame, bg='white')
        table_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        v_scrollbar = tk.Scrollbar(table_frame)
        v_scrollbar.pack(side='right', fill='y')
        h_scrollbar = tk.Scrollbar(table_frame, orient='horizontal')
        h_scrollbar.pack(side='bottom', fill='x')
        
        columns = ('ID', 'Name', 'Specialization', 'Phone', 'Email', 'Hospital')
        self.doctors_tree = ttk.Treeview(table_frame, columns=columns, show='headings',
                                        yscrollcommand=v_scrollbar.set,
                                        xscrollcommand=h_scrollbar.set)
        
        for col in columns:
            self.doctors_tree.heading(col, text=col)
            self.doctors_tree.column(col, width=150)
        
        self.doctors_tree.pack(fill='both', expand=True)
        v_scrollbar.config(command=self.doctors_tree.yview)
        h_scrollbar.config(command=self.doctors_tree.xview)
        
        # Bind double-click event
        self.doctors_tree.bind('<Double-1>', self.update_doctor_dialog)
        
        self.load_doctors()

    def create_appointments_tab(self):
        appointments_frame = tk.Frame(self.notebook, bg='white')
        self.notebook.add(appointments_frame, text='Appointments')
        
        # Control frame
        control_frame = tk.Frame(appointments_frame, bg='white')
        control_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Button(control_frame, text="Refresh", command=self.load_appointments, 
                 bg='#2ecc71', fg='white', font=('Arial', 10)).pack(side='left', padx=5)
        tk.Button(control_frame, text="Add Appointment", command=self.add_appointment_dialog, 
                 bg='#e74c3c', fg='white', font=('Arial', 10)).pack(side='left', padx=5)
        tk.Button(control_frame, text="Delete Selected", command=self.delete_appointment, 
                 bg='#c0392b', fg='white', font=('Arial', 10)).pack(side='left', padx=5)
        
        # Table frame
        table_frame = tk.Frame(appointments_frame, bg='white')
        table_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        v_scrollbar = tk.Scrollbar(table_frame)
        v_scrollbar.pack(side='right', fill='y')
        h_scrollbar = tk.Scrollbar(table_frame, orient='horizontal')
        h_scrollbar.pack(side='bottom', fill='x')
        
        columns = ('ID', 'Patient ID', 'Doctor ID', 'Date', 'Time', 'Status', 'Hospital')
        self.appointments_tree = ttk.Treeview(table_frame, columns=columns, show='headings',
                                             yscrollcommand=v_scrollbar.set,
                                             xscrollcommand=h_scrollbar.set)
        
        for col in columns:
            self.appointments_tree.heading(col, text=col)
            self.appointments_tree.column(col, width=120)
        
        self.appointments_tree.pack(fill='both', expand=True)
        v_scrollbar.config(command=self.appointments_tree.yview)
        h_scrollbar.config(command=self.appointments_tree.xview)
        
        # Bind double-click event
        self.appointments_tree.bind('<Double-1>', self.update_appointment_dialog)
        
        self.load_appointments()
    
    def create_medical_records_tab(self):
        records_frame = tk.Frame(self.notebook, bg='white')
        self.notebook.add(records_frame, text='Medical Records')
        
        # Control frame
        control_frame = tk.Frame(records_frame, bg='white')
        control_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Button(control_frame, text="Refresh", command=self.load_medical_records, 
                 bg='#2ecc71', fg='white', font=('Arial', 10)).pack(side='left', padx=5)
        tk.Button(control_frame, text="Add Record", command=self.add_medical_record_dialog, 
                 bg='#e74c3c', fg='white', font=('Arial', 10)).pack(side='left', padx=5)
        tk.Button(control_frame, text="Delete Selected", command=self.delete_medical_record, 
                 bg='#c0392b', fg='white', font=('Arial', 10)).pack(side='left', padx=5)
        
        # Table frame
        table_frame = tk.Frame(records_frame, bg='white')
        table_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        v_scrollbar = tk.Scrollbar(table_frame)
        v_scrollbar.pack(side='right', fill='y')
        h_scrollbar = tk.Scrollbar(table_frame, orient='horizontal')
        h_scrollbar.pack(side='bottom', fill='x')
        
        columns = ('ID', 'Patient ID', 'Doctor ID', 'Diagnosis', 'Prescription', 'Date', 'Hospital')
        self.records_tree = ttk.Treeview(table_frame, columns=columns, show='headings',
                                        yscrollcommand=v_scrollbar.set,
                                        xscrollcommand=h_scrollbar.set)
        
        for col in columns:
            self.records_tree.heading(col, text=col)
            self.records_tree.column(col, width=150)
        
        self.records_tree.pack(fill='both', expand=True)
        v_scrollbar.config(command=self.records_tree.yview)
        h_scrollbar.config(command=self.records_tree.xview)
        
        # Bind double-click event
        self.records_tree.bind('<Double-1>', self.update_medical_record_dialog)
        
        self.load_medical_records()
    
    def create_master_control_tab(self):
        master_frame = tk.Frame(self.notebook, bg='white')
        self.notebook.add(master_frame, text='Master Control')
        
        tk.Label(master_frame, text="Connected Hospitals", 
                font=('Arial', 14, 'bold'), bg='white').pack(pady=10)
        
        # Connection status
        status_frame = tk.Frame(master_frame, bg='white')
        status_frame.pack(fill='x', padx=20, pady=10)
        
        self.status_text = scrolledtext.ScrolledText(status_frame, height=10, width=80)
        self.status_text.pack()
        
        # Add hospital connection
        add_frame = tk.Frame(master_frame, bg='white')
        add_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(add_frame, text="Add Hospital URL:", font=('Arial', 10), bg='white').pack(side='left', padx=5)
        self.hospital_url_var = tk.StringVar()
        tk.Entry(add_frame, textvariable=self.hospital_url_var, width=40).pack(side='left', padx=5)
        tk.Button(add_frame, text="Connect", command=self.connect_hospital, 
                 bg='#3498db', fg='white', font=('Arial', 10)).pack(side='left', padx=5)
        
        tk.Button(master_frame, text="Refresh All Data", command=self.refresh_all_data, 
                 bg='#2ecc71', fg='white', font=('Arial', 12, 'bold')).pack(pady=20)
        
        self.update_connection_status()
    
    def connect_hospital(self):
        url = self.hospital_url_var.get().strip()
        if url:
            if self.add_remote_hospital(url):
                messagebox.showinfo("Success", f"Connected to hospital at {url}")
                self.update_connection_status()
                self.hospital_url_var.set('')
            else:
                messagebox.showerror("Error", f"Failed to connect to {url}")
    
    def update_connection_status(self):
        self.status_text.delete(1.0, tk.END)
        self.status_text.insert(tk.END, f"Local Hospital: {self.hospital_name} (localhost:{self.local_port})\n\n")
        
        if self.remote_clients:
            self.status_text.insert(tk.END, "Connected Remote Hospitals:\n")
            for i, client in enumerate(self.remote_clients, 1):
                health = client.check_health()
                if health:
                    self.status_text.insert(tk.END, f"{i}. {health['hospital']} - {client.base_url} [ONLINE]\n")
                else:
                    self.status_text.insert(tk.END, f"{i}. {client.base_url} [OFFLINE]\n")
        else:
            self.status_text.insert(tk.END, "No remote hospitals connected.\n")
    
    def load_patients(self):
        for item in self.patients_tree.get_children():
            self.patients_tree.delete(item)
        
        # Load local patients
        local_patients = self.local_db_instance.get_all('patients')
        for patient in local_patients:
            patient_id = f"{self.get_hospital_prefix()}-{patient.get('patient_id', '')}"
            self.patients_tree.insert('', 'end', values=(
                patient_id,
                patient.get('name', ''),
                patient.get('age', ''),
                patient.get('gender', ''),
                patient.get('phone', ''),
                patient.get('address', ''),
                self.hospital_name
            ))
        
        # Load remote patients if master
        if self.is_master:
            for client in self.remote_clients:
                remote_patients = client.get_patients()
                health = client.check_health()
                hospital_name = health['hospital'] if health else 'Unknown'
                hospital_prefix = self.get_hospital_prefix(hospital_name)
                for patient in remote_patients:
                    patient_id = f"{hospital_prefix}-{patient.get('patient_id', '')}"
                    self.patients_tree.insert('', 'end', values=(
                        patient_id,
                        patient.get('name', ''),
                        patient.get('age', ''),
                        patient.get('gender', ''),
                        patient.get('phone', ''),
                        patient.get('address', ''),
                        hospital_name
                    ))
    
    def search_patients(self):
        search_term = self.patient_search_var.get()
        for item in self.patients_tree.get_children():
            self.patients_tree.delete(item)
        
        # Search local
        local_patients = self.local_db_instance.search('patients', search_term)
        for patient in local_patients:
            patient_id = f"{self.get_hospital_prefix()}-{patient.get('patient_id', '')}"
            self.patients_tree.insert('', 'end', values=(
                patient_id,
                patient.get('name', ''),
                patient.get('age', ''),
                patient.get('gender', ''),
                patient.get('phone', ''),
                patient.get('address', ''),
                self.hospital_name
            ))
        
        # Search remote if master
        if self.is_master:
            for client in self.remote_clients:
                remote_patients = client.get_patients(search_term)
                health = client.check_health()
                hospital_name = health['hospital'] if health else 'Unknown'
                hospital_prefix = self.get_hospital_prefix(hospital_name)
                for patient in remote_patients:
                    patient_id = f"{hospital_prefix}-{patient.get('patient_id', '')}"
                    self.patients_tree.insert('', 'end', values=(
                        patient_id,
                        patient.get('name', ''),
                        patient.get('age', ''),
                        patient.get('gender', ''),
                        patient.get('phone', ''),
                        patient.get('address', ''),
                        hospital_name
                    ))
    
    def load_doctors(self):
        for item in self.doctors_tree.get_children():
            self.doctors_tree.delete(item)
        
        local_doctors = self.local_db_instance.get_all('doctors')
        for doctor in local_doctors:
            doctor_id = f"{self.get_hospital_prefix()}-{doctor.get('doctor_id', '')}"
            self.doctors_tree.insert('', 'end', values=(
                doctor_id,
                doctor.get('name', ''),
                doctor.get('specialization', ''),
                doctor.get('phone', ''),
                doctor.get('email', ''),
                self.hospital_name
            ))
        
        if self.is_master:
            for client in self.remote_clients:
                remote_doctors = client.get_doctors()
                health = client.check_health()
                hospital_name = health['hospital'] if health else 'Unknown'
                hospital_prefix = self.get_hospital_prefix(hospital_name)
                for doctor in remote_doctors:
                    doctor_id = f"{hospital_prefix}-{doctor.get('doctor_id', '')}"
                    self.doctors_tree.insert('', 'end', values=(
                        doctor_id,
                        doctor.get('name', ''),
                        doctor.get('specialization', ''),
                        doctor.get('phone', ''),
                        doctor.get('email', ''),
                        hospital_name
                    ))
    
    def search_doctors(self):
        search_term = self.doctor_search_var.get()
        for item in self.doctors_tree.get_children():
            self.doctors_tree.delete(item)
        
        local_doctors = self.local_db_instance.search('doctors', search_term)
        for doctor in local_doctors:
            doctor_id = f"{self.get_hospital_prefix()}-{doctor.get('doctor_id', '')}"
            self.doctors_tree.insert('', 'end', values=(
                doctor_id,
                doctor.get('name', ''),
                doctor.get('specialization', ''),
                doctor.get('phone', ''),
                doctor.get('email', ''),
                self.hospital_name
            ))
        
        if self.is_master:
            for client in self.remote_clients:
                remote_doctors = client.get_doctors(search_term)
                health = client.check_health()
                hospital_name = health['hospital'] if health else 'Unknown'
                hospital_prefix = self.get_hospital_prefix(hospital_name)
                for doctor in remote_doctors:
                    doctor_id = f"{hospital_prefix}-{doctor.get('doctor_id', '')}"
                    self.doctors_tree.insert('', 'end', values=(
                        doctor_id,
                        doctor.get('name', ''),
                        doctor.get('specialization', ''),
                        doctor.get('phone', ''),
                        doctor.get('email', ''),
                        hospital_name
                    ))

    def load_appointments(self):
        for item in self.appointments_tree.get_children():
            self.appointments_tree.delete(item)
        
        local_appointments = self.local_db_instance.get_all('appointments')
        hospital_prefix = self.get_hospital_prefix()
        for appt in local_appointments:
            self.appointments_tree.insert('', 'end', values=(
                f"{hospital_prefix}-{appt.get('appointment_id', '')}",
                f"{hospital_prefix}-{appt.get('patient_id', '')}",
                f"{hospital_prefix}-{appt.get('doctor_id', '')}",
                appt.get('appointment_date', ''),
                appt.get('appointment_time', ''),
                appt.get('status', ''),
                self.hospital_name
            ))
        
        if self.is_master:
            for client in self.remote_clients:
                remote_appointments = client.get_appointments()
                health = client.check_health()
                hospital_name = health['hospital'] if health else 'Unknown'
                hospital_prefix = self.get_hospital_prefix(hospital_name)
                for appt in remote_appointments:
                    self.appointments_tree.insert('', 'end', values=(
                        f"{hospital_prefix}-{appt.get('appointment_id', '')}",
                        f"{hospital_prefix}-{appt.get('patient_id', '')}",
                        f"{hospital_prefix}-{appt.get('doctor_id', '')}",
                        appt.get('appointment_date', ''),
                        appt.get('appointment_time', ''),
                        appt.get('status', ''),
                        hospital_name
                    ))
    
    def load_medical_records(self):
        for item in self.records_tree.get_children():
            self.records_tree.delete(item)
        
        local_records = self.local_db_instance.get_all('medical_records')
        hospital_prefix = self.get_hospital_prefix()
        for record in local_records:
            self.records_tree.insert('', 'end', values=(
                f"{hospital_prefix}-{record.get('record_id', '')}",
                f"{hospital_prefix}-{record.get('patient_id', '')}",
                f"{hospital_prefix}-{record.get('doctor_id', '')}",
                record.get('diagnosis', ''),
                record.get('prescription', ''),
                record.get('record_date', ''),
                self.hospital_name
            ))
        
        if self.is_master:
            for client in self.remote_clients:
                remote_records = client.get_medical_records()
                health = client.check_health()
                hospital_name = health['hospital'] if health else 'Unknown'
                hospital_prefix = self.get_hospital_prefix(hospital_name)
                for record in remote_records:
                    self.records_tree.insert('', 'end', values=(
                        f"{hospital_prefix}-{record.get('record_id', '')}",
                        f"{hospital_prefix}-{record.get('patient_id', '')}",
                        f"{hospital_prefix}-{record.get('doctor_id', '')}",
                        record.get('diagnosis', ''),
                        record.get('prescription', ''),
                        record.get('record_date', ''),
                        hospital_name
                    ))
    
    def refresh_all_data(self):
        self.load_patients()
        self.load_doctors()
        self.load_appointments()
        self.load_medical_records()
        self.update_connection_status()
        messagebox.showinfo("Success", "All data refreshed!")
    
    def add_patient_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Patient")
        dialog.geometry("450x450")
        dialog.configure(bg='white')
        
        tk.Label(dialog, text="Patient Information", font=('Arial', 14, 'bold'), bg='white').pack(pady=10)
        
        form_frame = tk.Frame(dialog, bg='white')
        form_frame.pack(padx=20, pady=10)
        
        fields = {}
        error_labels = {}
        
        # Name
        tk.Label(form_frame, text="Name:", font=('Arial', 10), bg='white').grid(row=0, column=0, sticky='w', pady=(5,0))
        name_entry = tk.Entry(form_frame, width=30)
        name_entry.grid(row=0, column=1, pady=(5,0), padx=10)
        fields['name'] = name_entry
        name_error = tk.Label(form_frame, text="", font=('Arial', 8), fg='red', bg='white')
        name_error.grid(row=1, column=1, sticky='w', padx=10)
        error_labels['name'] = name_error
        
        # Age
        tk.Label(form_frame, text="Age:", font=('Arial', 10), bg='white').grid(row=2, column=0, sticky='w', pady=(5,0))
        age_entry = tk.Entry(form_frame, width=30)
        age_entry.grid(row=2, column=1, pady=(5,0), padx=10)
        fields['age'] = age_entry
        age_error = tk.Label(form_frame, text="", font=('Arial', 8), fg='red', bg='white')
        age_error.grid(row=3, column=1, sticky='w', padx=10)
        error_labels['age'] = age_error
        
        # Gender - Dropdown
        tk.Label(form_frame, text="Gender:", font=('Arial', 10), bg='white').grid(row=4, column=0, sticky='w', pady=(5,0))
        gender_combo = ttk.Combobox(form_frame, width=28, state='readonly')
        gender_combo['values'] = ('Male', 'Female')
        gender_combo.grid(row=4, column=1, pady=(5,0), padx=10)
        fields['gender'] = gender_combo
        gender_error = tk.Label(form_frame, text="", font=('Arial', 8), fg='red', bg='white')
        gender_error.grid(row=5, column=1, sticky='w', padx=10)
        error_labels['gender'] = gender_error
        
        # Phone
        tk.Label(form_frame, text="Phone:", font=('Arial', 10), bg='white').grid(row=6, column=0, sticky='w', pady=(5,0))
        phone_entry = tk.Entry(form_frame, width=30)
        phone_entry.grid(row=6, column=1, pady=(5,0), padx=10)
        fields['phone'] = phone_entry
        phone_error = tk.Label(form_frame, text="", font=('Arial', 8), fg='red', bg='white')
        phone_error.grid(row=7, column=1, sticky='w', padx=10)
        error_labels['phone'] = phone_error
        
        # Address
        tk.Label(form_frame, text="Address:", font=('Arial', 10), bg='white').grid(row=8, column=0, sticky='w', pady=(5,0))
        address_entry = tk.Entry(form_frame, width=30)
        address_entry.grid(row=8, column=1, pady=(5,0), padx=10)
        fields['address'] = address_entry
        address_error = tk.Label(form_frame, text="", font=('Arial', 8), fg='red', bg='white')
        address_error.grid(row=9, column=1, sticky='w', padx=10)
        error_labels['address'] = address_error
        
        def clear_errors():
            for error_label in error_labels.values():
                error_label.config(text="")
        
        def save_patient():
            clear_errors()
            data = {key: entry.get() for key, entry in fields.items()}
            has_error = False
            
            # Validate name
            valid, msg = self.validate_name(data.get('name', ''))
            if not valid:
                error_labels['name'].config(text=msg)
                has_error = True
            
            # Validate age
            if data.get('age'):
                valid, msg = self.validate_age(data['age'])
                if not valid:
                    error_labels['age'].config(text=msg)
                    has_error = True
            
            # Validate phone
            if data.get('phone'):
                valid, msg = self.validate_phone(data['phone'])
                if not valid:
                    error_labels['phone'].config(text=msg)
                    has_error = True
            
            if has_error:
                return
            
            self.local_db_instance.insert('patients', data)
            messagebox.showinfo("Success", "Patient added successfully!")
            dialog.destroy()
            self.load_patients()
        
        tk.Button(dialog, text="Save", command=save_patient, 
                 bg='#2ecc71', fg='white', font=('Arial', 10, 'bold')).pack(pady=20)
    
    def add_doctor_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Doctor")
        dialog.geometry("450x400")
        dialog.configure(bg='white')
        
        tk.Label(dialog, text="Doctor Information", font=('Arial', 14, 'bold'), bg='white').pack(pady=10)
        
        form_frame = tk.Frame(dialog, bg='white')
        form_frame.pack(padx=20, pady=10)
        
        fields = {}
        error_labels = {}
        labels = ['Name', 'Specialization', 'Phone', 'Email']
        
        for i, label in enumerate(labels):
            tk.Label(form_frame, text=f"{label}:", font=('Arial', 10), bg='white').grid(row=i*2, column=0, sticky='w', pady=(5,0))
            entry = tk.Entry(form_frame, width=30)
            entry.grid(row=i*2, column=1, pady=(5,0), padx=10)
            fields[label.lower()] = entry
            
            # Error label
            error_label = tk.Label(form_frame, text="", font=('Arial', 8), fg='red', bg='white')
            error_label.grid(row=i*2+1, column=1, sticky='w', padx=10)
            error_labels[label.lower()] = error_label
        
        def clear_errors():
            for error_label in error_labels.values():
                error_label.config(text="")
        
        def save_doctor():
            clear_errors()
            data = {key: entry.get() for key, entry in fields.items()}
            has_error = False
            
            # Validate name (required)
            valid, msg = self.validate_name(data.get('name', ''))
            if not valid:
                error_labels['name'].config(text=msg)
                has_error = True
            
            # Validate specialization (required)
            valid, msg = self.validate_specialization(data.get('specialization', ''))
            if not valid:
                error_labels['specialization'].config(text=msg)
                has_error = True
            
            # Validate phone (required)
            valid, msg = self.validate_phone(data.get('phone', ''))
            if not valid:
                error_labels['phone'].config(text=msg)
                has_error = True
            
            # Validate email (required)
            valid, msg = self.validate_email(data.get('email', ''))
            if not valid:
                error_labels['email'].config(text=msg)
                has_error = True
            
            if has_error:
                return
            
            self.local_db_instance.insert('doctors', data)
            messagebox.showinfo("Success", "Doctor added successfully!")
            dialog.destroy()
            self.load_doctors()
        
        tk.Button(dialog, text="Save", command=save_doctor, 
                 bg='#2ecc71', fg='white', font=('Arial', 10, 'bold')).pack(pady=20)
    
    def add_appointment_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Appointment")
        dialog.geometry("550x450")
        dialog.configure(bg='white')
        
        tk.Label(dialog, text="Appointment Information", font=('Arial', 14, 'bold'), bg='white').pack(pady=10)
        
        form_frame = tk.Frame(dialog, bg='white')
        form_frame.pack(padx=20, pady=10)
        
        # Get all patients and doctors
        all_patients = self.local_db_instance.get_all('patients')
        all_doctors = self.local_db_instance.get_all('doctors')
        
        # Create patient list with ID and Name
        patient_list = [f"{p['patient_id']} - {p['name']}" for p in all_patients]
        doctor_list = [f"{d['doctor_id']} - {d['name']} ({d['specialization']})" for d in all_doctors]
        
        # Patient selection with search
        tk.Label(form_frame, text="Patient:", font=('Arial', 10), bg='white').grid(row=0, column=0, sticky='w', pady=5)
        patient_search_var = tk.StringVar()
        patient_combo = ttk.Combobox(form_frame, textvariable=patient_search_var, width=40)
        patient_combo['values'] = patient_list
        patient_combo.grid(row=0, column=1, pady=5, padx=10, columnspan=2)
        
        # Filter patients as user types
        def filter_patients(event):
            search_term = patient_search_var.get().lower()
            if search_term:
                filtered = [p for p in patient_list if search_term in p.lower()]
                patient_combo['values'] = filtered
            else:
                patient_combo['values'] = patient_list
        
        patient_combo.bind('<KeyRelease>', filter_patients)
        
        # Doctor selection with search
        tk.Label(form_frame, text="Doctor:", font=('Arial', 10), bg='white').grid(row=1, column=0, sticky='w', pady=5)
        doctor_search_var = tk.StringVar()
        doctor_combo = ttk.Combobox(form_frame, textvariable=doctor_search_var, width=40)
        doctor_combo['values'] = doctor_list
        doctor_combo.grid(row=1, column=1, pady=5, padx=10, columnspan=2)
        
        # Filter doctors as user types
        def filter_doctors(event):
            search_term = doctor_search_var.get().lower()
            if search_term:
                filtered = [d for d in doctor_list if search_term in d.lower()]
                doctor_combo['values'] = filtered
            else:
                doctor_combo['values'] = doctor_list
        
        doctor_combo.bind('<KeyRelease>', filter_doctors)
        
        # Appointment Date with Calendar
        tk.Label(form_frame, text="Date:", font=('Arial', 10), bg='white').grid(row=2, column=0, sticky='w', pady=5)
        date_entry = DateEntry(form_frame, width=39, background='darkblue',
                              foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        date_entry.grid(row=2, column=1, pady=5, padx=10, columnspan=2)
        
        # Appointment Time
        tk.Label(form_frame, text="Time (HH:MM):", font=('Arial', 10), bg='white').grid(row=3, column=0, sticky='w', pady=5)
        time_entry = tk.Entry(form_frame, width=42)
        time_entry.grid(row=3, column=1, pady=5, padx=10, columnspan=2)
        
        # Status
        tk.Label(form_frame, text="Status:", font=('Arial', 10), bg='white').grid(row=4, column=0, sticky='w', pady=5)
        status_combo = ttk.Combobox(form_frame, width=39, state='readonly')
        status_combo['values'] = ('Scheduled', 'Completed', 'Cancelled', 'No-Show')
        status_combo.set('Scheduled')
        status_combo.grid(row=4, column=1, pady=5, padx=10, columnspan=2)
        
        # Error labels
        error_label = tk.Label(form_frame, text="", font=('Arial', 9), fg='red', bg='white')
        error_label.grid(row=5, column=0, columnspan=3, pady=5)
        
        def save_appointment():
            error_label.config(text="")
            
            # Extract patient ID from selection
            patient_selection = patient_search_var.get().strip()
            doctor_selection = doctor_search_var.get().strip()
            
            # Validate patient selection - must be from dropdown list
            if not patient_selection:
                error_label.config(text="Please select a patient!")
                return
            
            if patient_selection not in patient_list:
                error_label.config(text="Please select a valid patient from the list!")
                patient_search_var.set('')
                return
            
            # Validate doctor selection - must be from dropdown list
            if not doctor_selection:
                error_label.config(text="Please select a doctor!")
                return
            
            if doctor_selection not in doctor_list:
                error_label.config(text="Please select a valid doctor from the list!")
                doctor_search_var.set('')
                return
            
            # Extract IDs (format: "ID - Name")
            try:
                patient_id = patient_selection.split(' - ')[0].strip()
                doctor_id = doctor_selection.split(' - ')[0].strip()
            except:
                error_label.config(text="Invalid patient or doctor selection!")
                return
            
            # Get date from calendar widget
            date_value = date_entry.get_date().strftime('%Y-%m-%d')
            valid, msg = self.validate_date(date_value)
            if not valid:
                error_label.config(text=f"Date error: {msg}")
                return
            
            # Validate time
            time_value = time_entry.get()
            valid, msg = self.validate_time(time_value)
            if not valid:
                error_label.config(text=f"Time error: {msg}")
                return
            
            data = {
                'patient_id': patient_id,
                'doctor_id': doctor_id,
                'appointment_date': date_value,
                'appointment_time': time_value,
                'status': status_combo.get()
            }
            
            self.local_db_instance.insert('appointments', data)
            messagebox.showinfo("Success", "Appointment added successfully!")
            dialog.destroy()
            self.load_appointments()
        
        tk.Button(dialog, text="Save", command=save_appointment, 
                 bg='#2ecc71', fg='white', font=('Arial', 10, 'bold')).pack(pady=20)
    
    def add_medical_record_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Medical Record")
        dialog.geometry("550x650")
        dialog.configure(bg='white')
        
        tk.Label(dialog, text="Medical Record Information", font=('Arial', 14, 'bold'), bg='white').pack(pady=10)
        
        form_frame = tk.Frame(dialog, bg='white')
        form_frame.pack(padx=20, pady=10)
        
        # Get all patients and doctors
        all_patients = self.local_db_instance.get_all('patients')
        all_doctors = self.local_db_instance.get_all('doctors')
        
        # Create patient list with ID and Name
        patient_list = [f"{p['patient_id']} - {p['name']}" for p in all_patients]
        doctor_list = [f"{d['doctor_id']} - {d['name']} ({d['specialization']})" for d in all_doctors]
        
        # Patient selection with search
        tk.Label(form_frame, text="Patient:", font=('Arial', 10), bg='white').grid(row=0, column=0, sticky='w', pady=(5,0))
        patient_search_var = tk.StringVar()
        patient_combo = ttk.Combobox(form_frame, textvariable=patient_search_var, width=40)
        patient_combo['values'] = patient_list
        patient_combo.grid(row=0, column=1, pady=(5,0), padx=10)
        patient_id_error = tk.Label(form_frame, text="", font=('Arial', 8), fg='red', bg='white')
        patient_id_error.grid(row=1, column=1, sticky='w', padx=10)
        
        # Filter patients as user types
        def filter_patients(event):
            search_term = patient_search_var.get().lower()
            if search_term:
                filtered = [p for p in patient_list if search_term in p.lower()]
                patient_combo['values'] = filtered
            else:
                patient_combo['values'] = patient_list
        
        patient_combo.bind('<KeyRelease>', filter_patients)
        
        # Doctor selection with search
        tk.Label(form_frame, text="Doctor:", font=('Arial', 10), bg='white').grid(row=2, column=0, sticky='w', pady=(5,0))
        doctor_search_var = tk.StringVar()
        doctor_combo = ttk.Combobox(form_frame, textvariable=doctor_search_var, width=40)
        doctor_combo['values'] = doctor_list
        doctor_combo.grid(row=2, column=1, pady=(5,0), padx=10)
        doctor_id_error = tk.Label(form_frame, text="", font=('Arial', 8), fg='red', bg='white')
        doctor_id_error.grid(row=3, column=1, sticky='w', padx=10)
        
        # Filter doctors as user types
        def filter_doctors(event):
            search_term = doctor_search_var.get().lower()
            if search_term:
                filtered = [d for d in doctor_list if search_term in d.lower()]
                doctor_combo['values'] = filtered
            else:
                doctor_combo['values'] = doctor_list
        
        doctor_combo.bind('<KeyRelease>', filter_doctors)
        
        # Diagnosis
        tk.Label(form_frame, text="Diagnosis:", font=('Arial', 10), bg='white').grid(row=4, column=0, sticky='w', pady=(5,0))
        diagnosis_entry = tk.Entry(form_frame, width=30)
        diagnosis_entry.grid(row=4, column=1, pady=(5,0), padx=10)
        diagnosis_error = tk.Label(form_frame, text="", font=('Arial', 8), fg='red', bg='white')
        diagnosis_error.grid(row=5, column=1, sticky='w', padx=10)
        
        # Prescription
        tk.Label(form_frame, text="Prescription:", font=('Arial', 10), bg='white').grid(row=6, column=0, sticky='w', pady=(5,0))
        prescription_entry = tk.Entry(form_frame, width=30)
        prescription_entry.grid(row=6, column=1, pady=(5,0), padx=10)
        prescription_error = tk.Label(form_frame, text="", font=('Arial', 8), fg='red', bg='white')
        prescription_error.grid(row=7, column=1, sticky='w', padx=10)
        
        # Notes
        tk.Label(form_frame, text="Notes:", font=('Arial', 10), bg='white').grid(row=8, column=0, sticky='nw', pady=(5,0))
        notes_text = tk.Text(form_frame, width=30, height=5)
        notes_text.grid(row=8, column=1, pady=(5,0), padx=10)
        
        # Record Date with Calendar
        tk.Label(form_frame, text="Record Date:", font=('Arial', 10), bg='white').grid(row=9, column=0, sticky='w', pady=(5,0))
        date_entry = DateEntry(form_frame, width=27, background='darkblue',
                              foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        date_entry.grid(row=9, column=1, pady=(5,0), padx=10)
        date_error = tk.Label(form_frame, text="", font=('Arial', 8), fg='red', bg='white')
        date_error.grid(row=10, column=1, sticky='w', padx=10)
        
        def clear_errors():
            patient_id_error.config(text="")
            doctor_id_error.config(text="")
            diagnosis_error.config(text="")
            prescription_error.config(text="")
            date_error.config(text="")
        
        def save_record():
            clear_errors()
            
            # Extract patient ID from selection
            patient_selection = patient_search_var.get()
            doctor_selection = doctor_search_var.get()
            
            has_error = False
            
            if not patient_selection:
                patient_id_error.config(text="Patient is required")
                has_error = True
            
            if not doctor_selection:
                doctor_id_error.config(text="Doctor is required")
                has_error = True
            
            if has_error:
                return
            
            # Extract IDs (format: "ID - Name")
            try:
                patient_id = patient_selection.split(' - ')[0].strip()
                doctor_id = doctor_selection.split(' - ')[0].strip()
            except:
                patient_id_error.config(text="Invalid selection!")
                return
            
            data = {
                'patient_id': patient_id,
                'doctor_id': doctor_id,
                'diagnosis': diagnosis_entry.get(),
                'prescription': prescription_entry.get(),
                'notes': notes_text.get(1.0, tk.END).strip(),
                'record_date': date_entry.get_date().strftime('%Y-%m-%d')
            }
            
            has_error = False
            
            # Validate diagnosis
            if data.get('diagnosis'):
                valid, msg = self.validate_diagnosis(data['diagnosis'])
                if not valid:
                    diagnosis_error.config(text=msg)
                    has_error = True
            
            # Validate prescription
            if data.get('prescription'):
                valid, msg = self.validate_name(data['prescription'])
                if not valid:
                    prescription_error.config(text="Minimum 3 characters")
                    has_error = True
            
            if has_error:
                return
            
            self.local_db_instance.insert('medical_records', data)
            messagebox.showinfo("Success", "Medical record added successfully!")
            dialog.destroy()
            self.load_medical_records()
        
        tk.Button(dialog, text="Save", command=save_record, 
                 bg='#2ecc71', fg='white', font=('Arial', 10, 'bold')).pack(pady=20)
    
    def delete_patient(self):
        selected = self.patients_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a patient to delete!")
            return
        
        item = self.patients_tree.item(selected[0])
        values = item['values']
        patient_id_with_prefix = values[0]
        patient_name = values[1]
        hospital = values[6]
        
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete patient '{patient_name}' (ID: {patient_id_with_prefix})?"):
            if hospital == self.hospital_name:
                # Extract actual ID from prefix (e.g., "CEN-5" -> "5")
                actual_id = patient_id_with_prefix.split('-')[1] if '-' in str(patient_id_with_prefix) else patient_id_with_prefix
                # Delete from local database
                self.local_db_instance.delete('patients', 'patient_id', actual_id)
                messagebox.showinfo("Success", "Patient deleted successfully!")
                self.load_patients()
            else:
                messagebox.showerror("Error", "Cannot delete patients from remote hospitals!")
    
    def delete_doctor(self):
        selected = self.doctors_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a doctor to delete!")
            return
        
        item = self.doctors_tree.item(selected[0])
        values = item['values']
        doctor_id_with_prefix = values[0]
        doctor_name = values[1]
        hospital = values[5]
        
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete doctor '{doctor_name}' (ID: {doctor_id_with_prefix})?"):
            if hospital == self.hospital_name:
                # Extract actual ID from prefix
                actual_id = doctor_id_with_prefix.split('-')[1] if '-' in str(doctor_id_with_prefix) else doctor_id_with_prefix
                # Delete from local database
                self.local_db_instance.delete('doctors', 'doctor_id', actual_id)
                messagebox.showinfo("Success", "Doctor deleted successfully!")
                self.load_doctors()
            else:
                messagebox.showerror("Error", "Cannot delete doctors from remote hospitals!")
    
    def delete_appointment(self):
        selected = self.appointments_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an appointment to delete!")
            return
        
        item = self.appointments_tree.item(selected[0])
        values = item['values']
        appointment_id_with_prefix = values[0]
        hospital = values[6]
        
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete appointment ID: {appointment_id_with_prefix}?"):
            if hospital == self.hospital_name:
                # Extract actual ID from prefix
                actual_id = appointment_id_with_prefix.split('-')[1] if '-' in str(appointment_id_with_prefix) else appointment_id_with_prefix
                # Delete from local database
                self.local_db_instance.delete('appointments', 'appointment_id', actual_id)
                messagebox.showinfo("Success", "Appointment deleted successfully!")
                self.load_appointments()
            else:
                messagebox.showerror("Error", "Cannot delete appointments from remote hospitals!")
    
    def delete_medical_record(self):
        selected = self.records_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a medical record to delete!")
            return
        
        item = self.records_tree.item(selected[0])
        values = item['values']
        record_id_with_prefix = values[0]
        hospital = values[6]
        
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete medical record ID: {record_id_with_prefix}?"):
            if hospital == self.hospital_name:
                # Extract actual ID from prefix
                actual_id = record_id_with_prefix.split('-')[1] if '-' in str(record_id_with_prefix) else record_id_with_prefix
                # Delete from local database
                self.local_db_instance.delete('medical_records', 'record_id', actual_id)
                messagebox.showinfo("Success", "Medical record deleted successfully!")
                self.load_medical_records()
            else:
                messagebox.showerror("Error", "Cannot delete medical records from remote hospitals!")

    def update_patient_dialog(self, event):
        selected = self.patients_tree.selection()
        if not selected:
            return
        
        item = self.patients_tree.item(selected[0])
        values = item['values']
        patient_id_with_prefix = values[0]
        hospital = values[6]
        
        # Only allow updating local hospital records
        if hospital != self.hospital_name:
            messagebox.showerror("Error", "Cannot update patients from remote hospitals!")
            return
        
        # Extract actual ID from prefix
        actual_id = patient_id_with_prefix.split('-')[1] if '-' in str(patient_id_with_prefix) else patient_id_with_prefix
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Update Patient")
        dialog.geometry("450x450")
        dialog.configure(bg='white')
        
        tk.Label(dialog, text="Update Patient Information", font=('Arial', 14, 'bold'), bg='white').pack(pady=10)
        
        form_frame = tk.Frame(dialog, bg='white')
        form_frame.pack(padx=20, pady=10)
        
        fields = {}
        error_labels = {}
        
        # Name
        tk.Label(form_frame, text="Name:", font=('Arial', 10), bg='white').grid(row=0, column=0, sticky='w', pady=(5,0))
        name_entry = tk.Entry(form_frame, width=30)
        name_entry.insert(0, values[1])
        name_entry.grid(row=0, column=1, pady=(5,0), padx=10)
        fields['name'] = name_entry
        name_error = tk.Label(form_frame, text="", font=('Arial', 8), fg='red', bg='white')
        name_error.grid(row=1, column=1, sticky='w', padx=10)
        error_labels['name'] = name_error
        
        # Age
        tk.Label(form_frame, text="Age:", font=('Arial', 10), bg='white').grid(row=2, column=0, sticky='w', pady=(5,0))
        age_entry = tk.Entry(form_frame, width=30)
        age_entry.insert(0, values[2])
        age_entry.grid(row=2, column=1, pady=(5,0), padx=10)
        fields['age'] = age_entry
        age_error = tk.Label(form_frame, text="", font=('Arial', 8), fg='red', bg='white')
        age_error.grid(row=3, column=1, sticky='w', padx=10)
        error_labels['age'] = age_error
        
        # Gender
        tk.Label(form_frame, text="Gender:", font=('Arial', 10), bg='white').grid(row=4, column=0, sticky='w', pady=(5,0))
        gender_combo = ttk.Combobox(form_frame, width=28, state='readonly')
        gender_combo['values'] = ('Male', 'Female')
        gender_combo.set(values[3])
        gender_combo.grid(row=4, column=1, pady=(5,0), padx=10)
        fields['gender'] = gender_combo
        gender_error = tk.Label(form_frame, text="", font=('Arial', 8), fg='red', bg='white')
        gender_error.grid(row=5, column=1, sticky='w', padx=10)
        error_labels['gender'] = gender_error
        
        # Phone
        tk.Label(form_frame, text="Phone:", font=('Arial', 10), bg='white').grid(row=6, column=0, sticky='w', pady=(5,0))
        phone_entry = tk.Entry(form_frame, width=30)
        phone_entry.insert(0, values[4])
        phone_entry.grid(row=6, column=1, pady=(5,0), padx=10)
        fields['phone'] = phone_entry
        phone_error = tk.Label(form_frame, text="", font=('Arial', 8), fg='red', bg='white')
        phone_error.grid(row=7, column=1, sticky='w', padx=10)
        error_labels['phone'] = phone_error
        
        # Address
        tk.Label(form_frame, text="Address:", font=('Arial', 10), bg='white').grid(row=8, column=0, sticky='w', pady=(5,0))
        address_entry = tk.Entry(form_frame, width=30)
        address_entry.insert(0, values[5])
        address_entry.grid(row=8, column=1, pady=(5,0), padx=10)
        fields['address'] = address_entry
        address_error = tk.Label(form_frame, text="", font=('Arial', 8), fg='red', bg='white')
        address_error.grid(row=9, column=1, sticky='w', padx=10)
        error_labels['address'] = address_error
        
        def clear_errors():
            for error_label in error_labels.values():
                error_label.config(text="")
        
        def update_patient():
            clear_errors()
            data = {key: entry.get() for key, entry in fields.items()}
            has_error = False
            
            # Validate name
            valid, msg = self.validate_name(data.get('name', ''))
            if not valid:
                error_labels['name'].config(text=msg)
                has_error = True
            
            # Validate age
            if data.get('age'):
                valid, msg = self.validate_age(data['age'])
                if not valid:
                    error_labels['age'].config(text=msg)
                    has_error = True
            
            # Validate phone
            if data.get('phone'):
                valid, msg = self.validate_phone(data['phone'])
                if not valid:
                    error_labels['phone'].config(text=msg)
                    has_error = True
            
            if has_error:
                return
            
            self.local_db_instance.update('patients', 'patient_id', actual_id, data)
            messagebox.showinfo("Success", "Patient updated successfully!")
            dialog.destroy()
            self.load_patients()
        
        tk.Button(dialog, text="Update", command=update_patient, 
                 bg='#f39c12', fg='white', font=('Arial', 10, 'bold')).pack(pady=20)
    
    def update_doctor_dialog(self, event):
        selected = self.doctors_tree.selection()
        if not selected:
            return
        
        item = self.doctors_tree.item(selected[0])
        values = item['values']
        doctor_id_with_prefix = values[0]
        hospital = values[5]
        
        if hospital != self.hospital_name:
            messagebox.showerror("Error", "Cannot update doctors from remote hospitals!")
            return
        
        actual_id = doctor_id_with_prefix.split('-')[1] if '-' in str(doctor_id_with_prefix) else doctor_id_with_prefix
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Update Doctor")
        dialog.geometry("450x400")
        dialog.configure(bg='white')
        
        tk.Label(dialog, text="Update Doctor Information", font=('Arial', 14, 'bold'), bg='white').pack(pady=10)
        
        form_frame = tk.Frame(dialog, bg='white')
        form_frame.pack(padx=20, pady=10)
        
        fields = {}
        error_labels = {}
        labels = ['Name', 'Specialization', 'Phone', 'Email']
        current_values = [values[1], values[2], values[3], values[4]]
        
        for i, label in enumerate(labels):
            tk.Label(form_frame, text=f"{label}:", font=('Arial', 10), bg='white').grid(row=i*2, column=0, sticky='w', pady=(5,0))
            entry = tk.Entry(form_frame, width=30)
            entry.insert(0, current_values[i])
            entry.grid(row=i*2, column=1, pady=(5,0), padx=10)
            fields[label.lower()] = entry
            
            error_label = tk.Label(form_frame, text="", font=('Arial', 8), fg='red', bg='white')
            error_label.grid(row=i*2+1, column=1, sticky='w', padx=10)
            error_labels[label.lower()] = error_label
        
        def clear_errors():
            for error_label in error_labels.values():
                error_label.config(text="")
        
        def update_doctor():
            clear_errors()
            data = {key: entry.get() for key, entry in fields.items()}
            has_error = False
            
            # Validate name (required)
            valid, msg = self.validate_name(data.get('name', ''))
            if not valid:
                error_labels['name'].config(text=msg)
                has_error = True
            
            # Validate specialization (required)
            valid, msg = self.validate_specialization(data.get('specialization', ''))
            if not valid:
                error_labels['specialization'].config(text=msg)
                has_error = True
            
            # Validate phone (required)
            valid, msg = self.validate_phone(data.get('phone', ''))
            if not valid:
                error_labels['phone'].config(text=msg)
                has_error = True
            
            # Validate email (required)
            valid, msg = self.validate_email(data.get('email', ''))
            if not valid:
                error_labels['email'].config(text=msg)
                has_error = True
            
            if has_error:
                return
            
            self.local_db_instance.update('doctors', 'doctor_id', actual_id, data)
            messagebox.showinfo("Success", "Doctor updated successfully!")
            dialog.destroy()
            self.load_doctors()
        
        tk.Button(dialog, text="Update", command=update_doctor, 
                 bg='#f39c12', fg='white', font=('Arial', 10, 'bold')).pack(pady=20)
    
    def update_appointment_dialog(self, event):
        selected = self.appointments_tree.selection()
        if not selected:
            return
        
        item = self.appointments_tree.item(selected[0])
        values = item['values']
        appointment_id_with_prefix = values[0]
        hospital = values[6]
        
        if hospital != self.hospital_name:
            messagebox.showerror("Error", "Cannot update appointments from remote hospitals!")
            return
        
        actual_id = appointment_id_with_prefix.split('-')[1] if '-' in str(appointment_id_with_prefix) else appointment_id_with_prefix
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Update Appointment")
        dialog.geometry("550x450")
        dialog.configure(bg='white')
        
        tk.Label(dialog, text="Update Appointment Information", font=('Arial', 14, 'bold'), bg='white').pack(pady=10)
        
        form_frame = tk.Frame(dialog, bg='white')
        form_frame.pack(padx=20, pady=10)
        
        # Extract patient_id and doctor_id without prefix
        patient_id_full = str(values[1])
        doctor_id_full = str(values[2])
        patient_id = patient_id_full.split('-')[1] if '-' in patient_id_full else patient_id_full
        doctor_id = doctor_id_full.split('-')[1] if '-' in doctor_id_full else doctor_id_full
        
        # Get all patients and doctors
        all_patients = self.local_db_instance.get_all('patients')
        all_doctors = self.local_db_instance.get_all('doctors')
        
        # Create patient list with ID and Name
        patient_list = [f"{p['patient_id']} - {p['name']}" for p in all_patients]
        doctor_list = [f"{d['doctor_id']} - {d['name']} ({d['specialization']})" for d in all_doctors]
        
        # Find current patient and doctor in lists
        current_patient = None
        current_doctor = None
        for p in patient_list:
            if p.startswith(f"{patient_id} -"):
                current_patient = p
                break
        for d in doctor_list:
            if d.startswith(f"{doctor_id} -"):
                current_doctor = d
                break
        
        # Patient selection with search
        tk.Label(form_frame, text="Patient:", font=('Arial', 10), bg='white').grid(row=0, column=0, sticky='w', pady=5)
        patient_search_var = tk.StringVar()
        if current_patient:
            patient_search_var.set(current_patient)
        patient_combo = ttk.Combobox(form_frame, textvariable=patient_search_var, width=40)
        patient_combo['values'] = patient_list
        patient_combo.grid(row=0, column=1, pady=5, padx=10, columnspan=2)
        
        # Filter patients as user types
        def filter_patients(event):
            search_term = patient_search_var.get().lower()
            if search_term:
                filtered = [p for p in patient_list if search_term in p.lower()]
                patient_combo['values'] = filtered
            else:
                patient_combo['values'] = patient_list
        
        patient_combo.bind('<KeyRelease>', filter_patients)
        
        # Doctor selection with search
        tk.Label(form_frame, text="Doctor:", font=('Arial', 10), bg='white').grid(row=1, column=0, sticky='w', pady=5)
        doctor_search_var = tk.StringVar()
        if current_doctor:
            doctor_search_var.set(current_doctor)
        doctor_combo = ttk.Combobox(form_frame, textvariable=doctor_search_var, width=40)
        doctor_combo['values'] = doctor_list
        doctor_combo.grid(row=1, column=1, pady=5, padx=10, columnspan=2)
        
        # Filter doctors as user types
        def filter_doctors(event):
            search_term = doctor_search_var.get().lower()
            if search_term:
                filtered = [d for d in doctor_list if search_term in d.lower()]
                doctor_combo['values'] = filtered
            else:
                doctor_combo['values'] = doctor_list
        
        doctor_combo.bind('<KeyRelease>', filter_doctors)
        
        # Appointment Date with Calendar
        tk.Label(form_frame, text="Date:", font=('Arial', 10), bg='white').grid(row=2, column=0, sticky='w', pady=5)
        date_entry = DateEntry(form_frame, width=39, background='darkblue',
                              foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        # Set current date value
        try:
            date_entry.set_date(values[3])
        except:
            pass
        date_entry.grid(row=2, column=1, pady=5, padx=10, columnspan=2)
        
        # Appointment Time
        tk.Label(form_frame, text="Time (HH:MM):", font=('Arial', 10), bg='white').grid(row=3, column=0, sticky='w', pady=5)
        time_entry = tk.Entry(form_frame, width=42)
        time_entry.insert(0, values[4])
        time_entry.grid(row=3, column=1, pady=5, padx=10, columnspan=2)
        
        # Status
        tk.Label(form_frame, text="Status:", font=('Arial', 10), bg='white').grid(row=4, column=0, sticky='w', pady=5)
        status_combo = ttk.Combobox(form_frame, width=39, state='readonly')
        status_combo['values'] = ('Scheduled', 'Completed', 'Cancelled', 'No-Show')
        status_combo.set(values[5])
        status_combo.grid(row=4, column=1, pady=5, padx=10, columnspan=2)
        
        # Error labels
        error_label = tk.Label(form_frame, text="", font=('Arial', 9), fg='red', bg='white')
        error_label.grid(row=5, column=0, columnspan=3, pady=5)
        
        def update_appointment():
            error_label.config(text="")
            
            # Extract patient ID from selection
            patient_selection = patient_search_var.get().strip()
            doctor_selection = doctor_search_var.get().strip()
            
            # Validate patient selection - must be from dropdown list
            if not patient_selection:
                error_label.config(text="Please select a patient!")
                return
            
            if patient_selection not in patient_list:
                error_label.config(text="Please select a valid patient from the list!")
                patient_search_var.set(current_patient if current_patient else '')
                return
            
            # Validate doctor selection - must be from dropdown list
            if not doctor_selection:
                error_label.config(text="Please select a doctor!")
                return
            
            if doctor_selection not in doctor_list:
                error_label.config(text="Please select a valid doctor from the list!")
                doctor_search_var.set(current_doctor if current_doctor else '')
                return
            
            # Extract IDs (format: "ID - Name")
            try:
                patient_id = patient_selection.split(' - ')[0].strip()
                doctor_id = doctor_selection.split(' - ')[0].strip()
            except:
                error_label.config(text="Invalid patient or doctor selection!")
                return
            
            # Get date from calendar widget
            date_value = date_entry.get_date().strftime('%Y-%m-%d')
            valid, msg = self.validate_date(date_value)
            if not valid:
                error_label.config(text=f"Date error: {msg}")
                return
            
            # Validate time
            time_value = time_entry.get()
            valid, msg = self.validate_time(time_value)
            if not valid:
                error_label.config(text=f"Time error: {msg}")
                return
            
            data = {
                'patient_id': patient_id,
                'doctor_id': doctor_id,
                'appointment_date': date_value,
                'appointment_time': time_value,
                'status': status_combo.get()
            }
            
            self.local_db_instance.update('appointments', 'appointment_id', actual_id, data)
            messagebox.showinfo("Success", "Appointment updated successfully!")
            dialog.destroy()
            self.load_appointments()
        
        tk.Button(dialog, text="Update", command=update_appointment, 
                 bg='#f39c12', fg='white', font=('Arial', 10, 'bold')).pack(pady=20)
    
    def update_medical_record_dialog(self, event):
        selected = self.records_tree.selection()
        if not selected:
            return
        
        item = self.records_tree.item(selected[0])
        values = item['values']
        record_id_with_prefix = values[0]
        hospital = values[6]
        
        if hospital != self.hospital_name:
            messagebox.showerror("Error", "Cannot update medical records from remote hospitals!")
            return
        
        actual_id = record_id_with_prefix.split('-')[1] if '-' in str(record_id_with_prefix) else record_id_with_prefix
        
        # Get full record from database to get notes field
        records = self.local_db_instance.get_all('medical_records')
        current_record = None
        for record in records:
            if str(record.get('record_id')) == str(actual_id):
                current_record = record
                break
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Update Medical Record")
        dialog.geometry("550x650")
        dialog.configure(bg='white')
        
        tk.Label(dialog, text="Update Medical Record Information", font=('Arial', 14, 'bold'), bg='white').pack(pady=10)
        
        form_frame = tk.Frame(dialog, bg='white')
        form_frame.pack(padx=20, pady=10)
        
        # Extract patient_id and doctor_id without prefix
        patient_id_full = str(values[1])
        doctor_id_full = str(values[2])
        patient_id = patient_id_full.split('-')[1] if '-' in patient_id_full else patient_id_full
        doctor_id = doctor_id_full.split('-')[1] if '-' in doctor_id_full else doctor_id_full
        
        # Get all patients and doctors
        all_patients = self.local_db_instance.get_all('patients')
        all_doctors = self.local_db_instance.get_all('doctors')
        
        # Create patient list with ID and Name
        patient_list = [f"{p['patient_id']} - {p['name']}" for p in all_patients]
        doctor_list = [f"{d['doctor_id']} - {d['name']} ({d['specialization']})" for d in all_doctors]
        
        # Find current patient and doctor in lists
        current_patient = None
        current_doctor = None
        for p in patient_list:
            if p.startswith(f"{patient_id} -"):
                current_patient = p
                break
        for d in doctor_list:
            if d.startswith(f"{doctor_id} -"):
                current_doctor = d
                break
        
        # Patient selection with search
        tk.Label(form_frame, text="Patient:", font=('Arial', 10), bg='white').grid(row=0, column=0, sticky='w', pady=(5,0))
        patient_search_var = tk.StringVar()
        if current_patient:
            patient_search_var.set(current_patient)
        patient_combo = ttk.Combobox(form_frame, textvariable=patient_search_var, width=40)
        patient_combo['values'] = patient_list
        patient_combo.grid(row=0, column=1, pady=(5,0), padx=10)
        patient_id_error = tk.Label(form_frame, text="", font=('Arial', 8), fg='red', bg='white')
        patient_id_error.grid(row=1, column=1, sticky='w', padx=10)
        
        # Filter patients as user types
        def filter_patients(event):
            search_term = patient_search_var.get().lower()
            if search_term:
                filtered = [p for p in patient_list if search_term in p.lower()]
                patient_combo['values'] = filtered
            else:
                patient_combo['values'] = patient_list
        
        patient_combo.bind('<KeyRelease>', filter_patients)
        
        # Doctor selection with search
        tk.Label(form_frame, text="Doctor:", font=('Arial', 10), bg='white').grid(row=2, column=0, sticky='w', pady=(5,0))
        doctor_search_var = tk.StringVar()
        if current_doctor:
            doctor_search_var.set(current_doctor)
        doctor_combo = ttk.Combobox(form_frame, textvariable=doctor_search_var, width=40)
        doctor_combo['values'] = doctor_list
        doctor_combo.grid(row=2, column=1, pady=(5,0), padx=10)
        doctor_id_error = tk.Label(form_frame, text="", font=('Arial', 8), fg='red', bg='white')
        doctor_id_error.grid(row=3, column=1, sticky='w', padx=10)
        
        # Filter doctors as user types
        def filter_doctors(event):
            search_term = doctor_search_var.get().lower()
            if search_term:
                filtered = [d for d in doctor_list if search_term in d.lower()]
                doctor_combo['values'] = filtered
            else:
                doctor_combo['values'] = doctor_list
        
        doctor_combo.bind('<KeyRelease>', filter_doctors)
        
        # Diagnosis
        tk.Label(form_frame, text="Diagnosis:", font=('Arial', 10), bg='white').grid(row=4, column=0, sticky='w', pady=(5,0))
        diagnosis_entry = tk.Entry(form_frame, width=30)
        diagnosis_entry.insert(0, values[3])
        diagnosis_entry.grid(row=4, column=1, pady=(5,0), padx=10)
        diagnosis_error = tk.Label(form_frame, text="", font=('Arial', 8), fg='red', bg='white')
        diagnosis_error.grid(row=5, column=1, sticky='w', padx=10)
        
        # Prescription
        tk.Label(form_frame, text="Prescription:", font=('Arial', 10), bg='white').grid(row=6, column=0, sticky='w', pady=(5,0))
        prescription_entry = tk.Entry(form_frame, width=30)
        prescription_entry.insert(0, values[4])
        prescription_entry.grid(row=6, column=1, pady=(5,0), padx=10)
        prescription_error = tk.Label(form_frame, text="", font=('Arial', 8), fg='red', bg='white')
        prescription_error.grid(row=7, column=1, sticky='w', padx=10)
        
        # Notes
        tk.Label(form_frame, text="Notes:", font=('Arial', 10), bg='white').grid(row=8, column=0, sticky='nw', pady=(5,0))
        notes_text = tk.Text(form_frame, width=30, height=5)
        if current_record and current_record.get('notes'):
            notes_text.insert(1.0, current_record.get('notes'))
        notes_text.grid(row=8, column=1, pady=(5,0), padx=10)
        
        # Record Date with Calendar
        tk.Label(form_frame, text="Record Date:", font=('Arial', 10), bg='white').grid(row=9, column=0, sticky='w', pady=(5,0))
        date_entry = DateEntry(form_frame, width=27, background='darkblue',
                              foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        # Set current date value
        try:
            date_entry.set_date(values[5])
        except:
            pass
        date_entry.grid(row=9, column=1, pady=(5,0), padx=10)
        date_error = tk.Label(form_frame, text="", font=('Arial', 8), fg='red', bg='white')
        date_error.grid(row=10, column=1, sticky='w', padx=10)
        
        def clear_errors():
            patient_id_error.config(text="")
            doctor_id_error.config(text="")
            diagnosis_error.config(text="")
            prescription_error.config(text="")
            date_error.config(text="")
        
        def update_record():
            clear_errors()
            
            # Extract patient ID from selection
            patient_selection = patient_search_var.get()
            doctor_selection = doctor_search_var.get()
            
            has_error = False
            
            if not patient_selection:
                patient_id_error.config(text="Patient is required")
                has_error = True
            
            if not doctor_selection:
                doctor_id_error.config(text="Doctor is required")
                has_error = True
            
            if has_error:
                return
            
            # Extract IDs (format: "ID - Name")
            try:
                patient_id = patient_selection.split(' - ')[0].strip()
                doctor_id = doctor_selection.split(' - ')[0].strip()
            except:
                patient_id_error.config(text="Invalid selection!")
                return
            
            data = {
                'patient_id': patient_id,
                'doctor_id': doctor_id,
                'diagnosis': diagnosis_entry.get(),
                'prescription': prescription_entry.get(),
                'notes': notes_text.get(1.0, tk.END).strip(),
                'record_date': date_entry.get_date().strftime('%Y-%m-%d')
            }
            
            has_error = False
            
            if data.get('diagnosis'):
                valid, msg = self.validate_diagnosis(data['diagnosis'])
                if not valid:
                    diagnosis_error.config(text=msg)
                    has_error = True
            
            if data.get('prescription'):
                valid, msg = self.validate_name(data['prescription'])
                if not valid:
                    prescription_error.config(text="Minimum 3 characters")
                    has_error = True
            
            if has_error:
                return
            
            self.local_db_instance.update('medical_records', 'record_id', actual_id, data)
            messagebox.showinfo("Success", "Medical record updated successfully!")
            dialog.destroy()
            self.load_medical_records()
        
        tk.Button(dialog, text="Update", command=update_record, 
                 bg='#f39c12', fg='white', font=('Arial', 10, 'bold')).pack(pady=20)

def main():
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python gui.py <hospital_name> [port] [is_master]")
        print("Example: python gui.py 'City Hospital' 5000 master")
        sys.exit(1)
    
    hospital_name = sys.argv[1]
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 5000
    is_master = len(sys.argv) > 3 and sys.argv[3].lower() == 'master'
    db_name = f"{hospital_name.replace(' ', '_').lower()}.db"
    
    root = tk.Tk()
    app = HospitalManagementGUI(root, is_master=is_master, local_port=port, 
                                local_db=db_name, hospital_name=hospital_name)
    root.mainloop()

if __name__ == '__main__':
    main()
