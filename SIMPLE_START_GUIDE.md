# Simple Start Guide - Step by Step

Let's start from scratch and make sure everything works.

---

## STEP 1: Test on ONE Computer First

Before trying to connect multiple laptops, let's make sure it works on one computer.

### 1a. Install Python Packages

Open Command Prompt and run:
```cmd
pip install flask requests pillow
```

Wait for it to finish. You should see "Successfully installed..."

### 1b. Run Basic Test

Double-click: **`test_basic.bat`**

This will:
- Check if Python is installed
- Check if packages are installed
- Test if the server can start
- Test if you can connect to it

**If this fails, tell me what error you see!**

---

## STEP 2: Test on ONE Computer with All 3 Hospitals

### 2a. Start Master Hospital

1. Double-click **`start_master.bat`**
2. You should see **TWO windows open**:
   - Window 1: Black window with text (server)
   - Window 2: Colorful window with buttons (GUI)

**Take a screenshot if something goes wrong!**

### 2b. Test Master Locally

In the GUI window:
1. Click on "Patients" tab
2. Click "Add Patient" button
3. Fill in:
   - Name: Test Patient
   - Age: 30
   - Gender: Male
4. Click "Save"
5. You should see the patient in the table

**Does this work?**
- ✅ YES → Continue to next step
- ❌ NO → Tell me what error you see

### 2c. Start Hospital 1

1. Double-click **`start_hospital1.bat`**
2. Again, TWO windows should open
3. In the GUI, add a patient named "Hospital 1 Patient"

### 2d. Connect Master to Hospital 1

1. Go back to the **Master GUI window**
2. Click on **"Master Control"** tab
3. In the "Add Hospital URL" box, type: `http://localhost:5001`
4. Click **"Connect"**

**What happens?**
- ✅ "Connected to hospital..." → SUCCESS!
- ❌ "Failed to connect..." → There's a problem

### 2e. View All Patients

1. In Master GUI, go to "Patients" tab
2. Click "Refresh"
3. You should see:
   - Test Patient (from Central Hospital)
   - Hospital 1 Patient (from City Hospital)

**Do you see both patients?**
- ✅ YES → System works! Now we can try multiple laptops
- ❌ NO → Something is wrong

---

## STEP 3: If Step 2 Works, Try Multiple Laptops

Only do this if Step 2 worked perfectly!

### 3a. On Laptop 1 (Master)

1. Find IP address:
   ```cmd
   ipconfig
   ```
   Write it down: ________________

2. Start master:
   ```cmd
   start_master.bat
   ```

### 3b. On Laptop 2

1. Find IP address:
   ```cmd
   ipconfig
   ```
   Write it down: ________________

2. Make sure it's on the SAME Wi-Fi as Laptop 1

3. Start hospital:
   ```cmd
   start_hospital1.bat
   ```

4. Test locally - open browser on Laptop 2:
   ```
   http://localhost:5001/health
   ```
   Should show: `{"status":"ok","hospital":"City Hospital"}`

5. Add firewall rule - run as Administrator:
   ```cmd
   netsh advfirewall firewall add rule name="Hospital Port 5001" dir=in action=allow protocol=TCP localport=5001
   ```

### 3c. Test Connection from Laptop 1

On Laptop 1, open browser:
```
http://[LAPTOP_2_IP]:5001/health
```
(Replace [LAPTOP_2_IP] with the actual IP from step 3b)

**Does it show the JSON response?**
- ✅ YES → Connection works! Use this IP in Master GUI
- ❌ NO → Connection is blocked

---

## Common Problems and Solutions

### Problem: "pip is not recognized"

**Solution:**
```cmd
python -m pip install flask requests pillow
```

### Problem: "Python is not recognized"

**Solution:** Python is not installed or not in PATH
1. Download Python from python.org
2. During installation, check "Add Python to PATH"
3. Restart computer

### Problem: Server window closes immediately

**Solution:** There's an error in the code
1. Open Command Prompt
2. Run manually:
   ```cmd
   python server.py "Test Hospital" 5001 test.db
   ```
3. Tell me what error you see

### Problem: GUI window doesn't open

**Solution:** 
1. Open Command Prompt
2. Run manually:
   ```cmd
   python gui.py "Test Hospital" 5001
   ```
3. Tell me what error you see

### Problem: "ModuleNotFoundError: No module named 'flask'"

**Solution:**
```cmd
pip install flask requests pillow
```

### Problem: Can't connect between laptops

**Checklist:**
- [ ] Both laptops on same Wi-Fi?
- [ ] Firewall rule added on Laptop 2?
- [ ] Server running on Laptop 2?
- [ ] Can ping from Laptop 1 to Laptop 2?
- [ ] Browser test works from Laptop 1?

---

## What to Tell Me If It Doesn't Work

Please provide:

1. **Which step failed?** (Step 1, 2a, 2b, etc.)

2. **What error message do you see?** (Copy the exact text)

3. **Screenshot of the error** (if possible)

4. **Run this and tell me the output:**
   ```cmd
   python --version
   pip list | findstr flask
   ```

5. **If testing between laptops:**
   - Are both on same Wi-Fi? What's the network name?
   - What are the IP addresses of both laptops?
   - Can you ping between them?

---

## Quick Diagnostic Commands

Run these and tell me the results:

**Check Python:**
```cmd
python --version
```

**Check packages:**
```cmd
pip list
```

**Check if server is running:**
```cmd
netstat -an | findstr :5001
```

**Test server locally:**
```cmd
curl http://localhost:5001/health
```
(or open in browser)

---

## Start Fresh

If everything is broken, start completely fresh:

1. **Close all windows** (server and GUI)

2. **Delete database files:**
   ```cmd
   del *.db
   ```

3. **Reinstall packages:**
   ```cmd
   pip uninstall flask requests pillow -y
   pip install flask requests pillow
   ```

4. **Run test_basic.bat** again

5. **Start from Step 1**
