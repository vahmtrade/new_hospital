# Troubleshooting: Failed to Connect

## Error: "Failed to connect to http://192.168.43.247:5001"

Let's diagnose the problem step by step.

---

## Step 1: Verify the Server is Running on Laptop 2

**On Laptop 2 (IP: 192.168.43.247):**

1. Check if `start_hospital1.bat` is running
2. You should see TWO windows open:
   - **Window 1**: Server running (shows "Running on http://0.0.0.0:5001")
   - **Window 2**: GUI application

3. Look for this message in the server window:
   ```
   * Running on http://0.0.0.0:5001
   * Running on http://127.0.0.1:5001
   * Running on http://192.168.43.247:5001
   ```

**If you DON'T see this:**
- The server is not running
- Close everything and run `start_hospital1.bat` again

---

## Step 2: Test Locally on Laptop 2

**On Laptop 2 (the one with IP 192.168.43.247):**

1. Open a web browser (Chrome, Edge, Firefox)
2. Go to: `http://localhost:5001/health`
3. You should see: `{"status":"ok","hospital":"City Hospital"}`

**If this works:** Server is running correctly ✅
**If this fails:** Server has a problem ❌

---

## Step 3: Check Firewall on Laptop 2

**On Laptop 2:**

Run Command Prompt as Administrator and check:

```cmd
netsh advfirewall firewall show rule name="Hospital System Port 5001"
```

**If you see "No rules match":**
- Firewall rule is missing
- Run: `netsh advfirewall firewall add rule name="Hospital System Port 5001" dir=in action=allow protocol=TCP localport=5001`

---

## Step 4: Test Network Connection

**On Laptop 1 (Master):**

### Test 4a: Ping Test
```cmd
ping 192.168.43.247
```

**Expected result:**
```
Reply from 192.168.43.247: bytes=32 time=2ms TTL=128
Reply from 192.168.43.247: bytes=32 time=1ms TTL=128
```

**If you see "Request timed out":**
- Laptops are not on the same network
- Or firewall is blocking ping

### Test 4b: Browser Test
Open browser on Laptop 1 and go to:
```
http://192.168.43.247:5001/health
```

**If you see JSON response:** Connection works! ✅
**If you see error:** Connection blocked ❌

---

## Step 5: Verify Both Laptops on Same Network

**On both laptops, run:**
```cmd
ipconfig
```

Check that both IPs start with the same numbers:
- ✅ **Good**: 192.168.43.247 and 192.168.43.100 (same network)
- ❌ **Bad**: 192.168.43.247 and 192.168.1.100 (different networks)

**Both laptops MUST be connected to the SAME Wi-Fi network!**

---

## Step 6: Check if Port is Actually Open

**On Laptop 2, run Command Prompt:**

```cmd
netstat -an | findstr :5001
```

**Expected result:**
```
TCP    0.0.0.0:5001           0.0.0.0:0              LISTENING
```

**If you see this:** Port is open and listening ✅
**If you see nothing:** Server is not running on port 5001 ❌

---

## Step 7: Temporarily Disable Firewall (Testing Only)

**On Laptop 2:**

1. Press Windows Key → Type "Windows Defender Firewall"
2. Click "Turn Windows Defender Firewall on or off"
3. Turn OFF for Private networks (temporarily)
4. Try connecting from Master again

**If it works now:**
- Problem is firewall
- Turn firewall back ON
- Add proper firewall rule (see Step 3)

**If it still doesn't work:**
- Problem is something else (network, server not running, etc.)

---

## Common Issues and Solutions

### Issue 1: "Connection timed out"
**Cause:** Firewall blocking
**Solution:** 
- Add firewall rule on Laptop 2
- Or temporarily disable firewall to test

### Issue 2: "Connection refused"
**Cause:** Server not running on Laptop 2
**Solution:** 
- Make sure `start_hospital1.bat` is running
- Check server window for errors

### Issue 3: "No route to host"
**Cause:** Laptops on different networks
**Solution:** 
- Connect both to same Wi-Fi
- Check IP addresses with `ipconfig`

### Issue 4: Wrong IP Address
**Cause:** IP address changed
**Solution:** 
- Run `ipconfig` on Laptop 2 again
- Use the current IP address

### Issue 5: Wrong Port
**Cause:** Using wrong port number
**Solution:** 
- Hospital 1 should use port 5001
- Hospital 2 should use port 5002
- Master uses port 5000

---

## Quick Diagnostic Checklist

Run through this checklist:

**On Laptop 2 (192.168.43.247):**
- [ ] `start_hospital1.bat` is running
- [ ] Server window shows "Running on http://0.0.0.0:5001"
- [ ] GUI window is open
- [ ] Browser test works: `http://localhost:5001/health`
- [ ] Firewall rule added for port 5001
- [ ] Connected to Wi-Fi

**On Laptop 1 (Master):**
- [ ] `start_master.bat` is running
- [ ] Connected to SAME Wi-Fi as Laptop 2
- [ ] Can ping 192.168.43.247
- [ ] Using correct URL: `http://192.168.43.247:5001`

---

## Still Not Working?

Try this manual test:

**On Laptop 1 (Master), open Python:**
```cmd
python
```

Then type:
```python
import requests
response = requests.get('http://192.168.43.247:5001/health', timeout=5)
print(response.json())
```

**If you see:** `{'status': 'ok', 'hospital': 'City Hospital'}`
- Connection works! Problem is in the GUI

**If you see error:**
- Copy the error message and we'll diagnose further

---

## Alternative: Test on Same Computer First

Before testing across laptops, test on ONE computer:

1. Start all three hospitals on one laptop
2. Use `localhost` URLs:
   - `http://localhost:5001`
   - `http://localhost:5002`
3. If this works, the code is fine
4. Then move to separate laptops

---

## Network Diagram - What Should Work

```
Laptop 1 (Master)              Laptop 2 (Hospital 1)
IP: 192.168.43.XXX             IP: 192.168.43.247
Port: 5000                     Port: 5001
                               
        [Same Wi-Fi Network]
                |
        ┌───────┴───────┐
        |               |
   [Laptop 1]      [Laptop 2]
   Can access →    Server running
   http://192.168.43.247:5001/health
```

---

## Get More Help

If still not working, provide these details:

1. **On Laptop 2**, what does this show?
   ```cmd
   netstat -an | findstr :5001
   ```

2. **On Laptop 1**, what does this show?
   ```cmd
   ping 192.168.43.247
   ```

3. **On Laptop 2**, what does the server window show?
   (Copy the last few lines)

4. Are both laptops on the same Wi-Fi network? What's the network name?
