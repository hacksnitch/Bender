# Bender Quick Reference Card

## 🚀 Quick Start Commands

```bash
# Start Bender
cd /home/pi/Bender
source bender-env/bin/activate
sudo bender-env/bin/python3 main.py

# Stop Bender
Ctrl+C  # or SIGTERM

# View logs
tail -f logs/bender.log

# Test hardware
python3 ultrasound.py
python3 initialize.py
```

## 📋 Status Indicators

| Log Message | Meaning | Action |
|-------------|---------|---------|
| `Hardware initialization complete` | ✅ System ready | Normal operation |
| `No tests available` | ℹ️ Waiting for tests | Check VersionOne |
| `Found test: TestName` | 🎯 Executing test | Monitor progress |
| `Test result: PASSED` | ✅ Test successful | Review results |
| `Test result: FAILED` | ❌ Test failed | Check vehicle position |
| `HTTP error querying` | 🌐 API issue | Check network/credentials |
| `Timeout waiting for echo` | 📡 Sensor issue | Check sensor wiring |
| `GPIO cleanup complete` | 🛑 Clean shutdown | System stopped safely |

## 🔧 Common Fixes

| Problem | Quick Fix |
|---------|-----------|
| Permission denied | `sudo usermod -a -G gpio pi && reboot` |
| Sensor not working | Check wiring, run `python3 ultrasound.py` |
| API errors | Verify `.env` credentials and network |
| Won't move | Check battery, verify GPIO pins |
| High CPU | Increase `POLL_TIME` in `.env` |

## 📁 Important Files

| File | Purpose |
|------|---------|
| `.env` | Configuration settings |
| `logs/bender.log` | System logs |
| `script1.py` | Current test script (auto-generated) |
| `main.py` | Main application |

## 🔌 GPIO Pin Map

| Function | GPIO | Physical |
|----------|------|----------|
| Ultrasonic Trigger | 16 | 36 |
| Ultrasonic Echo | 18 | 12 |
| Motor Forward | 12 | 32 |
| Motor Reverse | 11 | 23 |
| Motor Left | 13 | 33 |
| Motor Right | 15 | 10 |

## 📞 Emergency Contacts

- **Hardware Issue**: Check connections, power cycle
- **Software Issue**: Check logs, restart application  
- **Network Issue**: Verify WiFi, check VersionOne status
- **Emergency Stop**: Disconnect power or `Ctrl+C`

---
*Keep this card handy during operations!*