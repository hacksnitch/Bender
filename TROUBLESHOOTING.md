# Bender Troubleshooting Guide

## 🔍 Diagnostic Steps

### Step 1: Check System Status
```bash
# Check if Bender is running
ps aux | grep main.py

# Check system resources
top
df -h
free -h

# Check temperature (Raspberry Pi)
vcgencmd measure_temp
```

### Step 2: Review Recent Logs
```bash
# View last 50 log entries
tail -n 50 logs/bender.log

# Look for errors in last hour
grep "$(date -d '1 hour ago' '+%Y-%m-%d %H')" logs/bender.log | grep ERROR

# Check for specific issues
grep -E "(ERROR|CRITICAL|Exception)" logs/bender.log | tail -10
```

### Step 3: Test Components Individually
```bash
# Test sensor
python3 ultrasound.py

# Test system initialization
python3 initialize.py

# Test network connectivity
ping -c 3 google.com
```

---

## 🚨 Common Problems & Solutions

### Problem: Bender Won't Start

**Symptoms:**
- Application exits immediately
- "Permission denied" errors
- GPIO setup failures

**Diagnosis:**
```bash
# Check permissions
groups $USER

# Check GPIO availability
ls -la /dev/gpiomem

# Check Python environment
which python3
python3 --version
```

**Solutions:**
```bash
# Fix GPIO permissions
sudo usermod -a -G gpio $USER
sudo reboot

# Fix Python environment
source bender-env/bin/activate
pip install -r requirements.txt

# Run with proper permissions
sudo bender-env/bin/python3 main.py
```

---

### Problem: Sensor Readings Inconsistent

**Symptoms:**
- Frequent timeout messages
- Erratic distance readings
- "No echo received" errors

**Diagnosis:**
```bash
# Test sensor directly
python3 ultrasound.py

# Check for interference
# Run multiple times and compare results
for i in {1..5}; do python3 ultrasound.py; sleep 1; done
```

**Solutions:**
1. **Physical Issues:**
   ```bash
   # Check connections
   # Ensure trigger is on GPIO 16 (pin 36)
   # Ensure echo is on GPIO 18 (pin 12)
   # Verify 5V and GND connections
   ```

2. **Environmental Issues:**
   - Remove obstacles in sensor path
   - Check for reflective surfaces
   - Ensure sensor is mounted straight

3. **Software Issues:**
   ```bash
   # Increase timeout in distance.py
   nano distance.py
   # Look for timeout values and increase them
   ```

---

### Problem: VersionOne API Errors

**Symptoms:**
- "HTTP error querying for tests"
- "Authentication failed"
- "Connection timeout"

**Diagnosis:**
```bash
# Test network connectivity
ping your-v1-instance.com

# Test API manually
curl -u "username:password" "https://your-instance/rest-1.v1/Data/Test"

# Check credentials
cat .env | grep V1_
```

**Solutions:**
1. **Network Issues:**
   ```bash
   # Check WiFi connection
   iwconfig
   
   # Restart networking
   sudo systemctl restart networking
   ```

2. **Credential Issues:**
   ```bash
   # Update .env file
   nano .env
   # Verify V1_USERNAME and V1_PASSWORD
   ```

3. **API Issues:**
   - Verify VersionOne instance is accessible
   - Check if API endpoints have changed
   - Confirm user has necessary permissions

---

### Problem: Vehicle Movement Issues

**Symptoms:**
- Vehicle doesn't move
- Moves in wrong direction
- Inconsistent movement

**Diagnosis:**
```bash
# Check motor connections
# Test GPIO outputs with multimeter
# Verify battery levels
```

**Solutions:**
1. **Wiring Issues:**
   ```
   Forward:  GPIO 12 (pin 32)
   Reverse:  GPIO 11 (pin 23)
   Left:     GPIO 13 (pin 33)
   Right:    GPIO 15 (pin 10)
   ```

2. **Power Issues:**
   - Check battery charge
   - Verify power supply connections
   - Test without load

3. **Software Issues:**
   ```bash
   # Test individual motor controls
   python3 -c "
   from drive import car, Direction
   import time
   car.init_car('startup')
   car.go(Direction.FORWARD, 1.0)
   car.init_car('shutdown')
   "
   ```

---

### Problem: High CPU/Memory Usage

**Symptoms:**
- System becomes sluggish
- High load averages
- Out of memory errors

**Diagnosis:**
```bash
# Monitor resource usage
htop
iostat 1
free -m

# Check for memory leaks
ps aux --sort=-%mem | head
```

**Solutions:**
```bash
# Increase polling interval
echo "POLL_TIME=10" >> .env

# Restart Bender periodically (cron job)
echo "0 */6 * * * /home/pi/restart_bender.sh" | crontab -

# Clean up log files
logrotate /home/pi/Bender/logs/bender.log
```

