import unittest
import sys

from api_games.src import create_app

# Start test application to initialize needed variables
APP = create_app({"TESTING": True, "INITIALIZE_MODELS": False})

from api_games.src import db
from api_games.src.player.models.models import Player
from api_games.src.player.repository.player_repository import PlayerRepository


class PlayerRepositoryTests(unittest.TestCase):

    PLAYER = None

    def setUp(self):
        """
        Function executes before each test.
        """
        self.PLAYER = Player(username="Test Player")

        db.session.add(self.PLAYER)
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
        players = PlayerRepository.find_all()
        self.assertTrue(isinstance(players, list), f"Returned players object should be instance of list not {type(players)}")
        for player in players:
            self.assertTrue(isinstance(player, Player), f"Returned players should be instances of Player not {type(player)}")

    def test_find_by_id_existing_model(self):
        player = PlayerRepository.find_by_id(self.PLAYER.id)
        self.assertEqual(player.username, self.PLAYER.username, "Returned Player username should be equal to added Player username")

    def test_find_by_id_not_existing_model(self):
        player = PlayerRepository.find_by_id(sys.maxsize)
        self.assertTrue(player is None, "Returned not existing Player should be equal to None")

    def test_find_by_id_not_being_int(self):
        with self.assertRaises(TypeError):
            PlayerRepository.find_by_id("id")

    def test_create(self):
        player = Player(username="New Player")
        player_id = PlayerRepository.create(player)
        db_player = PlayerRepository.find_by_id(player_id)

        self.assertTrue(db_player is not None, "Created player should not be None")
        self.assertEqual(player.username, db_player.username, "Created Player fields should be equal to added Player fields")

    def test_create_player_not_being_player(self):
        with self.assertRaises(TypeError):
            PlayerRepository.create("player")

    def test_delete_existing_model(self):
        player_id = self.PLAYER.id
        PlayerRepository.delete(player_id)
        player = PlayerRepository.find_by_id(player_id)
        self.assertTrue(player is None, "After deleting, it should not be possible to getting deleted player")

    def test_delete_with_id_not_being_int(self):
        with self.assertRaises(TypeError):
            PlayerRepository.delete("id")

    def test_update_existing_player(self):
        player_id = self.PLAYER.id

        self.PLAYER.username = "Updated Username"

        PlayerRepository.update(self.PLAYER)

        player = PlayerRepository.find_by_id(player_id)
        self.assertEqual(player.username, "Updated Username", "Updated Player should has updated fields")

    def test_update_player_not_being_player(self):
        with self.assertRaises(TypeError):
            PlayerRepository.update("player")


if __name__ == "__main__":
    unittest.main()
