from api_games.src.game.models.models import Game

from api_games.src import db


class GameRepository(object):
    """ Class responsible for adding, saving, deleting and
        updating players models directly in database. """

    @staticmethod
    def find_all():
        """ Find all existing Game objects in database.

        Returns
        -------
        games : list[Game]
            List of founded Game objects.
        """
        return list(Game.query.all())

    @staticmethod
    def find_by_id(id):
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
    def create(game):
        """ Create new instance of Game object in database.

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
            raise TypeError(f"Illegal type of argument. Player could be only Player not {type(game)}")

        db.session.add(game)
        db.session.commit()

        return game.id

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

        player = Game.query.filter_by(id=id).first()
        if player:
            db.session.query(Game).filter_by(id=id).delete()
            db.session.commit()

    @staticmethod
    def update(game):
        """ Update existing game with provided game object

        Parameters
        ----------
        game : Game
            Game object to add.

        Raises
        ------
        TypeError
            If type of provided player is different than allowed.
        """
        if not isinstance(game, Game):
            raise TypeError(f"Illegal type of argument. Player could be only Player not {type(game)}")

        existing_game = Game.query.filter_by(id=game.id).first()
        if existing_game:
            db.session.add(game)
            db.session.commit()

