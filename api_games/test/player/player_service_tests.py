import unittest
from unittest.mock import patch
import sys

from api_games.src import create_app

# Start test application to initialize needed variables
APP = create_app({"TESTING": True, "INITIALIZE_MODELS": False})

from api_games.src.player.models.models import Player
from api_games.src.player.service.player_service import PlayerService
from api_games.src.player.repository.player_repository import PlayerRepository


class PlayerServiceTests(unittest.TestCase):

    def test_find_existing_player(self):
        with patch('api_games.src.player.repository.player_repository.PlayerRepository.find_by_id') as mocked_repo:
            mocked_repo.return_value = Player(username="Test Player Username")

            player = PlayerService.find(1)
            mocked_repo.assert_called_with(1)

            self.assertTrue(isinstance(player, Player), f"Returned player should be instance of Player not {type(player)}")

    def test_find_not_existing_player(self):
        with patch('api_games.src.player.repository.player_repository.PlayerRepository.find_by_id') as mocked_repo:
            mocked_repo.return_value = None

            player = PlayerService.find(sys.maxsize)
            mocked_repo.assert_called_with(sys.maxsize)
            self.assertTrue(player is None, "Returned value of not existing player should be equal to None")

    def test_find_with_id_not_being_int(self):
        with self.assertRaises(TypeError):
            PlayerService.find("id")

    def test_find_all(self):
        with patch('api_games.src.player.repository.player_repository.PlayerRepository.find_all') as mocked_repo:
            mocked_repo.return_value = [
                Player(username="player 1"),
                Player(username="player 2")
            ]

            players = PlayerService.find_all()
            mocked_repo.assert_called_once()

            self.assertTrue(isinstance(players, list), f"Returned players object should be instance of list not {type(players)}")
            for player in players:
                self.assertTrue(isinstance(player, Player), f"Returned players should be instances of Player not {type(player)}")

    def test_get_all_players_being_not_in_game(self):
        with patch('api_games.src.player.repository.player_repository.PlayerRepository.find_all') as mocked_repo:
            mocked_repo.return_value = [
                Player(id=1, username="Player 1", game_id=1),
                Player(id=2, username="Player 2", game_id=None),
                Player(id=3, username="Player 3", game_id=1),
            ]
            players = PlayerService.find_all_not_in_game()
            mocked_repo.assert_called_once()

            self.assertTrue(isinstance(players, list),
                            f"Returned players object should be instance of list not {type(players)}")
            self.assertTrue(len(players) == 1, "Should return list with only 1 player")
            for player in players:
                self.assertTrue(isinstance(player, Player),
                                f"Returned players should be instances of Player not {type(player)}")

    def test_get_all_players_being_in_game(self):
        with patch('api_games.src.player.repository.player_repository.PlayerRepository.find_all') as mocked_repo:
            mocked_repo.return_value = [
                Player(id=1, username="Player 1", game_id=None),
                Player(id=2, username="Player 2", game_id=None),
                Player(id=3, username="Player 3", game_id=1),
            ]
            players = PlayerService.find_all_in_game()
            mocked_repo.assert_called_once()

            self.assertTrue(isinstance(players, list),
                            f"Returned players object should be instance of list not {type(players)}")
            self.assertTrue(len(players) == 1, "Should return list with only 1 player")
            for player in players:
                self.assertTrue(isinstance(player, Player),
                                f"Returned players should be instances of Player not {type(player)}")

    def test_create(self):
        with patch('api_games.src.player.repository.player_repository.PlayerRepository.create') as mocked_repo:
            mocked_repo.return_value = 1

            player = Player(username="Test Player Username")
            player_id = PlayerService.create(player)
            mocked_repo.assert_called_with(player)

            self.assertTrue(isinstance(player_id, int), f"Returned id should be instance of int, not {type(player_id)}")
            self.assertTrue(player_id > 0, "Returned id should be grater than 0")

    def test_update_existing_player(self):
        with patch('api_games.src.player.repository.player_repository.PlayerRepository.update') as mocked_repo:
            mocked_repo.return_value = PlayerRepository.SUCCESS_RETURN_VALUE

            result = PlayerService.update(Player(username="Test Player"))
            mocked_repo.assert_called()

            self.assertEqual(result, PlayerService.SUCCESS_RETURN_VALUE, "When repository return SUCCESS then service should return SUCCESS")

    def test_update_with_player_not_being_player(self):
        with self.assertRaises(TypeError):
            PlayerService.update("player")

    def test_delete_existing_player(self):
        with patch('api_games.src.player.repository.player_repository.PlayerRepository.delete') as mocked_repo:
            mocked_repo.return_value = PlayerRepository.SUCCESS_RETURN_VALUE

            result = PlayerService.delete(1)
            mocked_repo.assert_called_with(1)

            self.assertEqual(result, PlayerService.SUCCESS_RETURN_VALUE, "When repository return SUCCESS then service should return SUCCESS")

    def test_delete_with_id_not_being_int(self):
        with self.assertRaises(TypeError):
            PlayerService.delete("id")


if __name__ == "__main__":
    unittest.main()
