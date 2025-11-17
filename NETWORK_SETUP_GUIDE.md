# Network Setup Guide - Connecting 3 Laptops

## Overview
To connect 3 laptops, each laptop needs to know the IP address of the others. The master laptop will connect to the other two hospitals using their IP addresses.

---

## Step 1: Find Each Laptop's IP Address

### On Windows (All 3 Laptops):

1. **Open Command Prompt**:
   - Press `Windows Key + R`
   - Type `cmd` and press Enter

2. **Run this command**:
   ```cmd
   ipconfig
   ```

3. **Look for your IP address**:
   ```
   Wireless LAN adapter Wi-Fi:
      IPv4 Address. . . . . . . . . . . : 192.168.1.100
   ```
   OR
   ```
   Ethernet adapter Ethernet:
      IPv4 Address. . . . . . . . . . . : 192.168.1.100
   ```

4. **Write down the IP address** for each laptop:
   - **Laptop 1 (Master)**: Example: `192.168.1.100`
   - **Laptop 2 (Hospital 1)**: Example: `192.168.1.101`
   - **Laptop 3 (Hospital 2)**: Example: `192.168.1.102`

---

## Step 2: Ensure All Laptops Are on Same Network

**All 3 laptops MUST be connected to the SAME Wi-Fi network or router!**

✅ **Correct**: All connected to "Home-WiFi"
❌ **Wrong**: Laptop 1 on "Home-WiFi", Laptop 2 on "Office-WiFi"

---

## Step 3: Configure Windows Firewall (All 3 Laptops)

Each laptop needs to allow Python through the firewall:

### Method 1: Quick (Allow Python)
1. Open **Windows Defender Firewall**
2. Click **"Allow an app through firewall"**
3. Click **"Change settings"** (requires admin)
4. Click **"Allow another app"**
5. Browse and select **Python** (usually in `C:\Python\python.exe`)
6. Check both **Private** and **Public** boxes
7. Click **OK**

### Method 2: Allow Specific Ports
1. Open **Windows Defender Firewall**
2. Click **"Advanced settings"**
3. Click **"Inbound Rules"** → **"New Rule"**
4. Select **"Port"** → Click **Next**
5. Select **TCP** and enter ports: `5000, 5001, 5002`
6. Select **"Allow the connection"**
7. Check all profiles (Domain, Private, Public)
8. Name it "Hospital System" → Click **Finish**

---

## Step 4: Start Each Hospital

### On Laptop 1 (Master - Central Hospital):
```cmd
# Double-click start_master.bat
# OR manually run:
python server.py "Central Hospital" 5000 central_hospital.db
python gui.py "Central Hospital" 5000 master
```
- **IP**: 192.168.1.100 (example)
- **Port**: 5000
- **URL**: `http://192.168.1.100:5000`

### On Laptop 2 (City Hospital):
```cmd
# Double-click start_hospital1.bat
# OR manually run:
python server.py "City Hospital" 5001 city_hospital.db
python gui.py "City Hospital" 5001
```
- **IP**: 192.168.1.101 (example)
- **Port**: 5001
- **URL**: `http://192.168.1.101:5001`

### On Laptop 3 (General Hospital):
```cmd
# Double-click start_hospital2.bat
# OR manually run:
python server.py "General Hospital" 5002 general_hospital.db
python gui.py "General Hospital" 5002
```
- **IP**: 192.168.1.102 (example)
- **Port**: 5002
- **URL**: `http://192.168.1.102:5002`

---

## Step 5: Connect Hospitals to Master

### On Laptop 1 (Master):

1. **Open the GUI** (should already be open)
2. **Go to "Master Control" tab**
3. **Add Hospital 1**:
   - In the "Add Hospital URL" field, type: `http://192.168.1.101:5001`
   - Click **"Connect"**
   - You should see: "Connected to hospital at http://192.168.1.101:5001"

4. **Add Hospital 2**:
   - In the "Add Hospital URL" field, type: `http://192.168.1.102:5002`
   - Click **"Connect"**
   - You should see: "Connected to hospital at http://192.168.1.102:5002"

