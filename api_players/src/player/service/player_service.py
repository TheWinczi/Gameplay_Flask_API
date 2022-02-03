# Import Player repository object
from ..repository.player_repository import PlayerRepository

# Import Player model
from ..models.models import Player


class PlayerService(object):

    def __init__(self):
        pass
    
    @staticmethod
    def find(id):
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
    def create(player):
        """ Create new instance of Player object in database.

        Parameters
        ----------
        player : Player
            Player object to add.

        Raises
        ------
        TypeError
            If type of provided player is different than allowed.
        """
        if not isinstance(player, Player):
            raise TypeError(f"Illegal type of argument. Player could be only Player not {type(player)}")
        return PlayerRepository.create(player)

    @staticmethod
    def update(player):
        """ Update existing player with provided player object

        Parameters
        ----------
        player : Player
            Player object to add.

        Raises
        ------
        TypeError
            If type of provided player is different than allowed.

        Notes
        -----
        If player with the same id as the provided player does
        not exist in database new player is created.
        """
        if not isinstance(player, Player):
            raise TypeError(f"Illegal type of argument. Player could be only Player not {type(player)}")

        return PlayerRepository.update(player)

    @staticmethod
    def delete(id):
        """ Delete Player object containing provided id from database.

        Parameters
        ----------
        id : int
            Id of the player to delete.

        Raises
        ------
        TypeError
            If type of provided id is different than allowed.
        """
        if not isinstance(id, int):
            raise TypeError(f"Illegal type of argument. Id could be only int not {type(id)}")

        PlayerRepository.delete(id)
