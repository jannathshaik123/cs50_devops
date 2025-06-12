from django.test import TestCase, Client

from .models import Airport, Flight, Passenger
# Create your tests here.

class FlightTests(TestCase):
    
    def setUp(self):
        """Set up the test case with some initial data"""
        airport1 = Airport.objects.create(code="AAA", city="CityA")
        airport2 = Airport.objects.create(code="BBB", city="CityB")
        
        Flight.objects.create(origin=airport1, destination=airport2, duration=100)
        Flight.objects.create(origin=airport2, destination=airport1, duration=-200)
        Flight.objects.create(origin=airport1, destination=airport1, duration=150)
        
    def test_departures_count(self):
        """Test the count of departures from an airport"""
        airport = Airport.objects.get(code="AAA")
        self.assertEqual(airport.depatures.count(), 2)
        
    def test_arrivals_count(self):
        """Test the count of arrivals to an airport"""
        airport = Airport.objects.get(code="AAA")
        self.assertEqual(airport.arrivals.count(), 2)
    
    def test_valid_flight(self):
        """Test if a flight is valid"""
        flight = Flight.objects.get(origin__code="AAA", destination__code="BBB")
        self.assertTrue(flight.is_valid_flight())
        
    def test_invalid_flight(self):
        """Test if a flight is invalid"""
        flight = Flight.objects.get(origin__code="BBB", destination__code="AAA")
        self.assertFalse(flight.is_valid_flight())
        
        flight = Flight.objects.get(origin__code="AAA", destination__code="AAA")
        self.assertFalse(flight.is_valid_flight())
