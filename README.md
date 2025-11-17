# Hospital Management System - Distributed Architecture

A distributed hospital management system that runs on three laptops with a master-slave architecture. Each laptop represents a hospital with its own database, and the master laptop can access and display data from all connected hospitals.

## Features

- **4 Core Tables**: Patients, Doctors, Appointments, Medical Records
- **Distributed Architecture**: Each hospital maintains its own database
- **Master Node**: Central hospital can access all data from connected hospitals
- **Powerful GUI**: Modern tkinter-based interface with tabs and search functionality
- **REST API**: Flask-based API for inter-hospital communication
- **Real-time Search**: Search patients and doctors across all connected hospitals
- **Local & Remote Access**: Each hospital can manage its own data, master can view all

## System Requirements

- Python 3.7 or higher
- Windows OS (batch scripts provided)
- Network connectivity between laptops (for distributed setup)

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

## Quick Start (Single Machine Testing)

### Option 1: Using Batch Scripts (Windows)

1. **Start Master Hospital** (Port 5000):
   - Double-click `start_master.bat`
   - This opens the Central Hospital with master capabilities

2. **Start Hospital 1** (Port 5001):
   - Double-click `start_hospital1.bat`
   - This opens City Hospital

3. **Start Hospital 2** (Port 5002):
   - Double-click `start_hospital2.bat`
   - This opens General Hospital

4. **Connect Hospitals to Master**:
   - In the Master Hospital GUI, go to "Master Control" tab
   - Add hospital URLs:
     - `http://localhost:5001` (City Hospital)
     - `http://localhost:5002` (General Hospital)
   - Click "Connect" for each

### Option 2: Manual Start

**Terminal 1 - Master Hospital Server:**
```bash
python server.py "Central Hospital" 5000 central_hospital.db
```

**Terminal 2 - Master Hospital GUI:**
```bash
python gui.py "Central Hospital" 5000 master
```

**Terminal 3 - Hospital 1 Server:**
```bash
python server.py "City Hospital" 5001 city_hospital.db
```

**Terminal 4 - Hospital 1 GUI:**
```bash
python gui.py "City Hospital" 5001
```

**Terminal 5 - Hospital 2 Server:**
```bash
python server.py "General Hospital" 5002 general_hospital.db
```

**Terminal 6 - Hospital 2 GUI:**
```bash
python gui.py "General Hospital" 5002
```

## Multi-Laptop Setup

### Laptop 1 (Master - Central Hospital):
```bash
# Start server
python server.py "Central Hospital" 5000 central_hospital.db

# Start GUI (in another terminal)
python gui.py "Central Hospital" 5000 master
```

### Laptop 2 (City Hospital):
```bash
# Start server
python server.py "City Hospital" 5001 city_hospital.db

# Start GUI (in another terminal)
python gui.py "City Hospital" 5001
```

### Laptop 3 (General Hospital):
```bash
# Start server
python server.py "General Hospital" 5002 general_hospital.db

# Start GUI (in another terminal)
python gui.py "General Hospital" 5002
```

### Connecting Hospitals

On the Master laptop:
1. Open the GUI and go to "Master Control" tab
2. Find the IP addresses of other laptops (use `ipconfig` on Windows)
3. Add hospital URLs:
   - `http://192.168.1.100:5001` (replace with actual IP of Laptop 2)
   - `http://192.168.1.101:5002` (replace with actual IP of Laptop 3)
4. Click "Connect" for each hospital

## Usage Guide

### Adding Data

Each hospital can add:
- **Patients**: Name, Age, Gender, Phone, Address
- **Doctors**: Name, Specialization, Phone, Email
- **Appointments**: Patient ID, Doctor ID, Date, Time, Status
- **Medical Records**: Patient ID, Doctor ID, Diagnosis, Prescription, Notes, Date

### Searching

- **Local Search**: Each hospital can search its own patients and doctors
- **Master Search**: Master hospital searches across all connected hospitals
- Results show which hospital the data belongs to

### Master Control

The master laptop has an additional "Master Control" tab that shows:
- Connected hospitals status
- Ability to add new hospital connections
- Refresh all data from all hospitals

## Architecture

```
┌─────────────────────────────────────┐
│     Master Laptop (Central)         │
│  ┌──────────┐      ┌──────────┐    │
│  │  Server  │◄────►│   GUI    │    │
│  │ Port 5000│      │ (Master) │    │
│  └────┬─────┘      └──────────┘    │
│       │                              │
│       │ SQLite DB                    │
└───────┼──────────────────────────────┘
        │
        │ REST API
        │
    ┌───┴────────────────────┐
    │                        │
┌───▼────────────┐  ┌───────▼─────────┐
│  Laptop 2      │  │  Laptop 3       │
│ (City Hosp)    │  │ (General Hosp)  │
│ ┌────────┐     │  │  ┌────────┐     │
│ │ Server │     │  │  │ Server │     │
│ │Port5001│     │  │  │Port5002│     │
│ └───┬────┘     │  │  └───┬────┘     │
│     │          │  │      │          │
│ SQLite DB      │  │  SQLite DB      │
└────────────────┘  └─────────────────┘
```

## Database Schema

### Patients Table
- patient_id (PRIMARY KEY)
- name
- age
- gender
- phone
- address
- created_at

### Doctors Table
- doctor_id (PRIMARY KEY)
- name
- specialization
- phone
- email
- created_at

### Appointments Table
- appointment_id (PRIMARY KEY)
- patient_id (FOREIGN KEY)
- doctor_id (FOREIGN KEY)
- appointment_date
- appointment_time
- status
- created_at

### Medical Records Table
- record_id (PRIMARY KEY)
- patient_id (FOREIGN KEY)
- doctor_id (FOREIGN KEY)
- diagnosis
- prescription
- notes
- record_date
- created_at

## API Endpoints

- `GET /health` - Check server status
- `GET /patients?search=<term>` - Get/search patients
- `POST /patients` - Add new patient
- `GET /doctors?search=<term>` - Get/search doctors
- `POST /doctors` - Add new doctor
- `GET /appointments` - Get all appointments
- `POST /appointments` - Add new appointment
- `GET /medical_records` - Get all medical records
- `POST /medical_records` - Add new medical record

## Troubleshooting

### Port Already in Use
If you get a port error, change the port number in the start command.

### Cannot Connect to Remote Hospital
- Ensure both laptops are on the same network
- Check firewall settings (allow Python through firewall)
- Verify the IP address and port are correct
- Test with `ping <ip_address>`

### GUI Not Responding
- Ensure the server is running before starting the GUI
- Check the terminal for error messages

## Security Notes

This is a demonstration system. For production use:
- Add authentication and authorization
- Use HTTPS instead of HTTP
- Implement data encryption
- Add input validation and sanitization
- Use proper database security measures
- Implement audit logging

## License

This project is for educational purposes.
