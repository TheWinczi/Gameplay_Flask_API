from api_games.src.playing.models.models import Playing
from api_games.src.decorators.logging import log_info
from api_games.src import db

from sqlalchemy import exc


class PlayingRepository(object):
    """ Class responsible for adding, saving, deleting and
    updating playings models directly in database. """

    SUCCESS_RETURN_VALUE = 1
    FAIL_RETURN_VALUE = 0

    @staticmethod
    @log_info()
    def find_all():
        """ Find all existing Playing objects in database.

        Returns
        -------
        playings : list[Playing]
            List of founded Playing objects.
        """
        return list(Playing.query.all())

    @staticmethod
    @log_info()
    def find(player_id: int,
             game_id: int):
        """ Find playing model with a provided combination of provided player and game ids.

        Parameters
        ----------
        player_id : int
            Id of the player.

        game_id : int
            Id of the game.

        Returns
        -------
        playing : Playing
            Founded playing object. None otherwise.

        Raises
        ------
        TypeError
            If type of provided player or game ids are different than allowed.
        """
        if not isinstance(player_id, int):
            raise TypeError(f"Illegal type of argument. Player id could be only int not {type(player_id)}")

        if not isinstance(game_id, int):
            raise TypeError(f"Illegal type of argument. Game id could be only int not {type(game_id)}")

        playing = Playing.query.filter_by(player_id=player_id, game_id=game_id).first()
        if playing:
            return playing
        else:
            return None

    @staticmethod
    @log_info()
    def find_by_id(id: int):
        """ Find playing model with a provided id.

        Parameters
        ----------
        id : int
            Id of the playing to find.

        Returns
        -------
        playing : Playing
            Founded playing object. None otherwise.

        Raises
        ------
        TypeError
            If type of provided id is different than allowed.
        """
        if not isinstance(id, int):
            raise TypeError(f"Illegal type of argument. Id could be only int not {type(id)}")

        playing = Playing.query.filter_by(id=id).first()
        if playing:
            return playing
        else:
            return None

    @staticmethod
    @log_info()
    def create(playing: Playing,
               fail_return_value=FAIL_RETURN_VALUE):
        """ Create new instance of Playing object in database.

        Parameters
        ----------
        playing : Playing
            Playing object to add.

        fail_return_value : Any
            Optional. Value returned when creating failed.

        Returns
        -------
        id : int
            Id of created playing. However when creating failed `fail_return_value` is returned.

        Raises
        ------
        TypeError
            If type of provided playing is different than allowed. Default = `FAIL_RETURN_VALUE`
        """
        if not isinstance(playing, Playing):
            raise TypeError(f"Illegal type of argument. Playing could be only Playing not {type(playing)}")

        try:
            db.session.add(playing)
            db.session.commit()
            return playing.id
        except exc.SQLAlchemyError:
            return fail_return_value

    @staticmethod
    @log_info()
    def delete(id: int,
               success_return_value=SUCCESS_RETURN_VALUE,
               fail_return_value=FAIL_RETURN_VALUE):
        """ Delete Playing object contains provided id from database.

        Parameters
        ----------
        id : int
            Id of the playing object to delete.

        success_return_value : Any
            Optional. Value returned when deleting succeed.

        fail_return_value : Any
            Optional. Value returned when deleting failed.

        Returns
        -------
        result : any
            When deleting succeed `success_return_value` is returned.
            When deleting failed `fail_return_value` is returned.

        Raises
        ------
        TypeError
            If type of provided id is different than allowed.
        """
        if not isinstance(id, int):
            raise TypeError(f"Illegal type of argument. Id could be only int not {type(id)}")

        playing = Playing.query.filter_by(id=id).first()
        if playing:
            try:
                db.session.query(Playing).filter_by(id=id).delete(synchronize_session='fetch')
                db.session.commit()
                return success_return_value
            except exc.SQLAlchemyError:
                return fail_return_value
        else:
            return fail_return_value

    @staticmethod
    @log_info()
    def update(playing: Playing,
               success_return_value=SUCCESS_RETURN_VALUE,
               fail_return_value=FAIL_RETURN_VALUE):
        """ Update existing playing with provided playing object

        Parameters
        ----------
        playing : Playing
            Playing object to add.

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
            If type of provided playing is different than allowed.
        """
        if not isinstance(playing, Playing):
            raise TypeError(f"Illegal type of argument. Playing could be only Playing not {type(playing)}")

        existing_playing = Playing.query.filter_by(id=playing.id).first()
        if existing_playing:
            try:
                db.session.add(playing)
                db.session.commit()
                return success_return_value
            except exc.SQLAlchemyError:
                return fail_return_value
        else:
            return fail_return_value
