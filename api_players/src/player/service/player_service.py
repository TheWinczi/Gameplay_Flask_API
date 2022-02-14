from api_players.src.player.repository.player_repository import PlayerRepository
from api_players.src.player.models.models import Player


class PlayerService(object):
    """ Class responsible for adding, saving, deleting and
        updating players using Player repository.
        Between repository and controller. """

    SUCCESS_RETURN_VALUE = 1
    FAIL_RETURN_VALUE = 0
    
    @staticmethod
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

        return PlayerRepository.find_by_id(id)

    @staticmethod
    def find_all():
        """ Find all existing Player objects in database.

        Returns
        -------
        players : list[Player]
            List of founded Player objects.
        """
        return PlayerRepository.find_all()

    @staticmethod
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
