from api_games.src.player.models.models import Player
from api_games.src.decorators.logging import log_info
from api_games.src import db

from sqlalchemy import exc


class PlayerRepository(object):
    """ Class responsible for adding, saving, deleting and
    updating players models directly in database. """

    SUCCESS_RETURN_VALUE = 1
    FAIL_RETURN_VALUE = 0

    @staticmethod
    @log_info()
    def find_all():
        """ Find all existing Player objects in database.

        Returns
        -------
        players : list[Player]
            List of founded Player objects.
        """
        return list(Player.query.all())

    @staticmethod
    @log_info()
    def find_by_id(id: int):
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
            If type of provided player is different than allowed. Default = `FAIL_RETURN_VALUE`
        """
        if not isinstance(player, Player):
            raise TypeError(f"Illegal type of argument. Player could be only Player not {type(player)}")

        try:
            db.session.add(player)
            db.session.commit()
            return player.id
        except exc.SQLAlchemyError:
            return fail_return_value

    @staticmethod
    @log_info()
    def delete(id: int,
               success_return_value=SUCCESS_RETURN_VALUE,
               fail_return_value=FAIL_RETURN_VALUE):
        """ Delete Player object  containing provided id from database.

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

        player = Player.query.filter_by(id=id).first()
        if player:
            try:
                db.session.query(Player).filter_by(id=id).delete(synchronize_session='fetch')
                db.session.commit()
                return success_return_value
            except exc.SQLAlchemyError:
                return fail_return_value
        else:
            return fail_return_value

    @staticmethod
    @log_info()
    def update(player: Player,
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

        existing_player = Player.query.filter_by(id=player.id).first()
        if existing_player:
            try:
                db.session.add(player)
                db.session.commit()
                return success_return_value
            except exc.SQLAlchemyError:
                return fail_return_value
        else:
            return fail_return_value
