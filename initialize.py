"""

System initialization and setup utilities for Bender vehicle.
"""
import logging
import os
import sys
from pathlib import Path
from typing import bool

# Add the current directory to the Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

logger = logging.getLogger(__name__)


def setup_logging(log_level: str = "INFO") -> None:
    """Setup logging configuration for the application.
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    # Create logs directory if it doesn't exist
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Configure logging
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_dir / 'bender.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    logger.info(f"Logging initialized at {log_level} level")


def check_permissions() -> bool:
    """Check if the application has necessary permissions.
    
    Returns:
        bool: True if permissions are adequate, False otherwise
    """
    # Check if running as root (required for GPIO on Raspberry Pi)
    if os.geteuid() != 0:
        logger.warning("Not running as root - GPIO operations may fail")
        return False
    
    # Check write permissions for script generation
    try:
        test_file = Path("test_write_permission.tmp")
        test_file.write_text("test")
        test_file.unlink()
        logger.info("Write permissions verified")
        return True
    except PermissionError:
        logger.error("Insufficient write permissions")
        return False


def validate_configuration() -> bool:
    """Validate configuration settings.
    
    Returns:
        bool: True if configuration is valid, False otherwise
    """
    try:
        from constants import (
            _INSTANCE_, _RESTENDPOINT_, _TRIG_, _ECHO_,
            _FORWARD_PIN_, _REVERSE_PIN_, _LEFT_PIN_, _RIGHT_PIN_
        )
        
        # Validate VersionOne configuration
        if not _INSTANCE_ or not _RESTENDPOINT_:
            logger.error("VersionOne configuration is incomplete")
            return False
        
        # Validate GPIO pin configuration
        gpio_pins = [_TRIG_, _ECHO_, _FORWARD_PIN_, _REVERSE_PIN_, _LEFT_PIN_, _RIGHT_PIN_]
        if len(set(gpio_pins)) != len(gpio_pins):
            logger.error("GPIO pin conflict detected")
            return False
        
        logger.info("Configuration validation passed")
        return True
        
    except ImportError as e:
        logger.error(f"Configuration import error: {e}")
        return False


def initialize_system() -> bool:
    """Initialize the complete system.
    
    Returns:
        bool: True if initialization successful, False otherwise
    """
    logger.info("Starting system initialization...")
    
    # Setup logging
    setup_logging()
    
    # Check permissions
    if not check_permissions():
        logger.warning("Permission issues detected - some features may not work")
    
    # Validate configuration
    if not validate_configuration():
        logger.error("Configuration validation failed")
        return False
    
    # Validate environment
    from dunno import validate_environment
    if not validate_environment():
        logger.error("Environment validation failed")
        return False
    
    logger.info("System initialization complete")
    return True


if __name__ == "__main__":
    if initialize_system():
        print("System initialization successful")
        sys.exit(0)
    else:
        print("System initialization failed")
        sys.exit(1)