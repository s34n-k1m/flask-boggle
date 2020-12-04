from unittest import TestCase

from app import app, games

from boggle import BoggleGame

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

            self.assertEqual(resp.status_code, 200)
            self.assertIn('id="newWordForm"', html)

    def test_api_new_game(self):
        """Test starting a new game."""

        with self.client as client:
            resp = client.get("/api/new-game")
            data = resp.get_json()

            self.assertEqual(resp.status_code, 200)
            self.assertIn('gameId', data)
            self.assertIsInstance(data['board'], list)
            self.assertIsInstance(data['board'][0], list)
            self.assertIn(data['gameId'], games)

    def test_api_score_word(self):
        """ Test scoring a valid word """

        with self.client as client:
            resp = client.get("/api/new-game")
            game_id = resp.get_json()['gameId']
            game = games[game_id]

            game.board = [
                ['V', 'F', 'A', 'O', 'Z'],
                ['O', 'B', 'L', 'E', 'I'],
                ['D', 'B', 'R', 'E', 'E'],
                ['A', 'L', 'I', 'Z', 'U'],
                ['R', 'L', 'E', 'R', 'I']]

            resp = client.post("/api/score-word",
                               json={'word': 'ALE', 'gameId': game_id})

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.get_json(), {'result': 'ok'})

            resp = client.post("/api/score-word",
                               json={'word': '#$@$*afafa', 'gameId': game_id})

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.get_json(), {'result': 'not-word'})

            resp = client.post("/api/score-word",
                               json={'word': 'CAT', 'gameId': game_id})

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.get_json(), {'result': 'not-on-board'})
