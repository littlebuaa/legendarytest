"""Class representing a simple test, inherit from this for a new test."""

import logging


class Test(object):
    def __init__(self, dut, name):
        self.dut = dut
        self.logger = logging.getLogger()
        self.name = name

    def run(self):
        """Run the test and return True if it passes, False otherwise."""
        self.logger.info("--------------- Test '%s' start ---------------", self.name)
        if self.test():
            self.logger.info("--------------- Test '%s' PASS ---------------", self.name)
            return True
        else:
            self.logger.info("--------------- Test '%s' FAIL ---------------", self.name)
            return False

    def test(self):
        """Implement test specific code here"""
        self.logger.info("WARNING: Test function for test '%s' not implemented!", self.name)
        return False

class TestResult(object):
    def __init__(self, status, data):
        """ status  :  True or False
            data :  a list of data list for csv.
            like    [
                        [test_item_1,value, range, result],
                        [test_item_2,value, range, result],
                    ]
        """
        self.data = data
        self.status = status
