import unittest

from prime import is_prime

class Test(unittest.TestCase):
    """_summary_

    Args:
        unittest (_type_): _description_
    """
    def test_1(self):
        """Test if 1 is prime"""
        self.assertFalse(is_prime(1))
        
    def test_2(self):
        """Test if 2 is prime"""
        self.assertTrue(is_prime(2))
    
    def test_8(self):
        """Test if 8 is prime"""
        self.assertFalse(is_prime(8))
    
    def test_13(self):
        """Test if 13 is prime"""
        self.assertTrue(is_prime(13))
    
    def test_25 (self):
        """Test if 25 is prime"""
        self.assertFalse(is_prime(25))
        
    def test_28(self):
        """Test if 28 is prime"""
        self.assertFalse(is_prime(28))
    
if __name__ == '__main__':
    unittest.main()