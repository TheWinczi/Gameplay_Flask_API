from api_games.src.game.repository.game_repository import GameRepository
from api_games.src.game.models.models import Game


class GameService(object):

    def __init__(self):
        pass

    @staticmethod
    def find(id):
        """ Find game model with a provided id.

        Parameters
        ----------
        id : int
            Id of the game to find.

        Returns
        -------
        game : Game
            Founded game object. None otherwise.

        Raises
        ------
        TypeError
            If type of provided id is different than allowed.
        """
        if not isinstance(id, int):
            raise TypeError(f"Illegal type of argument. Id could be only int not {type(id)}")

        return GameRepository.find_by_id(id)

    @staticmethod
    def find_all():
        """ Find all existing Game objects in database.

        Returns
        -------
        games : list[Game]
            List of founded Game objects.
        """
        return GameRepository.find_all()

    @staticmethod
    def create(game):
        """ Create new instance of Game object in database.

        Parameters
        ----------
        game : Game
            Game object to add.

        Raises
        ------
        TypeError
            If type of provided game is different than allowed.
        """
        if not isinstance(game, Game):
            raise TypeError(f"Illegal type of argument. Game could be only Game not {type(game)}")

        return GameRepository.create(game)

    @staticmethod
    def update(game):
        """ Update existing game with provided game object

        Parameters
        ----------
        game : Game
            Game object to add.

        Returns
        -------
        id : int
            Id of created game.

        Raises
        ------
        TypeError
            If type of provided game is different than allowed.
        """
        if not isinstance(game, Game):
            raise TypeError(f"Illegal type of argument. Game could be only Game not {type(game)}")

        return GameRepository.update(game)

    @staticmethod
    def delete(id):
        """ Delete Game object containing provided id from database.

        Parameters
        ----------
        id : int
            Id of the game to delete.

        Raises
        ------
        TypeError
            If type of provided id is different than allowed.
        """
        if not isinstance(id, int):
            raise TypeError(f"Illegal type of argument. Id could be only int not {type(id)}")

        GameRepository.delete(id)
