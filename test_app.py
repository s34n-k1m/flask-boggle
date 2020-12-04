from unittest import TestCase

from app import app, games

# Make Flask errors be real errors, not HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


class BoggleAppTestCase(TestCase):
    """Test flask app of Boggle."""

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        """Make sure information is in the session and HTML is displayed"""

        with self.client as client:
            resp = client.get('/')
            html = resp.get_data(as_text=True)

            # test that you're getting a template            
            self.assertEqual(resp.status_code, 200)
            self.assertIn('id="newWordForm"', html)


    def test_api_new_game(self):
        """Test starting a new game."""

        with self.client as client:
            # write a test for this route
            resp = client.get("/api/new-game")
            data = resp.get_json()

            self.assertEqual(resp.status_code, 200)
            self.assertIn('gameId', data)
            self.assertIsInstance(data['board'], list)
            self.assertIsInstance(data['board'][0], list)
            self.assertIn(data['gameId'], games)



