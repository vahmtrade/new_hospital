import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from client import HospitalClient
from database import HospitalDatabase
import threading
import json

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
    
    def add_remote_hospital(self, url):
        """Add a remote hospital connection (for master laptop)"""
        client = HospitalClient(url)
        if client.check_health():
            self.remote_clients.append(client)
            return True
        return False
    
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
            self.patients_tree.insert('', 'end', values=(
                patient.get('patient_id', ''),
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
                for patient in remote_patients:
                    self.patients_tree.insert('', 'end', values=(
                        patient.get('patient_id', ''),
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
            self.patients_tree.insert('', 'end', values=(
                patient.get('patient_id', ''),
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
                for patient in remote_patients:
                    self.patients_tree.insert('', 'end', values=(
                        patient.get('patient_id', ''),
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
            self.doctors_tree.insert('', 'end', values=(
                doctor.get('doctor_id', ''),
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
                for doctor in remote_doctors:
                    self.doctors_tree.insert('', 'end', values=(
                        doctor.get('doctor_id', ''),
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
            self.doctors_tree.insert('', 'end', values=(
                doctor.get('doctor_id', ''),
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
                for doctor in remote_doctors:
                    self.doctors_tree.insert('', 'end', values=(
                        doctor.get('doctor_id', ''),
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
        for appt in local_appointments:
            self.appointments_tree.insert('', 'end', values=(
                appt.get('appointment_id', ''),
                appt.get('patient_id', ''),
                appt.get('doctor_id', ''),
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
                for appt in remote_appointments:
                    self.appointments_tree.insert('', 'end', values=(
                        appt.get('appointment_id', ''),
                        appt.get('patient_id', ''),
                        appt.get('doctor_id', ''),
                        appt.get('appointment_date', ''),
                        appt.get('appointment_time', ''),
                        appt.get('status', ''),
                        hospital_name
                    ))
    
    def load_medical_records(self):
        for item in self.records_tree.get_children():
            self.records_tree.delete(item)
        
        local_records = self.local_db_instance.get_all('medical_records')
        for record in local_records:
            self.records_tree.insert('', 'end', values=(
                record.get('record_id', ''),
                record.get('patient_id', ''),
                record.get('doctor_id', ''),
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
                for record in remote_records:
                    self.records_tree.insert('', 'end', values=(
                        record.get('record_id', ''),
                        record.get('patient_id', ''),
                        record.get('doctor_id', ''),
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
        dialog.geometry("400x350")
        dialog.configure(bg='white')
        
        tk.Label(dialog, text="Patient Information", font=('Arial', 14, 'bold'), bg='white').pack(pady=10)
        
        form_frame = tk.Frame(dialog, bg='white')
        form_frame.pack(padx=20, pady=10)
        
        fields = {}
        labels = ['Name', 'Age', 'Gender', 'Phone', 'Address']
        
        for i, label in enumerate(labels):
            tk.Label(form_frame, text=f"{label}:", font=('Arial', 10), bg='white').grid(row=i, column=0, sticky='w', pady=5)
            entry = tk.Entry(form_frame, width=30)
            entry.grid(row=i, column=1, pady=5, padx=10)
            fields[label.lower()] = entry
        
        def save_patient():
            data = {key: entry.get() for key, entry in fields.items()}
            if data['name']:
                self.local_db_instance.insert('patients', data)
                messagebox.showinfo("Success", "Patient added successfully!")
                dialog.destroy()
                self.load_patients()
            else:
                messagebox.showerror("Error", "Name is required!")
        
        tk.Button(dialog, text="Save", command=save_patient, 
                 bg='#2ecc71', fg='white', font=('Arial', 10, 'bold')).pack(pady=20)
    
    def add_doctor_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Doctor")
        dialog.geometry("400x350")
        dialog.configure(bg='white')
        
        tk.Label(dialog, text="Doctor Information", font=('Arial', 14, 'bold'), bg='white').pack(pady=10)
        
        form_frame = tk.Frame(dialog, bg='white')
        form_frame.pack(padx=20, pady=10)
        
        fields = {}
        labels = ['Name', 'Specialization', 'Phone', 'Email']
        
        for i, label in enumerate(labels):
            tk.Label(form_frame, text=f"{label}:", font=('Arial', 10), bg='white').grid(row=i, column=0, sticky='w', pady=5)
            entry = tk.Entry(form_frame, width=30)
            entry.grid(row=i, column=1, pady=5, padx=10)
            fields[label.lower()] = entry
        
        def save_doctor():
            data = {key: entry.get() for key, entry in fields.items()}
            if data['name']:
                self.local_db_instance.insert('doctors', data)
                messagebox.showinfo("Success", "Doctor added successfully!")
                dialog.destroy()
                self.load_doctors()
            else:
                messagebox.showerror("Error", "Name is required!")
        
        tk.Button(dialog, text="Save", command=save_doctor, 
                 bg='#2ecc71', fg='white', font=('Arial', 10, 'bold')).pack(pady=20)
    
    def add_appointment_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Appointment")
        dialog.geometry("400x400")
        dialog.configure(bg='white')
        
        tk.Label(dialog, text="Appointment Information", font=('Arial', 14, 'bold'), bg='white').pack(pady=10)
        
        form_frame = tk.Frame(dialog, bg='white')
        form_frame.pack(padx=20, pady=10)
        
        fields = {}
        labels = ['Patient ID', 'Doctor ID', 'Appointment Date (YYYY-MM-DD)', 'Appointment Time (HH:MM)', 'Status']
        
        for i, label in enumerate(labels):
            tk.Label(form_frame, text=f"{label}:", font=('Arial', 10), bg='white').grid(row=i, column=0, sticky='w', pady=5)
            entry = tk.Entry(form_frame, width=30)
            entry.grid(row=i, column=1, pady=5, padx=10)
            key = label.lower().replace(' ', '_').replace('(', '').replace(')', '').replace('-', '_')
            if 'yyyy' in key or 'hh' in key:
                key = key.split('_')[0] + '_' + key.split('_')[1]
            fields[key] = entry
        
        def save_appointment():
            data = {
                'patient_id': fields['patient_id'].get(),
                'doctor_id': fields['doctor_id'].get(),
                'appointment_date': fields['appointment_date'].get(),
                'appointment_time': fields['appointment_time'].get(),
                'status': fields['status'].get() or 'Scheduled'
            }
            if data['patient_id'] and data['doctor_id']:
                self.local_db_instance.insert('appointments', data)
                messagebox.showinfo("Success", "Appointment added successfully!")
                dialog.destroy()
                self.load_appointments()
            else:
                messagebox.showerror("Error", "Patient ID and Doctor ID are required!")
        
        tk.Button(dialog, text="Save", command=save_appointment, 
                 bg='#2ecc71', fg='white', font=('Arial', 10, 'bold')).pack(pady=20)
    
    def add_medical_record_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Medical Record")
        dialog.geometry("450x500")
        dialog.configure(bg='white')
        
        tk.Label(dialog, text="Medical Record Information", font=('Arial', 14, 'bold'), bg='white').pack(pady=10)
        
        form_frame = tk.Frame(dialog, bg='white')
        form_frame.pack(padx=20, pady=10)
        
        tk.Label(form_frame, text="Patient ID:", font=('Arial', 10), bg='white').grid(row=0, column=0, sticky='w', pady=5)
        patient_id_entry = tk.Entry(form_frame, width=30)
        patient_id_entry.grid(row=0, column=1, pady=5, padx=10)
        
        tk.Label(form_frame, text="Doctor ID:", font=('Arial', 10), bg='white').grid(row=1, column=0, sticky='w', pady=5)
        doctor_id_entry = tk.Entry(form_frame, width=30)
        doctor_id_entry.grid(row=1, column=1, pady=5, padx=10)
        
        tk.Label(form_frame, text="Diagnosis:", font=('Arial', 10), bg='white').grid(row=2, column=0, sticky='w', pady=5)
        diagnosis_entry = tk.Entry(form_frame, width=30)
        diagnosis_entry.grid(row=2, column=1, pady=5, padx=10)
        
        tk.Label(form_frame, text="Prescription:", font=('Arial', 10), bg='white').grid(row=3, column=0, sticky='w', pady=5)
        prescription_entry = tk.Entry(form_frame, width=30)
        prescription_entry.grid(row=3, column=1, pady=5, padx=10)
        
        tk.Label(form_frame, text="Notes:", font=('Arial', 10), bg='white').grid(row=4, column=0, sticky='nw', pady=5)
        notes_text = tk.Text(form_frame, width=30, height=5)
        notes_text.grid(row=4, column=1, pady=5, padx=10)
        
        tk.Label(form_frame, text="Record Date (YYYY-MM-DD):", font=('Arial', 10), bg='white').grid(row=5, column=0, sticky='w', pady=5)
        date_entry = tk.Entry(form_frame, width=30)
        date_entry.grid(row=5, column=1, pady=5, padx=10)
        
        def save_record():
            data = {
                'patient_id': patient_id_entry.get(),
                'doctor_id': doctor_id_entry.get(),
                'diagnosis': diagnosis_entry.get(),
                'prescription': prescription_entry.get(),
                'notes': notes_text.get(1.0, tk.END).strip(),
                'record_date': date_entry.get()
            }
            if data['patient_id'] and data['doctor_id']:
                self.local_db_instance.insert('medical_records', data)
                messagebox.showinfo("Success", "Medical record added successfully!")
                dialog.destroy()
                self.load_medical_records()
            else:
                messagebox.showerror("Error", "Patient ID and Doctor ID are required!")
        
        tk.Button(dialog, text="Save", command=save_record, 
                 bg='#2ecc71', fg='white', font=('Arial', 10, 'bold')).pack(pady=20)
    
    def delete_patient(self):
        selected = self.patients_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a patient to delete!")
            return
        
        item = self.patients_tree.item(selected[0])
        values = item['values']
        patient_id = values[0]
        patient_name = values[1]
        hospital = values[6]
        
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete patient '{patient_name}' (ID: {patient_id})?"):
            if hospital == self.hospital_name:
                # Delete from local database
                self.local_db_instance.delete('patients', 'patient_id', patient_id)
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
        doctor_id = values[0]
        doctor_name = values[1]
        hospital = values[5]
        
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete doctor '{doctor_name}' (ID: {doctor_id})?"):
            if hospital == self.hospital_name:
                # Delete from local database
                self.local_db_instance.delete('doctors', 'doctor_id', doctor_id)
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
        appointment_id = values[0]
        hospital = values[6]
        
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete appointment ID: {appointment_id}?"):
            if hospital == self.hospital_name:
                # Delete from local database
                self.local_db_instance.delete('appointments', 'appointment_id', appointment_id)
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
        record_id = values[0]
        hospital = values[6]
        
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete medical record ID: {record_id}?"):
            if hospital == self.hospital_name:
                # Delete from local database
                self.local_db_instance.delete('medical_records', 'record_id', record_id)
                messagebox.showinfo("Success", "Medical record deleted successfully!")
                self.load_medical_records()
            else:
                messagebox.showerror("Error", "Cannot delete medical records from remote hospitals!")

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
