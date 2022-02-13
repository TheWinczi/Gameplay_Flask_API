import unittest
import sys

from api_games.src import create_app

# Start test application to initialize needed variables
APP = create_app({"TESTING": True, "INITIALIZE_MODELS": False})

from api_games.src import db
from api_games.src.game.models.models import Game
from api_games.src.game.repository.game_repository import GameRepository


class GameRepositoryTests(unittest.TestCase):

    GAME = None

    def setUp(self):
        """
        Function executes before each test.
        """
        self.GAME = Game(description="Test Game Description")

        db.session.add(self.GAME)
        db.session.commit()

    def tearDown(self):
        """
        Function executes after each test.
        """
        meta = db.metadata
        for table in reversed(meta.sorted_tables):
            db.session.execute(table.delete())
        db.session.commit()

    # ---------- ---------- TESTS ---------- ----------

    def test_find_all(self):
        games = GameRepository.find_all()
        self.assertTrue(isinstance(games, list), f"Returned games object should be instance of list not {type(games)}")
        for game in games:
            self.assertTrue(isinstance(game, Game), f"Returned games should be instances of Game not {type(game)}")

    def test_find_by_id_existing_model(self):
        game = GameRepository.find_by_id(self.GAME.id)
        self.assertEqual(game.description, self.GAME.description, "Returned Game description should be equal to added Game description")

    def test_find_by_id_not_existing_model(self):
        game = GameRepository.find_by_id(sys.maxsize)
        self.assertTrue(game is None, "Returned not existing Game should be equal to None")

    def test_find_by_id_not_being_int(self):
        with self.assertRaises(TypeError):
            GameRepository.find_by_id("id")

    def test_create(self):
        game = Game(description="New Game")
        game_id = GameRepository.create(game)
        db_game = GameRepository.find_by_id(game_id)

        self.assertTrue(db_game is not None, "Created game should not be None")
        self.assertEqual(game.description, db_game.description, "Created Game fields should be equal to added Game fields")

    def test_create_game_not_being_game(self):
        game = "game"
        with self.assertRaises(TypeError):
            GameRepository.create(game)

    def test_delete_existing_game(self):
        game_id = self.GAME.id
        GameRepository.delete(game_id)
        game = GameRepository.find_by_id(game_id)
        self.assertTrue(game is None, "After deleting, it should not be possible to getting deleted game")

    def test_delete_with_id_not_being_int(self):
        with self.assertRaises(TypeError):
            GameRepository.delete("id")

    def test_update_existing_game(self):
        game_id = self.GAME.id

        self.GAME.description = "Updated Description"

        GameRepository.update(self.GAME)

        game = GameRepository.find_by_id(game_id)
        self.assertEqual(game.description, "Updated Description", "Updated Game should has updated fields")


if __name__ == "__main__":
    unittest.main()
