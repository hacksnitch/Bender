
"""
Standalone ultrasonic sensor test script.
This file is kept for testing sensor functionality independently.
"""
import logging
import time

try:
    import RPi.GPIO as GPIO
except ImportError:
    print("Warning: RPi.GPIO not available. Running in simulation mode.")
    GPIO = None

from constants import _TRIG_, _ECHO_

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_ultrasonic_sensor():
    """Test ultrasonic sensor independently."""
    if GPIO is None:
        logger.warning("GPIO not available, cannot test sensor")
        return
    
    try:
        logger.info("Starting ultrasonic sensor test")
        
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(_TRIG_, GPIO.OUT)
        GPIO.setup(_ECHO_, GPIO.IN)

        GPIO.output(_TRIG_, False)
        logger.info("Waiting for sensor to settle...")
        time.sleep(2)

        # Send trigger pulse
        GPIO.output(_TRIG_, True)
        time.sleep(0.00001)
        GPIO.output(_TRIG_, False)

        # Measure echo timing
        while GPIO.input(_ECHO_) == 0:
            pulse_start = time.time()

        while GPIO.input(_ECHO_) == 1:
            pulse_end = time.time()

        # Calculate distance
        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17150
        distance = round(distance, 2)

        logger.info(f"Distance: {distance}cm")
        
    except Exception as e:
        logger.error(f"Error during sensor test: {e}")
    finally:
        if GPIO:
            GPIO.cleanup()
            logger.info("GPIO cleanup complete")


if __name__ == "__main__":
    test_ultrasonic_sensor()