---

### Problem: Test Execution Failures

**Symptoms:**
- Tests always fail
- Script execution errors
- Dynamic script issues

**Diagnosis:**
```bash
# Check last generated script
cat script1.py

# Review test execution logs
grep "execTest" logs/bender.log
```

**Solutions:**
1. **Script Issues:**
   - Review VersionOne test descriptions
   - Ensure Python syntax is correct
   - Check for infinite loops

2. **Position Issues:**
   ```bash
   # Manually test position detection
   python3 -c "from testTools import am_i_home; print(am_i_home())"
   ```

3. **Execution Environment:**
   - Verify script has necessary imports
   - Check for security restrictions

---

## 🔧 Advanced Diagnostics

### Enable Debug Logging
```bash
# Temporary debug mode
LOG_LEVEL=DEBUG python3 main.py

# Permanent debug mode
echo "LOG_LEVEL=DEBUG" >> .env
```

### Hardware Testing Script
```bash
# Create comprehensive test
cat > hardware_test.py << 'EOF'
#!/usr/bin/env python3
import time
from distance import check_distance
from drive import car, Direction
from ussInit import init_ultrasonic_sensor

print("=== Bender Hardware Test ===")

# Test sensor initialization
print("Testing sensor initialization...")
if init_ultrasonic_sensor():
    print("✅ Sensor initialization: PASS")
else:
    print("❌ Sensor initialization: FAIL")

# Test distance measurement
print("Testing distance measurement...")
for i in range(3):
    dist = check_distance()
    if dist:
        print(f"  Reading {i+1}: {dist}cm")
    else:
        print(f"  Reading {i+1}: FAILED")
    time.sleep(1)

# Test motor initialization
print("Testing motor initialization...")
if car.init_car("startup"):
    print("✅ Motor initialization: PASS")
    
    # Test each direction
    for direction in [Direction.FORWARD, Direction.REVERSE, Direction.LEFT, Direction.RIGHT]:
        print(f"Testing {direction.value}...")
        car.go(direction, 0.5)
        time.sleep(1)
    
    car.init_car("shutdown")
    print("✅ Motor test complete")
else:
    print("❌ Motor initialization: FAIL")

print("=== Test Complete ===")
EOF

python3 hardware_test.py
```

### Network Diagnostics
```bash
# Test VersionOne connectivity
cat > network_test.py << 'EOF'
#!/usr/bin/env python3
import requests
from constants import _INSTANCE_, _USERNAME_, _PASSWORD_

print("=== Network Connectivity Test ===")

# Test basic connectivity
try:
    response = requests.get(_INSTANCE_, timeout=10)
    print(f"✅ Instance reachable: {response.status_code}")
except Exception as e:
    print(f"❌ Instance unreachable: {e}")

# Test API endpoint
try:
    url = f"{_INSTANCE_}/rest-1.v1/Data/Test"
    response = requests.get(url, auth=(_USERNAME_, _PASSWORD_), timeout=10)
    print(f"✅ API accessible: {response.status_code}")
except Exception as e:
    print(f"❌ API error: {e}")

print("=== Network Test Complete ===")
EOF

python3 network_test.py
```

---

## 📋 Maintenance Checklist

### Daily
- [ ] Check system is running: `ps aux | grep main.py`
- [ ] Review error logs: `grep ERROR logs/bender.log | tail -5`
- [ ] Verify network connectivity
- [ ] Check physical connections

### Weekly  
- [ ] Review full log file
- [ ] Clean sensor lens
- [ ] Check battery levels
- [ ] Test hardware components
- [ ] Backup configuration

### Monthly
- [ ] Update system packages
- [ ] Update Python dependencies  
- [ ] Clean temporary files
- [ ] Review and archive logs
- [ ] Performance review

---

## 🆘 Emergency Procedures

### Immediate Stop
```bash
# Software stop
sudo pkill -TERM -f main.py

# Force stop
sudo pkill -9 -f main.py

# Physical stop
# Disconnect power/battery
```

### Recovery Mode
```bash
# Safe mode startup (minimal logging)
LOG_LEVEL=WARNING AUTOTEST=false python3 main.py

# Manual control mode
python3 -c "
from drive import car, Direction
car.init_car('startup')
# Manually control vehicle
car.go(Direction.REVERSE, 2.0)  # Move to safe position
car.init_car('shutdown')
"
```

### Factory Reset
```bash
# Backup current state
cp .env .env.emergency_backup

# Reset to defaults
cp .env.example .env

# Clear logs and temporary files
rm -f logs/bender.log script1.py *.tmp

# Reinitialize system
python3 initialize.py
```

---

*For additional support, check the main USER_GUIDE.md or create an issue on GitHub.*