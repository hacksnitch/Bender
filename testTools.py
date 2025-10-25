"""Test utility functions for Bender vehicle."""
import logging
from typing import bool

from distance import check_distance
from constants import _ORIGIN_

logger = logging.getLogger(__name__)


def am_i_home() -> bool:
    """Check if the vehicle is at the home position.
    
    Returns:
        bool: True if vehicle is at or within origin distance, False otherwise.
    """
    try:
        current_distance = check_distance()
        is_home = current_distance <= _ORIGIN_
        
        if is_home:
            logger.info(f"Vehicle is home (distance: {current_distance}cm)")
        else:
            logger.info(f"Vehicle is away from home (distance: {current_distance}cm)")
            
        return is_home
    except Exception as e:
        logger.error(f"Error checking home position: {e}")
        return False
