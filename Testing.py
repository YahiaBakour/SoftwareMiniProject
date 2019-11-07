import sys
import unittest
from main import app
from APIs import GooglePlacesApi,WeatherApi

class BasicTests(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        self.app = app.test_client() 
        self.assertEqual(app.debug, False)
        
###############
#### tests ####
###############
 
    def test_main_page(self):            #Not Logged In, Should go straight to Login
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_login_page(self):           #Not Logged In, Should go straight to page
        response = self.app.get('/Login', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_about_page(self):           #Not Logged In, Should go straight to page
        response = self.app.get('/aboutus', follow_redirects=False)
        self.assertEqual(response.status_code, 200)

    def test_register_page(self):       #Not Logged In, Should give a redirect to Login URL
        response = self.app.get('/RegisterPreference', follow_redirects=False)
        self.assertEqual(response.status_code, 302)

    def test_load_page(self):           #Not Logged In, Should give a redirect to Login URL
        response = self.app.get('/LoadPreference', follow_redirects=False)
        self.assertEqual(response.status_code, 302)

    def test_google_geolocation_api(self):     #Should not throw error
        self.assertIsNotNone(GooglePlacesApi.get_coords('Lisbon'))

    def test_weatherAPI(self):                  #Should not throw error
        self.assertIsNotNone(WeatherApi.returnWeatherData(GooglePlacesApi.get_coords('Lisbon')))

if __name__ == '__main__':
    unittest.main()