import pdb

def add_numbers(x, y):
    result = x + y
    pdb.set_trace() # Start the debugger at this point in the code
    return result

result = add_numbers(2, 3)
print(result)



import unittest

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, n):
        if n % i == 0:
            return False
    return True

class TestIsPrime(unittest.TestCase):
    def test_is_prime(self):
        self.assertTrue(is_prime(2))
        self.assertTrue(is_prime(3))
        self.assertTrue(is_prime(5))
        self.assertFalse(is_prime(4))

if __name__ == '__main__':
    unittest.main()



#Regular expressions:

import re

# Search for a phone number in a string
text = 'My phone number is 555-7777'
match = re.search(r'\d{3}-\d{4}', text)
if match:
    print(match.group(0))

# Extract email addresses from a string
text = 'My email is example@devops.com, but I also use other@cloud.com'
matches = re.findall(r'\S+@\S+', text)
print(matches)



#Datetime library:

from datetime import datetime, timedelta

# Get the current date and time
now = datetime.now()
print(now) # Output: 2023-02-17 11:33:27.257712

# Create a datetime object for a specific date and time
date = datetime(2023, 2, 1, 12, 0)
print(date) # Output: 2023-02-01 12:00:00

# Calculate the difference between two dates
delta = now - date
print(delta) # Output: 15 days, 23:33:27.257712