5. **Verify Connection**:
   - The status box should show:
     ```
     Local Hospital: Central Hospital (localhost:5000)
     
     Connected Remote Hospitals:
     1. City Hospital - http://192.168.1.101:5001 [ONLINE]
     2. General Hospital - http://192.168.1.102:5002 [ONLINE]
     ```

---

## Step 6: Test the Connection

### Test 1: Add Data on Laptop 2
1. On **Laptop 2** (City Hospital), add a patient:
   - Name: John Doe
   - Age: 35
   - Gender: Male

### Test 2: View from Master
1. On **Laptop 1** (Master), go to "Patients" tab
2. Click **"Refresh"**
3. You should see John Doe with Hospital column showing "City Hospital"

### Test 3: Search Across Hospitals
1. On **Laptop 1** (Master), in Patients tab
2. Type "John" in search box
3. Click **"Search"**
4. Results from ALL hospitals appear!

---

## Troubleshooting

### Problem: "Failed to connect to hospital"

**Solution 1: Check IP Address**
```cmd
# On the laptop you're trying to connect to, run:
ipconfig
# Verify the IP address is correct
```

**Solution 2: Test Connection**
```cmd
# On Master laptop, run:
ping 192.168.1.101
# Should show replies, not "Request timed out"
```

**Solution 3: Check if Server is Running**
- Make sure the server window is open on the target laptop
- Look for: "Running on http://0.0.0.0:5001"

**Solution 4: Test in Browser**
- On Master laptop, open browser
- Go to: `http://192.168.1.101:5001/health`
- Should show: `{"hospital":"City Hospital","status":"ok"}`

### Problem: "Connection timed out"

**Cause**: Firewall is blocking the connection

**Solution**:
1. Temporarily disable Windows Firewall (for testing)
2. If it works, re-enable firewall and add Python exception (see Step 3)

### Problem: Different subnets

**Check**: All IPs should start with same numbers
- ✅ Good: 192.168.1.100, 192.168.1.101, 192.168.1.102
- ❌ Bad: 192.168.1.100, 192.168.2.101, 10.0.0.102

**Solution**: Connect all laptops to the same Wi-Fi network

---

## Quick Reference Card

Print this and keep it with each laptop:

```
┌─────────────────────────────────────────────┐
│  LAPTOP 1 - MASTER (Central Hospital)      │
├─────────────────────────────────────────────┤
│  IP Address: 192.168.1.___                  │
│  Port: 5000                                 │
│  Start: start_master.bat                    │
│  Role: Can see ALL hospitals                │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│  LAPTOP 2 - Hospital 1 (City Hospital)      │
├─────────────────────────────────────────────┤
│  IP Address: 192.168.1.___                  │
│  Port: 5001                                 │
│  Start: start_hospital1.bat                 │
│  Role: Independent hospital                 │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│  LAPTOP 3 - Hospital 2 (General Hospital)   │
├─────────────────────────────────────────────┤
│  IP Address: 192.168.1.___                  │
│  Port: 5002                                 │
│  Start: start_hospital2.bat                 │
│  Role: Independent hospital                 │
└─────────────────────────────────────────────┘

MASTER CONNECTS TO:
• http://192.168.1.___:5001 (Hospital 1)
• http://192.168.1.___:5002 (Hospital 2)
```

---

## Network Diagram

```
        [Router/Wi-Fi]
              |
    ┌─────────┼─────────┐
    |         |         |
[Laptop 1] [Laptop 2] [Laptop 3]
  Master    Hospital1  Hospital2
192.168.1  192.168.1  192.168.1
  .100       .101       .102
Port 5000  Port 5001  Port 5002
    |         ↑         ↑
    └─────────┴─────────┘
    Master connects to both
```

---

## Alternative: Testing on One Computer

If you want to test everything on ONE computer first:

**Use localhost (no IP needed)**:
- Master: `http://localhost:5000`
- Hospital 1: `http://localhost:5001`
- Hospital 2: `http://localhost:5002`

In Master Control tab, connect to:
- `http://localhost:5001`
- `http://localhost:5002`

This is perfect for testing before deploying to 3 laptops!
