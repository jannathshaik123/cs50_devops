import os
import pathlib
import unittest

from selenium import webdriver
from selenium.webdriver.common.by import By

def file_uri(filename):
    return pathlib.Path(os.path.abspath(filename)).as_uri() 

driver = webdriver.Chrome()

class WebpageTest(unittest.TestCase):
    
    def test_title(self):
        driver.get(file_uri("counter.html"))
        self.assertEqual(driver.title, "Counter")
        
    def test_counter_increment(self):
        driver.get(file_uri("counter.html"))
        increment_button = driver.find_element(By.ID, "increment")
        increment_button.click()
        
        new_count = int(driver.find_element(By.TAG_NAME, "h1").text)
        self.assertEqual(new_count, 1)
        
    def test_counter_decrement(self):
        driver.get(file_uri("counter.html"))
        decrement_button = driver.find_element(By.ID, "decrement")
        decrement_button.click()
        
        new_count = int(driver.find_element(By.TAG_NAME, "h1").text)
        self.assertEqual(new_count, -1)
        
    def test_multiple_increments(self):
        driver.get(file_uri("counter.html"))
        increment_button = driver.find_element(By.ID, "increment")
        for _ in range(5):
            increment_button.click()
        
        new_count = int(driver.find_element(By.TAG_NAME, "h1").text)
        self.assertEqual(new_count, 5)

if __name__ == "__main__":
    unittest.main()