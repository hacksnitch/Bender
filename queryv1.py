"""VersionOne API integration for test management."""
import logging
import re
import types
from typing import Dict, Optional, Any
from xml.etree import ElementTree as ET

import html2text
import requests
from requests.auth import HTTPBasicAuth

from constants import _USERNAME_, _PASSWORD_

logger = logging.getLogger(__name__)


class VersionOneClient:
    """Client for interacting with VersionOne API."""
    
    def __init__(self, instance_endpoint: str, username: str = None, password: str = None):
        self.instance_endpoint = instance_endpoint
        self.auth = HTTPBasicAuth(
            username or _USERNAME_,
            password or _PASSWORD_
        )
        self.session = requests.Session()
        self.session.auth = self.auth
    
    def query_for_tests(self) -> Dict[str, str]:
        """Query VersionOne for available tests.
        
        Returns:
            Dict[str, str]: Test information or NOTEST if no tests found.
        """
        query = '?sel=Name,Number,Status.Name,Description,ID&where=(Reference="Car";-Status)'
        url = f"{self.instance_endpoint}/Test{query}"
        
        try:
            logger.debug(f"Querying for tests: {url}")
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            # Check if we have a meaningful response
            if len(response.text) <= 150:
                logger.info("No tests found in designated folder")
                return self._no_test_response()
            
            # Parse XML response
            tree = ET.ElementTree(ET.fromstring(response.content))
            root = tree.getroot()
            
            if len(root) == 0:
                logger.info("No test elements found in response")
                return self._no_test_response()
            
            # Extract test information
            test_element = root[0]
            name = self._safe_get_text(test_element, 0, "Unknown")
            number = self._safe_get_text(test_element, 1, "-1")
            status = self._safe_get_text(test_element, 2, "Unknown")
            description = self._safe_get_text(test_element, 3, "")
            
            # Extract OID from ID attribute
            oid = self._extract_oid(test_element.attrib.get('id', ''))
            
            test_info = {
                'Name': name,
                'Number': number,
                'Status': status,
                'Desc': description,
                'ID': oid
            }
            
            logger.info(f"Found test: {name} (#{number})")
            return test_info
            
        except requests.RequestException as e:
            logger.error(f"HTTP error querying for tests: {e}")
            return self._no_test_response()
        except ET.ParseError as e:
            logger.error(f"XML parsing error: {e}")
            return self._no_test_response()
        except Exception as e:
            logger.error(f"Unexpected error querying for tests: {e}")
            return self._no_test_response()
    
    def _safe_get_text(self, element: ET.Element, index: int, default: str) -> str:
        """Safely extract text from XML element at given index."""
        try:
            return element[index].text or default
        except (IndexError, AttributeError):
            return default
    
    def _extract_oid(self, id_string: str) -> str:
        """Extract OID from VersionOne ID string."""
        if not id_string:
            return "NOTEST"
        
        match = re.search(r'Test:([0-9]+)', id_string)
        return match.group(1) if match else "NOTEST"
    
    def _no_test_response(self) -> Dict[str, str]:
        """Return standard no-test response."""
        return {
            'Name': 'NOTEST',
            'Number': '-1',
            'Status': 'NOTEST',
            'Desc': 'NOTEST',
            'ID': 'NOTEST'
        }

    def clean_string(self, dirty_string: str) -> str:
        """Clean HTML from string content.
        
        Args:
            dirty_string: String potentially containing HTML
            
        Returns:
            str: Cleaned string with HTML removed
        """
        try:
            return html2text.html2text(dirty_string)
        except Exception as e:
            logger.error(f"Error cleaning string: {e}")
            return dirty_string
    
    def output_script_to_file(self, code: str, filename: str = "script1.py") -> bool:
        """Output code to a Python script file for dynamic execution.
        
        Args:
            code: Python code to write to file
            filename: Target filename
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            with open(filename, "w", encoding="utf-8") as file:
                file.write(code)
            logger.info(f"Saved script to {filename}")
            return True
        except Exception as e:
            logger.error(f"Error writing script to file: {e}")
            return False
    
    def update_test(self, oid: str, pass_fail_status: str) -> bool:
        """Update test status in VersionOne.
        
        Args:
            oid: Test object ID
            pass_fail_status: Status to set (PASSED or FAILED)
            
        Returns:
            bool: True if update successful, False otherwise
        """
        url = f"{self.instance_endpoint}/Test/{oid}"
        payload = f'<Asset><Relation name="Status" act="set"><Asset idref="{pass_fail_status}"/></Relation></Asset>'
        
        try:
            response = self.session.post(url, data=payload, timeout=30)
            response.raise_for_status()
            logger.info(f"Updated test {oid} with status {pass_fail_status}")
            return True
        except requests.RequestException as e:
            logger.error(f"Error updating test: {e}")
            return False
    
    def exec_test(self, filename: str) -> bool:
        """Execute a Python test script dynamically.
        
        Args:
            filename: Path to Python script to execute
            
        Returns:
            bool: True if execution successful, False otherwise
        """
        try:
            logger.info(f"Executing test script: {filename}")
            with open(filename, "r", encoding="utf-8") as file_ptr:
                source_code = file_ptr.read()
            
            # Compile and execute in isolated module
            compiled_code = compile(source_code, filename, "exec")
            test_module = types.ModuleType("<test_module>")
            
            # Execute with limited globals for security
            safe_globals = {
                '__builtins__': {
                    'print': print,
                    'len': len,
                    'str': str,
                    'int': int,
                    'float': float,
                    'bool': bool,
                    'range': range,
                    'time': __import__('time'),
                }
            }
            
            exec(compiled_code, safe_globals, test_module.__dict__)
            logger.info("Test script executed successfully")
            return True
            
        except FileNotFoundError:
            logger.error(f"Test script not found: {filename}")
            return False
        except Exception as e:
            logger.error(f"Error executing test script: {e}")
            return False
    
    def update_conversation(self, test_number: str, pass_fail_status: str) -> bool:
        """Update conversation with test results.
        
        Args:
            test_number: Test number for reference
            pass_fail_status: Test result status
            
        Returns:
            bool: True if update successful, False otherwise
        """
        from datetime import datetime
        
        status_text = "PASSED" if "129" in pass_fail_status else "FAILED"
        message = f"Ran test #{test_number} - Result: {status_text}. Executed by Bender autonomous vehicle."
        current_time = datetime.now().isoformat()
        
        url = f"{self.instance_endpoint}/Expression"
        payload = f'''<Asset>
            <Relation name="Author" act="set"><Asset idref="Member:20" /></Relation>
            <Attribute name="AuthoredAt">{current_time}</Attribute>
            <Attribute name="Content" act="set">{message}</Attribute>
            <Relation name="InReplyTo" act="set"><Asset idref="Expression:27605" /></Relation>
        </Asset>'''
        
        try:
            response = self.session.post(url, data=payload, timeout=30)
            response.raise_for_status()
            logger.info(f"Updated conversation with test result: {status_text}")
            return True
        except requests.RequestException as e:
            logger.error(f"Error updating conversation: {e}")
            return False


# Legacy function wrappers for backward compatibility
def QueryForTests(instance_endpoint: str) -> Dict[str, str]:
    """Legacy wrapper for querying tests."""
    client = VersionOneClient(instance_endpoint)
    return client.query_for_tests()

def cleanString(dirty_string: str) -> str:
    """Legacy wrapper for string cleaning."""
    client = VersionOneClient("")
    return client.clean_string(dirty_string)

def outputScriptToFile(code: str) -> bool:
    """Legacy wrapper for script output."""
    client = VersionOneClient("")
    return client.output_script_to_file(code)

def updateTest(instance_endpoint: str, oid: str, pass_fail: str) -> bool:
    """Legacy wrapper for test updates."""
    client = VersionOneClient(instance_endpoint)
    return client.update_test(oid, pass_fail)

def execTest(filename: str) -> bool:
    """Legacy wrapper for test execution."""
    client = VersionOneClient("")
    return client.exec_test(filename)

def updateConversation(instance_endpoint: str, number: str, pass_fail: str) -> bool:
    """Legacy wrapper for conversation updates."""
    client = VersionOneClient(instance_endpoint)
    return client.update_conversation(number, pass_fail)

