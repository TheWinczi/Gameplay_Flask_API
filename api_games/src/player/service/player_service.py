from api_games.src.player.repository.player_repository import PlayerRepository
from api_games.src.player.models.models import Player
from api_games.src.decorators.logging import log_info


class PlayerService(object):
    """ Class responsible for adding, saving, deleting and
        updating players using Player repository.
        Between repository and controller. """

    SUCCESS_RETURN_VALUE = 1
    FAIL_RETURN_VALUE = 0

    @staticmethod
    @log_info()
    def find(id: int):
        """ Find player model with a provided id.

        Parameters
        ----------
        id : int
            Id of the player to find.

        Returns
        -------
        player : Player
            Founded player object. None otherwise.

        Raises
        ------
        TypeError
            If type of provided id is different than allowed.
        """
        if not isinstance(id, int):
            raise TypeError(f"Illegal type of argument. Id could be only int not {type(id)}")

        return PlayerRepository.find(id)

    @staticmethod
    @log_info()
    def find_all():
        """ Find all existing Player objects in database.

        Returns
        -------
        players : list[Player]
            List of founded Player objects.
        """
        return PlayerRepository.find_all()

    @staticmethod
    @log_info()
    def find_all_in_game():
        """ Find all existing Players being in a Game in database.

        Returns
        -------
        players : list[Player]
            List of founded Player objects being in a Game.
        """
        players = PlayerRepository.find_all()
        players = list(
            filter(lambda player: player.game_id is not None, players)
        )
        return players

    @staticmethod
    @log_info()
    def find_all_not_in_game():
        """ Find all existing Players not being in any Game in database.

        Returns
        -------
        players : list[Player]
            List of founded Player objects not being in any Game.
        """
        players = PlayerRepository.find_all()
        players = list(
            filter(lambda player: player.game_id is None, players)
        )
        return players

    @staticmethod
    @log_info()
    def create(player: Player,
               fail_return_value=FAIL_RETURN_VALUE):
        """ Create new instance of Player object in database.

        Parameters
        ----------
        player : Player
            Player object to add.

        fail_return_value : Any
            Optional. Value returned when creating failed.

        Returns
        -------
        id : int
            Id of created player. However when creating failed `fail_return_value` is returned.

        Raises
        ------
        TypeError
            If type of provided player is different than allowed.
        """
        if not isinstance(player, Player):
            raise TypeError(f"Illegal type of argument. Player could be only Player not {type(player)}")

        result = PlayerRepository.create(player)
        if result != PlayerRepository.FAIL_RETURN_VALUE:
            return result
        else:
            return fail_return_value

    @staticmethod
    @log_info()
    def delete(id: int,
               success_return_value=SUCCESS_RETURN_VALUE,
               fail_return_value=FAIL_RETURN_VALUE):
        """ Delete Player object containing provided id from database.

        Parameters
        ----------
        id : int
            Id of the player to delete.

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

        result = PlayerRepository.delete(id)
        if result == PlayerRepository.SUCCESS_RETURN_VALUE:
            return success_return_value
        elif result == PlayerRepository.FAIL_RETURN_VALUE:
            return fail_return_value

    @staticmethod
    @log_info()
    def update(player,
               success_return_value=SUCCESS_RETURN_VALUE,
               fail_return_value=FAIL_RETURN_VALUE):
        """ Update existing player with provided player object

        Parameters
        ----------
        player : Player
            Player object to add.

        success_return_value : Any
            Optional. Value returned when updating succeed.

        fail_return_value : Any
            Optional. Value returned when updating failed.

        Returns
        -------
        result : Any
            When updating succeed `success_return_value` is returned.
            When updating failed `fail_return_value` is returned.

        Raises
        ------
        TypeError
            If type of provided player is different than allowed.
        """
        if not isinstance(player, Player):
            raise TypeError(f"Illegal type of argument. Player could be only Player not {type(player)}")

        result = PlayerRepository.update(player)
        if result == PlayerRepository.SUCCESS_RETURN_VALUE:
            return success_return_value
        elif result == PlayerRepository.FAIL_RETURN_VALUE:
            return fail_return_value
