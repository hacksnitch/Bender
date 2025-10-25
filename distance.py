"""Distance measurement using ultrasonic sensor."""
import logging
import time
from typing import Optional

try:
    import RPi.GPIO as GPIO
except ImportError:
    print("Warning: RPi.GPIO not available. Running in simulation mode.")
    GPIO = None

from constants import _TRIG_, _ECHO_

logger = logging.getLogger(__name__)

# Speed of sound in cm/s at room temperature
SOUND_SPEED_CM_PER_SEC = 34300


def check_distance() -> Optional[float]:
    """Measure distance using ultrasonic sensor.
    
    Returns:
        Optional[float]: Distance in centimeters, or None if measurement failed.
    """
    if GPIO is None:
        logger.warning("GPIO not available, returning simulated distance")
        return 10.0  # Simulate being close to home
        
    try:
        # Initialize sensor
        GPIO.output(_TRIG_, False)
        logger.debug("Initializing ultrasonic sensor")
        time.sleep(0.1)  # Reduced from 1 second

        # Transmit sound wave
        GPIO.output(_TRIG_, True)
        time.sleep(0.00001)
        GPIO.output(_TRIG_, False)

        # Measure echo timing with timeout protection
        pulse_start = time.time()
        timeout_start = time.time()
        
        while GPIO.input(_ECHO_) == 0:
            pulse_start = time.time()
            if time.time() - timeout_start > 1.0:  # 1 second timeout
                logger.warning("Timeout waiting for echo start")
                return None

        timeout_start = time.time()
        while GPIO.input(_ECHO_) == 1:
            pulse_end = time.time()
            if time.time() - timeout_start > 1.0:  # 1 second timeout
                logger.warning("Timeout waiting for echo end")
                return None

        # Calculate distance
        pulse_duration = pulse_end - pulse_start
        distance_cm = (pulse_duration * SOUND_SPEED_CM_PER_SEC) / 2  # Divide by 2 for round trip
        distance_cm = round(distance_cm, 2)
        
        # Convert to inches for logging
        distance_inches = round(distance_cm * 0.393701, 2)
        
        logger.info(f"Distance: {distance_cm}cm ({distance_inches}inches)")
        if distance_inches > 12:
            feet = round(distance_inches / 12, 1)
            logger.info(f"Distance: {feet} feet")
            
        return distance_cm
        
    except Exception as e:
        logger.error(f"Error measuring distance: {e}")
        return None
