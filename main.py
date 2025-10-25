"""
Bender Autonomous Testing Vehicle
Main control loop for the autonomous RC car that integrates with VersionOne.
"""
import logging
import os
import re
import sys
import signal
from time import sleep
from typing import Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bender.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Import modules
import constants
import distance
import drive
import queryv1
import testTools
import ussInit
from constants import (
    _INSTANCE_, _RESTENDPOINT_, _POLLTIME_, 
    _AUTOTEST_, _ORIGIN_, _PASSED_, _FAILED_
)
from queryv1 import VersionOneClient
from testTools import am_i_home


class BenderController:
    """Main controller for Bender autonomous vehicle."""
    
    def __init__(self):
        self.running = True
        self.v1_client = VersionOneClient(f"{_INSTANCE_}/{_RESTENDPOINT_}")
        self.current_location = 13.0
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully."""
        logger.info(f"Received signal {signum}, shutting down...")
        self.running = False
    
    def initialize_hardware(self) -> bool:
        """Initialize car and sensor hardware.
        
        Returns:
            bool: True if initialization successful, False otherwise
        """
        logger.info("Initializing Bender hardware...")
        
        # Initialize car motors
        if not drive.init_car("startup"):
            logger.error("Failed to initialize car motors")
            return False
        
        # Initialize ultrasonic sensor
        if not ussInit.init_ultrasonic_sensor():
            logger.error("Failed to initialize ultrasonic sensor")
            return False
        
        logger.info("Hardware initialization complete")
        return True
    
    def get_initial_position(self) -> float:
        """Get initial position and move to home if needed.
        
        Returns:
            float: Current distance from home position
        """
        logger.info("Getting initial position...")
        
        current_distance = distance.check_distance()
        if current_distance is None:
            logger.warning("Could not get initial distance reading, using default")
            current_distance = self.current_location
        
        logger.info(f"Initial position: {current_distance}cm from home")
        
        # Move to home position if not already there
        if current_distance > _ORIGIN_:
            logger.info("Moving to home position...")
            current_distance = drive.go_home(_ORIGIN_, current_distance)
        
        return current_distance
    def process_test(self, test_info: dict) -> bool:
        """Process and execute a single test.
        
        Args:
            test_info: Test information from VersionOne
            
        Returns:
            bool: True if test processing successful, False otherwise
        """
        if not _AUTOTEST_:
            logger.warning("Automated testing is disabled")
            return False
        
        try:
            # Clean the test description
            cleaned_description = self.v1_client.clean_string(test_info['Desc'])
            
            # Check for GitHub repo reference
            github_match = re.search(r'^-G\s+(\w+)', cleaned_description)
            if github_match:
                repo_name = github_match.group(1)
                logger.info(f"GitHub repo reference found: {repo_name}")
                logger.warning("GitHub integration not yet implemented")
                return False
            
            # Output script to file
            if not self.v1_client.output_script_to_file(cleaned_description):
                logger.error("Failed to output script to file")
                return False
            
            # Ensure we're at home position before testing
            if self.current_location > _ORIGIN_:
                logger.info("Moving to home position before test execution")
                self.current_location = drive.go_home(_ORIGIN_, self.current_location)
            
            # Execute the test
            logger.info(f"Executing test: {test_info['Name']}")
            if not self.v1_client.exec_test("script1.py"):
                logger.error("Test execution failed")
                return False
            
            # Determine pass/fail based on final position
            test_result = _PASSED_ if am_i_home() else _FAILED_
            result_text = "PASSED" if test_result == _PASSED_ else "FAILED"
            
            logger.info(f"Test result: {result_text}")
            
            # Update test status in VersionOne
            if not self.v1_client.update_test(test_info['ID'], test_result):
                logger.error("Failed to update test status")
            
            # Update conversation with results
            if not self.v1_client.update_conversation(test_info['Number'], test_result):
                logger.error("Failed to update conversation")
            
            return True
            
        except Exception as e:
            logger.error(f"Error processing test: {e}")
            return False
    
    def run_main_loop(self):
        """Run the main control loop."""
        logger.info("Starting main control loop...")
        
        while self.running:
            try:
                # Query for available tests
                logger.debug("Querying for tests...")
                test_info = self.v1_client.query_for_tests()
                
                if test_info['Status'] == 'NOTEST':
                    logger.debug("No tests available - checking home position")
                    # Ensure we stay at home when not testing
                    current_distance = distance.check_distance()
                    if current_distance and current_distance > _ORIGIN_:
                        self.current_location = drive.go_home(_ORIGIN_, current_distance)
                else:
                    logger.info(f"Found test: {test_info['Name']} (#{test_info['Number']})")
                    self.process_test(test_info)
                
                # Sleep between polling cycles
                logger.debug(f"Sleeping for {_POLLTIME_} seconds...")
                sleep(_POLLTIME_)
                
            except KeyboardInterrupt:
                logger.info("Keyboard interrupt received")
                break
            except Exception as e:
                logger.error(f"Error in main loop: {e}")
                sleep(_POLLTIME_)  # Continue after errors
    
    def shutdown(self):
        """Gracefully shutdown the system."""
        logger.info("Shutting down Bender...")
        
        # Stop any ongoing movement
        if hasattr(drive, 'car'):
            drive.car.stop()
        
        # Cleanup GPIO
        if not drive.init_car("shutdown"):
            logger.warning("GPIO cleanup may not have completed properly")
        
        logger.info("Shutdown complete")


def main():
    """Main entry point."""
    logger.info("Starting Bender Autonomous Testing Vehicle")
    
    controller = BenderController()
    
    try:
        # Initialize hardware
        if not controller.initialize_hardware():
            logger.error("Hardware initialization failed, exiting")
            return 1
        
        # Get initial position
        controller.current_location = controller.get_initial_position()
        
        # Run main loop
        controller.run_main_loop()
        
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        return 1
    finally:
        controller.shutdown()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

	
	
			
