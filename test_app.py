# Imports
import app
import unittest

# Classes
class FlaskTestApp(unittest.TestCase):
    def setUp(self):
        app.app.testing = True
        self.app = app.app.test_client()
        self.app.application.config['WTF_CSRF_ENABLED'] = False

    # Testing if flask is initialized correctly
    def test_01_app(self):
        response = self.app.get("/", content_type="html/text")
        self.assertEqual(response.status_code, 200)
    
    # Index Page
    # Testing if the message from the index page is correctly created
    def test_02_index(self):
        response = self.app.get("/", content_type="html/text")
        self.assertTrue(b"Welcome to FTC!" in response.data)
    
    # Home Page
    # Testing if the options from the home page are correctly created
    def test_03_home(self):
        response = self.app.get("/home", content_type="html/text")
        self.assertTrue(b"Create a new spaceship" in response.data)

    # Testing if the first option is correctly working
    def test_04_home_create_ship(self):
        response = self.app.post("/home", data=dict(radio_buttons="Option 1"), follow_redirects=True)
        self.assertIn(b"The spaceship has been created!", response.data)

# Main
if __name__ == "__main__":
    unittest.main()
