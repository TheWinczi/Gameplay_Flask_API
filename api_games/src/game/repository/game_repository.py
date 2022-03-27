from api_games.src.game.models.models import Game
from api_games.src.decorators.logging import log_info
from api_games.src import db

from sqlalchemy import exc


class GameRepository(object):
    """ Class responsible for adding, saving, deleting and
        updating players models directly in database. """

    SUCCESS_RETURN_VALUE = 1
    FAIL_RETURN_VALUE = 0

    @staticmethod
    @log_info()
    def find_all():
        """ Find all existing Game objects in database.

        Returns
        -------
        games : list[Game]
            List of founded Game objects.
        """
        return list(Game.query.all())

    @staticmethod
    @log_info()
    def find(id: int):
        """ Find Game model with a provided id.

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

        game = Game.query.filter_by(id=id).first()
        if game:
            return game
        else:
            return None

    @staticmethod
    @log_info()
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
            Id of created game. However when creating failed `fail_return_value` is returned.

        Raises
        ------
        TypeError
            If type of provided game is different than allowed.
        """
        if not isinstance(game, Game):
            raise TypeError(f"Illegal type of argument. Player could be only Player not {type(game)}")

        try:
            db.session.add(game)
            db.session.commit()
            return game.id
        except exc.SQLAlchemyError:
            return fail_return_value

    @staticmethod
    @log_info()
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

        player = Game.query.filter_by(id=id).first()
        if player:
            try:
                db.session.query(Game).filter_by(id=id).delete()
                db.session.commit()
                return success_return_value
            except exc.SQLAlchemyError:
                return fail_return_value
        else:
            return fail_return_value

    @staticmethod
    @log_info()
    def update(game: Game,
               success_return_value=SUCCESS_RETURN_VALUE,
               fail_return_value=FAIL_RETURN_VALUE):
        """ Update existing game with provided game object

        Parameters
        ----------
        game : Game
            Game object to add.

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
        if not isinstance(game, Game):
            raise TypeError(f"Illegal type of argument. Player could be only Player not {type(game)}")

        existing_game = Game.query.filter_by(id=game.id).first()
        if existing_game:
            try:
                db.session.add(game)
                db.session.commit()
                return success_return_value
            except exc.SQLAlchemyError:
                return fail_return_value
        else:
            return fail_return_value
