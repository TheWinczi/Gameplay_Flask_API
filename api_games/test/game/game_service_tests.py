import unittest
from unittest.mock import patch
import sys

from api_games.src import create_app

# Start test application to initialize needed variables
APP = create_app({"TESTING": True, "INITIALIZE_MODELS": False})

from api_games.src.game.models.models import Game
from api_games.src.game.service.game_service import GameService


class GameServiceTests(unittest.TestCase):

    def test_find_existing_game(self):
        with patch('api_games.src.game.repository.game_repository.GameRepository.find_by_id') as mocked_repo:
            mocked_repo.return_value = Game(description="Test Game Description")

            game = GameService.find(1)
            mocked_repo.assert_called_with(1)

            self.assertTrue(isinstance(game, Game), f"Returned game should be instance of Game not {type(game)}")

    def test_find_not_existing_game(self):
        with patch('api_games.src.game.repository.game_repository.GameRepository.find_by_id') as mocked_repo:
            mocked_repo.return_value = None

            game = GameService.find(sys.maxsize)
            mocked_repo.assert_called_with(sys.maxsize)
            self.assertTrue(game is None, "Returned not existing game should be equal to None")

    def test_find_with_id_not_being_int(self):
        with self.assertRaises(TypeError):
            GameService.find("id")

    def test_find_all(self):
        with patch('api_games.src.game.repository.game_repository.GameRepository.find_all') as mocked_repo:
            mocked_repo.return_value = [
                Game(description="Game 1"),
                Game(description="Game 2")
            ]

            games = GameService.find_all()
            mocked_repo.assert_called_once()

            self.assertTrue(isinstance(games, list), f"Returned games object should be instance of list not {type(games)}")
            for game in games:
                self.assertTrue(isinstance(game, Game), f"Returned games should be instances of Game not {type(game)}")

    def test_create(self):
        with patch('api_games.src.game.repository.game_repository.GameRepository.create') as mocked_repo:
            mocked_repo.return_value = 1

            game = Game(description="Test Game Description")
            game_id = GameService.create(game)
            mocked_repo.assert_called_with(game)

            self.assertTrue(isinstance(game_id, int), f"Returned id should be instance of int, not {type(game_id)}")
            self.assertTrue(game_id > 0, "Returned id should be grater than 0")

    def test_update_with_game_not_being_game(self):
        with self.assertRaises(TypeError):
            GameService.update("")

    def test_delete_with_id_not_being_int(self):
        with self.assertRaises(TypeError):
            GameService.delete("id")


if __name__ == "__main__":
    unittest.main()
