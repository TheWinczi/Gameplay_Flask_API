import unittest
from unittest.mock import patch

import sys
from datetime import datetime

from api_games.src import create_app

# Start test application to initialize needed variables
APP = create_app({"TESTING": True, "INITIALIZE_MODELS": False})

from api_games.src.game.models.models import Game
from api_games.src.player.models.models import Player


class GameControllerTests(unittest.TestCase):

    APP = None

    @classmethod
    def setUpClass(cls):
        """
        Function executes once before all tests.
        """
        cls.APP = APP.test_client()

    def test_get_all_games(self):
        with patch('api_games.src.game.service.game_service.GameService.find_all') as mocked_service:
            mocked_service.return_value = [
                Game(id=1, description="Game 1"),
                Game(id=2, description="Game 2")
            ]
            games = self.APP.get('/api/games')
            mocked_service.assert_called_once()

            json = games.json
            self.assertTrue(isinstance(json, dict), "Should be possible to convert responded object to dictionary")
            self.assertEqual(games.status_code, 200, "Response code of getting existing games should be equal 200")
            self.assertTrue("games" in json.keys(), "Responded json should contain 'games' key")
            self.assertTrue(isinstance(json["games"], list), "Responded json should contain list of games available under 'games' key")

    def test_get_existing_game_with_id(self):
        with patch('api_games.src.game.service.game_service.GameService.find') as mocked_service:
            mocked_service.return_value = Game(id=1, description="Game 1", date_created=datetime.now())
            game = self.APP.get('/api/games/1')
            mocked_service.assert_called_with(1)

            json = game.json
            self.assertTrue("id" in json.keys(), "Responded json should contain 'id' key")
            self.assertTrue("date_created" in json.keys(), "Responded json should contain 'date_created' key")
            self.assertTrue("description" in json.keys(), "Responded json should contain 'description' key")

    def test_get_not_existing_game_with_id(self):
        with patch('api_games.src.game.service.game_service.GameService.find') as mocked_service:
            mocked_service.return_value = None

            game = self.APP.get(f'/api/games/{sys.maxsize}')
            mocked_service.assert_called_with(sys.maxsize)

            self.assertEqual(game.status_code, 404, "Response code of getting not existing game should be equal 404")

    def test_get_existing_game_players(self):
        with patch('api_games.src.game.service.game_service.GameService.find') as mocked_service:
            mocked_service.return_value = Game(description="Test Game Description", players=[
                Player(username="Test Player Username")
            ])

            players = self.APP.get('/api/games/1/players')
            mocked_service.assert_called_with(1)
            json = players.json

            self.assertTrue(isinstance(json, dict), "Should be possible to convert responded object to dictionary")
            self.assertEqual(players.status_code, 200, "Response code of getting existing players should be equal 200")
            self.assertTrue("players" in json.keys(), "Responded json should contain 'players' key")
            self.assertTrue(isinstance(json["players"], list), "Responded json should contain list of players available under 'players' key")

    def test_get_not_existing_game_players(self):
        with patch('api_games.src.game.service.game_service.GameService.find') as mocked_service:
            mocked_service.return_value = None

            players = self.APP.get(f'/api/games/{sys.maxsize}/players')
            mocked_service.assert_called_with(sys.maxsize)

            self.assertEqual(players.status_code, 404, "Response code of getting not existing player should be equal 404")

    def test_post_game(self):
        with patch('api_games.src.game.service.game_service.GameService.create') as mocked_service:
            mocked_service.return_value = 1

            response = self.APP.post('/api/games', data=dict(
                description="Test Game Description",
            ))
            mocked_service.assert_called()

            self.assertEqual(response.status_code, 201, "Created response status code should be equal 201")

    def test_put_existing_game(self):
        with patch('api_games.src.game.service.game_service.GameService.find') as mocked_find_service, \
                patch('api_games.src.game.service.game_service.GameService.update') as mocked_update_service:
            mocked_find_service.return_value = Game(description="Test Game Description")
            mocked_update_service.return_value = 1

            response = self.APP.put("/api/games/1", data=dict(
                description="Updated Description",
            ))
            mocked_find_service.assert_called_with(1)
            mocked_update_service.assert_called()

            self.assertEqual(response.status_code, 202, "Response code of deleting not existing game should be equal 404")

    def test_put_not_existing_game(self):
        with patch('api_games.src.game.service.game_service.GameService.find') as mocked_service:
            mocked_service.return_value = None

            response = self.APP.put(f"/api/games/{sys.maxsize}", data=dict(
                description="Updated Description"
            ))
            mocked_service.assert_called_with(sys.maxsize)
            self.assertEqual(response.status_code, 404, "Response code of updateing not existing game should be equal 404")

    def test_delete_existing_game(self):
        with patch('api_games.src.game.service.game_service.GameService.find') as mocked_find_service, \
                patch('api_games.src.game.service.game_service.GameService.delete') as mocked_delete_service:
            mocked_find_service.return_value = Game(description="Game Description")
            mocked_delete_service.return_value = 1

            response = self.APP.delete("/api/games/1")
            mocked_find_service.assert_called_with(1)
            mocked_delete_service.assert_called_with(1)

            self.assertEqual(response.status_code, 202, "Response code of deleting existing game should be equal 202")

    def test_delete_not_existing_game(self):
        with patch('api_games.src.game.service.game_service.GameService.find') as mocked_service:
            mocked_service.return_value = None

            response = self.APP.delete(f"/api/games/{sys.maxsize}")
            mocked_service.assert_called_with(sys.maxsize)
            self.assertEqual(response.status_code, 404, "Response code of deleting not existing game should be equal 404")


if __name__ == "__main__":
    unittest.main()
