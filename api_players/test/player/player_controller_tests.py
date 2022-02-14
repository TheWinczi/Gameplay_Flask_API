import unittest
from unittest.mock import patch

import sys
from datetime import datetime

from api_players.src import create_app

# Start test application to initialize needed variables
APP = create_app({"TESTING": True, "INITIALIZE_MODELS": False})

from api_players.src.player.models.models import Player
from api_players.src.player.service.player_service import PlayerService


class PlayerControllerTests(unittest.TestCase):

    APP = None

    @classmethod
    def setUpClass(cls):
        """
        Function executes once before all tests.
        """
        cls.APP = APP.test_client()

    def test_get_all_players(self):
        with patch('api_players.src.player.service.player_service.PlayerService.find_all') as mocked_service:
            mocked_service.return_value = [
                Player(id=1, username="Player 1"),
                Player(id=2, username="Player 2")
            ]
            players = self.APP.get('/api/players')
            mocked_service.assert_called_once()

            json = players.json
            self.assertTrue(isinstance(json, dict), "Should be possible to convert responded object to dictionary")
            self.assertEqual(players.status_code, 200, "Response code of getting existing players should be equal 200")
            self.assertTrue("players" in json.keys(), "Responded json should contain 'players' key")
            self.assertTrue(isinstance(json["players"], list), "Responded json should contain list of players available under 'players' key")

    def test_get_existing_player_with_id(self):
        with patch('api_players.src.player.service.player_service.PlayerService.find') as mocked_service:
            mocked_service.return_value = Player(id=1, username="Player 1", image_file="default.jpg",
                                                 date_created=datetime.now(), date_modified=datetime.now())
            player = self.APP.get('/api/players/1')
            mocked_service.assert_called_with(1)

            json = player.json
            self.assertTrue("id" in json.keys(), "Responded json should contain 'id' key")
            self.assertTrue("date_created" in json.keys(), "Responded json should contain 'date_created' key")
            self.assertTrue("date_modified" in json.keys(), "Responded json should contain 'date_modified' key")
            self.assertTrue("username" in json.keys(), "Responded json should contain 'username' key")
            self.assertTrue("image_file" in json.keys(), "Responded json should contain 'image_file' key")

    def test_get_not_existing_player_with_id(self):
        with patch('api_players.src.player.service.player_service.PlayerService.find') as mocked_service:
            mocked_service.return_value = None

            player = self.APP.get(f'/api/players/{sys.maxsize}')
            mocked_service.assert_called_with(sys.maxsize)

            self.assertEqual(player.status_code, 404, "Response code of getting not existing player should be equal 404")

    def test_post_player(self):
        with patch('api_players.src.player.service.player_service.PlayerService.create') as mocked_service, \
                patch('api_players.src.player.event.player_event.PlayerEvent.create') as mocked_event:
            mocked_service.return_value = 1

            response = self.APP.post('/api/players', data=dict(
                username="Test Player Username",
                image_file="image_file.png"
            ))
            mocked_service.assert_called()
            mocked_event.assert_called()

            self.assertEqual(response.status_code, 201, "Created response status code should be equal 201")
            self.assertTrue("location" in response.json.keys(), "Responded json should contain 'location' key")

    def test_put_existing_player(self):
        with patch('api_players.src.player.service.player_service.PlayerService.find') as mocked_find_service, \
                patch('api_players.src.player.service.player_service.PlayerService.update') as mocked_update_service:
            mocked_find_service.return_value = Player(username="Test Player Username")
            mocked_update_service.return_value = PlayerService.SUCCESS_RETURN_VALUE

            response = self.APP.put("/api/players/1", data=dict(
                username="Updated Username",
                image_file="test_image.png"
            ))
            mocked_find_service.assert_called_with(1)
            mocked_update_service.assert_called()

            self.assertEqual(response.status_code, 202, "Response code of updating existing player should be equal 202")

    def test_put_not_existing_player(self):
        with patch('api_players.src.player.service.player_service.PlayerService.find') as mocked_service:
            mocked_service.return_value = None

            response = self.APP.put(f"/api/players/{sys.maxsize}", data=dict(
                username="Updated Username"
            ))
            mocked_service.assert_called_with(sys.maxsize)
            self.assertEqual(response.status_code, 404, "Response code of updateing not existing player should be equal 404")

    def test_delete_existing_player(self):
        with patch('api_players.src.player.service.player_service.PlayerService.find') as mocked_find_service, \
                patch('api_players.src.player.service.player_service.PlayerService.delete') as mocked_delete_service, \
                patch('api_players.src.player.event.player_event.PlayerEvent.delete') as mocked_event:
            mocked_find_service.return_value = Player(username="Player Username")
            mocked_delete_service.return_value = PlayerService.SUCCESS_RETURN_VALUE

            response = self.APP.delete("/api/players/1")
            mocked_find_service.assert_called_with(1)
            mocked_delete_service.assert_called_with(1)
            mocked_event.assert_called()

            self.assertEqual(response.status_code, 202, "Response code of deleting existing player should be equal 202")

    def test_delete_not_existing_player(self):
        with patch('api_players.src.player.service.player_service.PlayerService.find') as mocked_service:
            mocked_service.return_value = None

            response = self.APP.delete(f"/api/players/{sys.maxsize}")
            mocked_service.assert_called_with(sys.maxsize)
            self.assertEqual(response.status_code, 404, "Response code of deleting not existing player should be equal 404")


if __name__ == "__main__":
    unittest.main()
