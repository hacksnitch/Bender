"""Configuration constants for Bender autonomous testing vehicle."""
import os
from typing import Final

# VersionOne API Configuration
_INSTANCE_: Final[str] = os.getenv("V1_INSTANCE", "https://www11.v1host.com/VersionOneMi")
_RESTENDPOINT_: Final[str] = "rest-1.v1/Data"
_USERNAME_: Final[str] = os.getenv("V1_USERNAME", "admin")
_PASSWORD_: Final[str] = os.getenv("V1_PASSWORD", "admin")

# System Configuration
_AUTOTEST_: Final[bool] = True
_POLLTIME_: Final[int] = 5
_CTR_: Final[int] = 0

# GPIO Pin Configuration
_TRIG_: Final[int] = 16
_ECHO_: Final[int] = 18

# Motor GPIO Pins
_REVERSE_PIN_: Final[int] = 11
_FORWARD_PIN_: Final[int] = 12
_LEFT_PIN_: Final[int] = 13
_RIGHT_PIN_: Final[int] = 15

# VersionOne Test Status IDs
_PASSED_: Final[str] = "TestStatus:129"
_FAILED_: Final[str] = "TestStatus:155"
_CLOSED_: Final[str] = "TestStatus:1413"

# Physical Configuration
_ORIGIN_: Final[float] = 15.0  # Origin position in centimeters
