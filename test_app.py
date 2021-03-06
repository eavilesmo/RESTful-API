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

    # Create Spaceship Page
    # Testing if the create a spaceship option is correctly working
    def test_04_create_spaceship(self):
        response = self.app.post("/create-ship", data=dict(spaceship_life="5", spaceship_total_power="15"), follow_redirects=True)
        self.assertIn(b"The spaceship has been created! Life: 5, total power: 15", response.data)
    
    # Testing if the second option (see all spaceships) is correctly working
    def test_05_see_all_spaceships(self):
        response = self.app.post("/home", data=dict(radio_buttons="Option 2"), follow_redirects=True)
        self.assertIn(b"Spaceship 0. Life: 5, total power: 15", response.data)
    
    # Attack Page
    # Testing if the attack page is correctly created
    def test_06_attack_page(self):
        response = self.app.get("/attack", content_type="html/text")
        self.assertTrue(b"Please choose the spaceship you want to attack:" in response.data)
    
    # Testing if the attack function works correctly
    def test_07_attack_function(self):
        response = self.app.post("/create-ship", data=dict(spaceship_life="5", spaceship_total_power="15"), follow_redirects=True)
        response = self.app.post("/attack", data=dict(attacker_ship=0, attacked_ship=1), follow_redirects=True)
        self.assertTrue(b"Spaceship 1 was attacked by spaceship 0!" in response.data)
    
    # Testing if the attack function works correctly with incorrect data
    def test_08_attack_function_incorrect_data(self):
        response = self.app.post("/attack", data=dict(attacker_ship=150500, attacked_ship=450500), follow_redirects=True)
        self.assertTrue(b"The spaceship ID is not correct." in response.data)
    
    # Testing if the attack function does not work when the attacked spaceship health is 0
    def test_09_attack_function_attacked_with_no_health(self):
        for n in range(5):
            self.app.post("/attack", data=dict(attacker_ship=0, attacked_ship=1), follow_redirects=True)
        response = self.app.post("/attack", data=dict(attacker_ship=0, attacked_ship=1), follow_redirects=True)
        self.assertTrue(b"The spaceship you are trying to attack has no life left!" in response.data)
    
    # Testing if the attack function does not work when the attacker spaceship health is 0
    def test_10_attack_function_attacker_with_no_health(self):
        response = self.app.post("/attack", data=dict(attacker_ship=1, attacked_ship=0), follow_redirects=True)
        self.assertTrue(b"The attacker spaceship has no life left!" in response.data)
    
    # Testing if the attack function does not work when the attacker and the attacked spaceship is the same
    def test_11_attack_function_with_same_spaceship(self):
        response = self.app.post("/attack", data=dict(attacker_ship=0, attacked_ship=0), follow_redirects=True)
        self.assertTrue(b"The attacker spaceship and the attacked spaceship cannot be the same!" in response.data)

# Main
if __name__ == "__main__":
    unittest.main()
