"""Ultrasonic sensor initialization module."""
import logging
import sys
from typing import bool

try:
    import RPi.GPIO as GPIO
except ImportError:
    print("Warning: RPi.GPIO not available. Running in simulation mode.")
    GPIO = None

from constants import _TRIG_, _ECHO_

logger = logging.getLogger(__name__)


def init_ultrasonic_sensor() -> bool:
    """Initialize ultrasonic sensor GPIO pins.
    
    Returns:
        bool: True if initialization successful, False otherwise.
    """
    if GPIO is None:
        logger.warning("GPIO not available, skipping ultrasonic sensor initialization")
        return False
        
    try:
        GPIO.setup(_TRIG_, GPIO.OUT)
        GPIO.setup(_ECHO_, GPIO.IN)
        logger.info("Ultrasonic sensor setup successful")
        return True
    except Exception as e:
        logger.error(f"Error setting up ultrasonic sensor: {e}")
        return False 

