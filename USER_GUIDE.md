# Bender Autonomous Testing Vehicle - User Guide

## Table of Contents
1. [Getting Started](#getting-started)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Daily Operations](#daily-operations)
5. [Monitoring & Troubleshooting](#monitoring--troubleshooting)
6. [Advanced Usage](#advanced-usage)
7. [Maintenance](#maintenance)
8. [FAQ](#faq)

---

## Getting Started

### What is Bender?

Bender is an autonomous RC car that integrates with VersionOne (now CollabNet VersionOne) to automatically execute tests. The vehicle:

- Polls your VersionOne instance for new tests
- Downloads test scripts dynamically
- Executes tests on itself (movement, sensor validation)
- Reports results back to VersionOne
- Updates project conversations with outcomes

### Prerequisites

Before you begin, ensure you have:

- **Hardware**: Raspberry Pi (3B+ or newer) with RC car and ultrasonic sensor
- **Software**: VersionOne instance with API access
- **Network**: WiFi connection for API communication
- **Permissions**: Administrator access to Raspberry Pi

---

## Installation

### Step 1: Prepare Raspberry Pi

```bash
# Update your Raspberry Pi
sudo apt update && sudo apt upgrade -y

# Install required system packages
sudo apt install python3 python3-pip python3-venv git -y

# Install GPIO library
sudo apt install python3-rpi.gpio -y
```

### Step 2: Download Bender

```bash
# Navigate to your preferred directory
cd /home/pi

# Clone the repository
git clone https://github.com/hacksnitch/Bender.git
cd Bender
```

### Step 3: Setup Python Environment

```bash
# Create virtual environment
python3 -m venv bender-env

# Activate environment
source bender-env/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 4: Hardware Setup

Connect your hardware according to this wiring diagram:

| Component | GPIO Pin | Physical Pin | Wire Color (typical) |
|-----------|----------|--------------|---------------------|
| Ultrasonic Trigger | 16 | 36 | Orange |
| Ultrasonic Echo | 18 | 12 | Yellow |
| Motor Forward | 12 | 32 | Green |
| Motor Reverse | 11 | 23 | Blue |
| Motor Left | 13 | 33 | Purple |
| Motor Right | 15 | 10 | Gray |
| Ground | GND | 6,9,14,20,25,30,34,39 | Black |
| 5V Power | 5V | 2,4 | Red |

---

## Configuration

### Step 1: Create Configuration File

```bash
# Copy the example configuration
cp .env.example .env

# Edit the configuration
nano .env
```

### Step 2: Configure VersionOne Integration

Update your `.env` file with your VersionOne details:

```bash
# VersionOne API Configuration
V1_INSTANCE=https://your-instance.v1host.com/YourInstance
V1_USERNAME=your_api_username
V1_PASSWORD=your_api_password

# System Configuration
AUTOTEST=true
POLL_TIME=5
LOG_LEVEL=INFO

# Physical Configuration (adjust if needed)
ORIGIN_DISTANCE=15.0
```

### Step 3: Test Configuration

```bash
# Test system initialization
python3 initialize.py

# Expected output:
# System initialization successful
```

### Step 4: Hardware Validation

```bash
# Test ultrasonic sensor
python3 ultrasound.py

# Expected output:
# Distance: XX.XX cm (X.XX inches)
```

---

## Daily Operations

### Starting Bender

```bash
# Navigate to Bender directory
cd /home/pi/Bender

# Activate virtual environment
source bender-env/bin/activate

# Start Bender (requires sudo for GPIO)
sudo bender-env/bin/python3 main.py
```

### Normal Operation Flow

1. **Startup**: Bender initializes hardware and moves to home position
2. **Polling**: Every 5 seconds, checks VersionOne for new tests
3. **Test Execution**: When a test is found:
   - Downloads the test script
   - Moves to home position
   - Executes the test
   - Reports results
4. **Standby**: Returns to polling mode

### Stopping Bender

To safely stop Bender:

- **Method 1**: Press `Ctrl+C` in the terminal
- **Method 2**: Send SIGTERM: `sudo pkill -TERM -f main.py`

The system will:
- Stop all motor movement
- Clean up GPIO resources
- Save final logs
- Exit gracefully

---

## Monitoring & Troubleshooting

### Log Files

Bender creates detailed logs in the `logs/` directory:

```bash
# View real-time logs
tail -f logs/bender.log

# Search for errors
grep "ERROR" logs/bender.log

# Search for specific operations
grep "test" logs/bender.log
```

### Log Levels

- **DEBUG**: Detailed technical information
- **INFO**: General operational messages
- **WARNING**: Potential issues that don't stop operation
- **ERROR**: Problems that affect functionality
- **CRITICAL**: Severe problems that stop the system

### Common Issues and Solutions

#### 1. GPIO Permission Errors

**Problem**: `Permission denied` when accessing GPIO

**Solution**:
```bash
# Add user to gpio group
sudo usermod -a -G gpio pi

# Reboot required
sudo reboot

# Alternative: Run with sudo
sudo bender-env/bin/python3 main.py
```

#### 2. Sensor Timeout Issues

**Problem**: `Timeout waiting for echo` messages

**Solutions**:
- Check physical connections
- Ensure sensor has clear line of sight
- Verify GPIO pin configuration in `.env`
- Test sensor independently: `python3 ultrasound.py`

#### 3. VersionOne API Errors

**Problem**: `HTTP error querying for tests`

**Solutions**:
- Verify network connectivity: `ping your-v1-instance.com`
- Check credentials in `.env` file
- Validate VersionOne instance URL
- Test API manually: `curl -u username:password "https://your-instance/rest-1.v1/Data/Test"`

#### 4. Motor Control Issues

**Problem**: Vehicle doesn't move or moves incorrectly

**Solutions**:
- Check motor wiring connections
- Verify GPIO pin assignments match your hardware
- Test individual pins with multimeter
- Check battery levels

#### 5. High CPU Usage

**Problem**: System becomes sluggish

**Solutions**:
- Increase `POLL_TIME` in `.env` (default: 5 seconds)
- Check for infinite loops in generated test scripts
- Monitor with: `top -p $(pgrep -f main.py)`

---

## Advanced Usage

### Custom Test Scripts

VersionOne test descriptions can contain Python code that Bender will execute. Example:

```python
# Test Description in VersionOne:
import time
from drive import car, Direction

# Move forward for 2 seconds
car.go(Direction.FORWARD, 2.0)
time.sleep(1)

# Move backward to return home
car.go(Direction.REVERSE, 2.0)
```

### GitHub Integration (Future Feature)

Tests can reference GitHub repositories:

```
-G repository_name
```

This will clone and execute tests from the specified repository.

### Development Mode

For development without Raspberry Pi hardware:

```bash
# Run on any system - GPIO operations will be simulated
python3 main.py
```

### Custom Configuration

You can override any configuration with environment variables:

```bash
# Temporary override
POLL_TIME=10 LOG_LEVEL=DEBUG python3 main.py

# Or add to your shell profile
export BENDER_LOG_LEVEL=DEBUG
```

---

## Maintenance

### Regular Maintenance Tasks

#### Daily
- Check log files for errors
- Verify system is responding to tests
- Clean sensor lens if needed

#### Weekly
- Review accumulated logs: `logrotate logs/bender.log`
- Check battery levels
- Inspect physical connections

#### Monthly
- Update system packages: `sudo apt update && sudo apt upgrade`
- Update Python dependencies: `pip install -r requirements.txt --upgrade`
- Clean temporary files: `rm -f *.tmp script1.py`

### Backup Configuration

```bash
# Backup your configuration
cp .env .env.backup.$(date +%Y%m%d)

# Backup custom modifications
tar -czf bender-backup-$(date +%Y%m%d).tar.gz *.py .env logs/
```

### System Health Check

```bash
# Run comprehensive system check
python3 initialize.py

# Check disk space
df -h

# Check memory usage
free -h

# Check system temperature (Raspberry Pi)
vcgencmd measure_temp
```

---

## FAQ

### Q: Can I run multiple Bender instances?

**A**: Not recommended on the same hardware due to GPIO conflicts. You can run one instance per Raspberry Pi.

### Q: How do I change the polling frequency?

**A**: Update `POLL_TIME` in your `.env` file. Value is in seconds.

### Q: What happens if WiFi disconnects?

**A**: Bender will continue running but cannot communicate with VersionOne. It will retry connections automatically.

### Q: Can I customize the home position?

**A**: Yes, adjust `ORIGIN_DISTANCE` in `.env`. Value is in centimeters from the nearest obstacle.

### Q: How do I add custom sensors?

**A**: Modify the appropriate modules (`distance.py`, `constants.py`) and add your sensor logic. Ensure GPIO pins don't conflict.

### Q: What's the maximum test execution time?

**A**: No hard limit, but tests should include their own timeouts. The system will continue polling for new tests regardless.

### Q: Can I use this with other project management tools?

**A**: Currently only VersionOne is supported. The API integration is in `queryv1.py` - you could adapt this for other systems.

### Q: How do I contribute to the project?

**A**: Fork the repository on GitHub, make your changes, and submit a pull request. See the main README for contribution guidelines.

---

## Support

For additional support:

1. Check the logs: `logs/bender.log`
2. Review this documentation
3. Check the main README.md
4. Create an issue on GitHub
5. Review the source code - it's well-documented!

## Emergency Procedures

### Emergency Stop

If Bender is moving erratically:

1. **Physical**: Disconnect power/battery
2. **Software**: `Ctrl+C` in terminal
3. **Remote**: `sudo pkill -9 python3` (from SSH)

### Reset to Factory Settings

```bash
# Stop Bender
sudo pkill -TERM -f main.py

# Reset configuration
cp .env.example .env

# Clear logs
rm -f logs/bender.log

# Reinitialize
python3 initialize.py
```

---

*This documentation covers Bender v2.0. For older versions, please refer to the git history.*