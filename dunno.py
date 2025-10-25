"""
Utility functions and experimental code for Bender vehicle.
This file contains helper functions that don't fit in other modules.
"""
import logging
import sys
import os
from typing import Any, Dict

logger = logging.getLogger(__name__)


def safe_exit(exit_code: int = 0) -> None:
    """Safely exit the application with proper cleanup.
    
    Args:
        exit_code: Exit code to return to the system
    """
    logger.info(f"Safely exiting with code {exit_code}")
    try:
        sys.exit(exit_code)
    except SystemExit:
        os._exit(exit_code)


def log_system_info() -> Dict[str, Any]:
    """Log system information for debugging purposes.
    
    Returns:
        Dict containing system information
    """
    import platform
    
    info = {
        'platform': platform.system(),
        'version': platform.version(),
        'machine': platform.machine(),
        'python_version': platform.python_version(),
    }
    
    logger.info(f"System info: {info}")
    return info


def validate_environment() -> bool:
    """Validate that the environment is properly configured.
    
    Returns:
        bool: True if environment is valid, False otherwise
    """
    try:
        # Check if we're on a Raspberry Pi
        with open('/proc/cpuinfo', 'r') as f:
            cpuinfo = f.read()
            is_raspberry_pi = 'BCM' in cpuinfo or 'Raspberry Pi' in cpuinfo
        
        if not is_raspberry_pi:
            logger.warning("Not running on Raspberry Pi - GPIO functionality will be limited")
        
        # Check for required modules
        required_modules = ['requests', 'html2text']
        missing_modules = []
        
        for module in required_modules:
            try:
                __import__(module)
            except ImportError:
                missing_modules.append(module)
        
        if missing_modules:
            logger.error(f"Missing required modules: {missing_modules}")
            return False
        
        logger.info("Environment validation passed")
        return True
        
    except Exception as e:
        logger.error(f"Error validating environment: {e}")
        return False
