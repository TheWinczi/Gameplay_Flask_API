from api_games.src.game.repository.game_repository import GameRepository
from api_games.src.game.models.models import Game


class GameService(object):
    """ Class responsible for adding, saving, deleting and
        updating games using Game repository.
        Between repository and controller. """

    SUCCESS_RETURN_VALUE = 1
    FAIL_RETURN_VALUE = 0

    @staticmethod
    def find(id: int):
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
    def create(game: Game,
               fail_return_value=FAIL_RETURN_VALUE):
        """ Create new instance of Game object in database.

        Parameters
        ----------
        game : Game
            Game object to add.

        fail_return_value : Any
            Optional. Value returned when creating failed.

        Returns
        -------
        id : int
            Id of created player. However when creating failed `fail_return_value` is returned.

        Raises
        ------
        TypeError
            If type of provided game is different than allowed.
        """
        if not isinstance(game, Game):
            raise TypeError(f"Illegal type of argument. Game could be only Game not {type(game)}")

        result = GameRepository.create(game)
        if result != GameRepository.FAIL_RETURN_VALUE:
            return result
        else:
            return fail_return_value

    @staticmethod
    def delete(id: int,
               success_return_value=SUCCESS_RETURN_VALUE,
               fail_return_value=FAIL_RETURN_VALUE):
        """ Delete Game object containing provided id from database.

        Parameters
        ----------
        id : int
            Id of the game to delete.

        success_return_value : Any
            Optional. Value returned when deleting succeed.

        fail_return_value : Any
            Optional. Value returned when deleting failed.

        Returns
        -------
        result : Any
            When deleting succeed `success_return_value` is returned.
            When deleting failed `fail_return_value` is returned.

        Raises
        ------
        TypeError
            If type of provided id is different than allowed.
        """
        if not isinstance(id, int):
            raise TypeError(f"Illegal type of argument. Id could be only int not {type(id)}")

        result = GameRepository.delete(id)
        if result == GameRepository.SUCCESS_RETURN_VALUE:
            return success_return_value
        elif result == GameRepository.FAIL_RETURN_VALUE:
            return fail_return_value

    @staticmethod
    def update(game: Game,
               success_return_value=SUCCESS_RETURN_VALUE,
               fail_return_value=FAIL_RETURN_VALUE):
        """ Update existing game with provided game object

        Parameters
        ----------
        game : Game
            Game object to add.

        success_return_value : Any
            Optional. Value returned when deleting succeed.

        fail_return_value : Any
            Optional. Value returned when deleting failed.

        Returns
        -------
        result : Any
            When updating succeed `success_return_value` is returned.
            When updating failed `fail_return_value` is returned.

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

        result = GameRepository.update(game)
        if result == GameRepository.SUCCESS_RETURN_VALUE:
            return success_return_value
        elif result == GameRepository.FAIL_RETURN_VALUE:
            return fail_return_value
