"""Motor control and driving functions for Bender vehicle."""
import logging
import time
from typing import Optional, Literal
from enum import Enum

try:
    import RPi.GPIO as GPIO
except ImportError:
    print("Warning: RPi.GPIO not available. Running in simulation mode.")
    GPIO = None

from constants import (_REVERSE_PIN_, _FORWARD_PIN_, _LEFT_PIN_, _RIGHT_PIN_)
import distance

logger = logging.getLogger(__name__)


class Direction(Enum):
    """Valid movement directions."""
    REVERSE = "reverse"
    FORWARD = "forward"
    LEFT = "left"
    RIGHT = "right"
    STOP = "stop"


class CarController:
    """Controls the RC car motors and movement."""
    
    def __init__(self):
        self.is_initialized = False
        
    def init_car(self, mode: Literal["startup", "shutdown"]) -> bool:
        """Initialize or shutdown car GPIO pins.
        
        Args:
            mode: Either "startup" to initialize or "shutdown" to cleanup
            
        Returns:
            bool: True if operation successful, False otherwise
        """
        if GPIO is None:
            logger.warning("GPIO not available, skipping car initialization")
            return False
            
        try:
            if mode == "startup":
                GPIO.setmode(GPIO.BOARD)
                
                # Setup motor control pins
                GPIO.setup(_REVERSE_PIN_, GPIO.OUT)  # Reverse
                GPIO.setup(_FORWARD_PIN_, GPIO.OUT)  # Forward
                GPIO.setup(_LEFT_PIN_, GPIO.OUT)     # Left
                GPIO.setup(_RIGHT_PIN_, GPIO.OUT)    # Right
                
                # Ensure all motors are off initially
                self.stop()
                self.is_initialized = True
                logger.info("Car initialization successful")
                return True
                
            elif mode == "shutdown":
                if self.is_initialized:
                    self.stop()  # Stop all motors before cleanup
                    GPIO.cleanup()
                    self.is_initialized = False
                    logger.info("Car GPIO cleanup successful")
                return True
                
        except Exception as e:
            logger.error(f"Error during car {mode}: {e}")
            return False
            
        return False
    
    def go(self, direction: Direction, interval: float) -> bool:
        """Move the car in specified direction for given time.
        
        Args:
            direction: Direction to move
            interval: Time in seconds to move
            
        Returns:
            bool: True if movement successful, False otherwise
        """
        if GPIO is None:
            logger.info(f"Simulating movement: {direction.value} for {interval}s")
            time.sleep(interval)
            return True
            
        if not self.is_initialized:
            logger.error("Car not initialized")
            return False
            
        try:
            pin_map = {
                Direction.REVERSE: _REVERSE_PIN_,
                Direction.FORWARD: _FORWARD_PIN_,
                Direction.LEFT: _LEFT_PIN_,
                Direction.RIGHT: _RIGHT_PIN_,
            }
            
            if direction == Direction.STOP:
                self.stop()
                return True
                
            if direction in pin_map:
                pin = pin_map[direction]
                GPIO.output(pin, GPIO.HIGH)
                time.sleep(interval)
                GPIO.output(pin, GPIO.LOW)
                logger.debug(f"Moved {direction.value} for {interval}s")
                return True
            else:
                logger.error(f"Invalid direction: {direction}")
                return False
                
        except Exception as e:
            logger.error(f"Error during movement: {e}")
            return False
    
    def stop(self) -> None:
        """Stop all motors."""
        if GPIO is not None and self.is_initialized:
            try:
                all_pins = [_REVERSE_PIN_, _FORWARD_PIN_, _LEFT_PIN_, _RIGHT_PIN_]
                for pin in all_pins:
                    GPIO.output(pin, GPIO.LOW)
                logger.debug("All motors stopped")
            except Exception as e:
                logger.error(f"Error stopping motors: {e}")
    
    def go_home(self, home_distance: float, current_distance: float) -> float:
        """Navigate back to home position using reverse movement.
        
        Args:
            home_distance: Target distance from obstacle (home position)
            current_distance: Current distance from obstacle
            
        Returns:
            float: Final distance after movement
        """
        if GPIO is None:
            logger.info("Simulating go_home movement")
            return home_distance
            
        logger.info(f"Navigating home: current={current_distance}cm, target={home_distance}cm")
        
        try:
            while current_distance > home_distance:
                # Use PWM for more controlled movement
                pwm = GPIO.PWM(_REVERSE_PIN_, 4)  # 4Hz frequency
                pwm.start(35)  # 35% duty cycle
                time.sleep(1)
                pwm.stop()
                
                # Check new distance
                new_distance = distance.check_distance()
                if new_distance is None:
                    logger.warning("Failed to get distance reading, stopping")
                    break
                    
                current_distance = new_distance
                logger.info(f"{current_distance}cm away, moving toward home")
                
                # Safety check to prevent infinite loop
                if current_distance > 100:  # If we're more than 1m away, something's wrong
                    logger.error("Distance reading seems incorrect, stopping")
                    break
                    
        except Exception as e:
            logger.error(f"Error during go_home: {e}")
            
        logger.info(f"Final position: {current_distance}cm from home")
        return current_distance


# Global car controller instance
car = CarController()

# Legacy function wrappers for backward compatibility
def init_car(mode: str) -> bool:
    """Legacy wrapper for car initialization."""
    return car.init_car(mode)

def go_home(home: float, current: float) -> float:
    """Legacy wrapper for go_home functionality."""
    return car.go_home(home, current)
	

