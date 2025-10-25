# Bender Autonomous Testing Vehicle

An innovative IoT project that integrates a Raspberry Pi-controlled RC car with VersionOne's Agile project management system to create an autonomous testing vehicle that can execute tests on itself.

![Bender Picture](https://github.com/user-attachments/assets/d3cffdf6-7bab-4eb8-919a-f62b0162d46c)

## Overview

Bender was originally developed during a hackweek at VersionOne. The concept is groundbreaking: an autonomous vehicle that can:

- 🚗 Navigate autonomously using ultrasonic sensors
- 📡 Poll VersionOne for available tests via REST API
- 🔄 Download and execute Python test scripts dynamically
- ✅ Report test results back to VersionOne
- 💬 Update project conversations with test outcomes

This represents an early example of **Infrastructure as Code testing** where the testing infrastructure itself becomes the test subject.

## What's New in v2.0

This repository contains a completely modernized version of the original codebase:

- ✨ **Python 3** compatibility with type hints
- 🔒 **Enhanced security** with environment-based configuration
- 📝 **Comprehensive logging** throughout the system
- 🛡️ **Robust error handling** and graceful degradation
- 🏗️ **Object-oriented architecture** with proper separation of concerns
- 🧪 **Simulation mode** for development without Raspberry Pi hardware
- 📚 **Complete documentation** and setup instructions

## Hardware Requirements

### Core Components
- **Raspberry Pi** (3B+ or newer recommended)
- **RC Car** with accessible motor controls
- **HC-SR04 Ultrasonic Sensor** for distance measurement
- **Jumper wires** for GPIO connections
- **MicroSD card** (16GB+)

### GPIO Pin Configuration
| Component | GPIO Pin | Physical Pin |
|-----------|----------|--------------|
| Ultrasonic Trigger | 16 | 36 |
| Ultrasonic Echo | 18 | 12 |
| Motor Forward | 12 | 32 |
| Motor Reverse | 11 | 23 |
| Motor Left | 13 | 33 |
| Motor Right | 15 | 10 |

## Software Setup

### 1. Prerequisites

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python 3 and pip (if not already installed)
sudo apt install python3 python3-pip python3-venv git -y

# Install GPIO library
sudo apt install python3-rpi.gpio -y
```

### 2. Clone and Setup

```bash
# Clone the repository
git clone https://github.com/hacksnitch/Bender.git
cd Bender

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit configuration (use your preferred editor)
nano .env
```

Update the `.env` file with your VersionOne credentials and any GPIO pin changes.

### 4. Initialize System

```bash
# Test system initialization
python3 initialize.py

# Run hardware tests (optional)
python3 ultrasound.py  # Test sensor
```

### 5. Run Bender

```bash
# Start the autonomous vehicle (requires sudo for GPIO)
sudo venv/bin/python3 main.py
```

## Development Mode

For development without Raspberry Pi hardware:

```bash
# The system automatically detects missing RPi.GPIO and runs in simulation mode
python3 main.py
```

## Architecture

### Core Modules

- **`main.py`** - Main control loop and system orchestration
- **`drive.py`** - Motor control and movement functions
- **`distance.py`** - Ultrasonic sensor interface
- **`queryv1.py`** - VersionOne API client
- **`constants.py`** - Configuration management
- **`initialize.py`** - System initialization and validation
- **`testTools.py`** - Test utility functions

### Key Features

- **Graceful Degradation**: Works in simulation mode without hardware
- **Secure Configuration**: Environment-based secrets management
- **Comprehensive Logging**: Full audit trail of operations
- **Error Recovery**: Robust error handling with automatic recovery
- **Signal Handling**: Graceful shutdown on SIGINT/SIGTERM
- **Type Safety**: Full type hints for better code reliability

## API Integration

### VersionOne Configuration

The system integrates with VersionOne's REST API:

```
Endpoint: https://your-instance.v1host.com/YourInstance/rest-1.v1/Data
Query: /Test?sel=Name,Number,Status.Name,Description,ID&where=(Reference="Car";-Status)
```

### Test Execution Flow

1. Poll VersionOne for tests with `Reference="Car"`
2. Download test description (Python code)
3. Generate executable script (`script1.py`)
4. Move to home position if needed
5. Execute test script
6. Determine pass/fail based on final position
7. Update test status in VersionOne
8. Post results to project conversation

## Safety Features

- **Position Validation**: Always returns to home position
- **Timeout Protection**: Prevents infinite sensor waits
- **GPIO Cleanup**: Proper GPIO cleanup on shutdown
- **Permission Checks**: Validates required system permissions
- **Hardware Detection**: Graceful handling of missing hardware

## Logging

Logs are written to both console and `logs/bender.log`:

```bash
# View real-time logs
tail -f logs/bender.log

# View specific log levels
grep "ERROR" logs/bender.log
```

## Troubleshooting

### Common Issues

1. **GPIO Permission Errors**
   ```bash
   sudo groupadd gpio
   sudo usermod -a -G gpio $USER
   # Reboot required
   ```

2. **Sensor Timeout Issues**
   - Check wiring connections
   - Verify GPIO pin configuration
   - Test with `python3 ultrasound.py`

3. **VersionOne API Errors**
   - Verify credentials in `.env`
   - Check network connectivity
   - Validate VersionOne instance URL

### Development

```bash
# Run tests (if implemented)
python3 -m pytest

# Code formatting
python3 -m black .

# Type checking
python3 -m mypy .
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Future Roadmap

- 🦀 **Rust Port**: Complete rewrite in Rust for better performance
- 🤖 **AI Integration**: Machine learning for better navigation
- 📱 **Web Interface**: Real-time monitoring dashboard
- 🔌 **Plugin System**: Extensible test framework
- 🌐 **IoT Integration**: MQTT and other IoT protocols

## License

This project is open source. Feel free to use, modify, and distribute as needed.

## Acknowledgments

- Original concept developed during VersionOne hackweek
- Inspired by autonomous vehicle testing methodologies
- Built with the Raspberry Pi and Python communities
