from src import db
from src.player.models.models import Player


class PlayerRepository(object):
    """ Class responsible for adding, saving, deleting and
    updating players models inside directly in database. """

    def __init__(self):
        pass

    @staticmethod
    def find_all():
        """ Find all existing Player objects in database.

        Returns
        -------
        players : list[Player]
            List of founded Player objects.
        """
        return list(Player.query.all())

    @staticmethod
    def find_by_id(id):
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

        player = Player.query.filter_by(id=id).first()
        if player:
            return player
        else:
            return None

    @staticmethod
    def delete(id):
        """ Delete Player object  containing provided id from database.

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

        player = Player.query.filter_by(id=id).first()
        if player:
            db.session.query(Player).filter_by(id=id).delete()
            db.session.commit()

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

        db.session.add(player)
        db.session.commit()

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

        existing_player = Player.query.filter_by(id=player.id).first()
        if existing_player:
            db.session.add(player)
            db.session.commit()
        else:
            PlayerRepository.create(player)
