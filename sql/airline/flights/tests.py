from django.test import TestCase, Client
from django.db import models
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
        
    def test_index(self):
        """Test the index view"""
        client = Client()
        response = client.get('/flights/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['flights'].count(), 3)
        
    def test_valid_flight_detail(self):
        """Test the flight detail view"""
        client = Client()
        flight = Flight.objects.get(origin__code="AAA", destination__code="BBB")
        response = client.get(f'/flights/{flight.id}')
        self.assertEqual(response.status_code, 200)
        
    def test_invalid_flight_detail(self):
        """Test the flight detail view with an invalid flight ID"""
        client = Client()
        max_flight_id = Flight.objects.aggregate(models.Max('id'))['id__max']
        
        response = client.get(f'/flights/{max_flight_id + 1}')
        self.assertEqual(response.status_code, 404) # Assuming 500 for invalid flight ID, adjust as needed
        
    def test_flight_passengers(self):
        """Test the flight passengers view"""
        client = Client()
        flight = Flight.objects.get(origin__code="AAA", destination__code="BBB")
        passenger1 = Passenger.objects.create(first="John", last="Doe")
        passenger2 = Passenger.objects.create(first="Jane", last="Smith")
        flight.passengers.add(passenger1, passenger2)
        
        response = client.get(f'/flights/{flight.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['passengers'].count(), 2)
        
    def test_non_passengers(self):
        """Test the non-passengers view"""
        client = Client()
        flight = Flight.objects.get(origin__code="AAA", destination__code="BBB")
        passenger1 = Passenger.objects.create(first="Jane", last="Doe")
        response = client.get(f'/flights/{flight.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['non_passengers'].count(), 1)