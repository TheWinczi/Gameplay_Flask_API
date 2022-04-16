from api_games.src.playing.repository.playing_repository import PlayingRepository
from api_games.src.playing.models.models import Playing
from api_games.src.game.models.models import Game
from api_games.src.player.models.models import Player
from api_games.src.decorators.logging import log_info


class PlayingService(object):
    """ Class responsible for adding, saving, deleting and
        updating playings using Playing repository.
        Between repository and controller. """

    SUCCESS_RETURN_VALUE = 1
    FAIL_RETURN_VALUE = 0

    @staticmethod
    @log_info()
    def find(player_id, game_id):
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
            raise TypeError(f"Illegal type of argument. Player id could be only int not {type(id)}")

        if not isinstance(game_id, int):
            raise TypeError(f"Illegal type of argument. Game id could be only int not {type(id)}")

        return PlayingRepository.find(player_id, game_id)

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

        return PlayingRepository.find(id=id)

    @staticmethod
    @log_info()
    def find_all():
        """ Find all existing Playing objects in database.

        Returns
        -------
        playings : list[Playing]
            List of founded Playing objects.
        """
        return PlayingRepository.find_all()

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
            If type of provided playing is different than allowed.
        """
        if not isinstance(playing, Playing):
            raise TypeError(f"Illegal type of argument. Playing could be only Playing not {type(playing)}")

        result = PlayingRepository.create(playing)
        if result != PlayingRepository.FAIL_RETURN_VALUE:
            return result
        else:
            return fail_return_value

    @staticmethod
    @log_info()
    def connect_player_and_game(player: Player,
                                game: Game,
                                score: int = 0,
                                success_return_value=SUCCESS_RETURN_VALUE,
                                fail_return_value=FAIL_RETURN_VALUE):
        """ Connect provided Player and Game - create new Playing object

        Parameters
        ----------
        player : Player
            Player to connect.

        game : Game
            Game to which player will connect.

        score : int, Default = 0
            Optional. Score of player in the game. Default = 0.

        success_return_value : Any
            Optional. Value returned when connecting succeed.

        fail_return_value : Any
            Optional. Value returned when connecting failed.

        Returns
        -------
        result : Any
            When connecting succeed `success_return_value` is returned.
            When connecting failed `fail_return_value` is returned.

        Raises
        ------
        TypeError
            If types of provided player or game are different than allowed.
        """
        if not isinstance(player, Player):
            raise TypeError(f"Illegal type of argument. Player could be only Player instance not {type(player)}")

        if not isinstance(game, Game):
            raise TypeError(f"Illegal type of argument. Game could be only Game instance not {type(game)}")

        if not isinstance(score, int):
            raise TypeError(f"Illegal type of argument. Score could be only int not {type(score)}")

        playing = Playing()
        playing.game = game
        playing.player = player
        playing.score = score

        result = PlayingRepository.create(playing)
        if result == PlayingRepository.FAIL_RETURN_VALUE:
            return fail_return_value
        else:
            return success_return_value

    @staticmethod
    @log_info()
    def delete(player_id: int,
               game_id: int,
               success_return_value=SUCCESS_RETURN_VALUE,
               fail_return_value=FAIL_RETURN_VALUE):
        """ Delete Player object containing provided id from database.

        Parameters
        ----------
        player_id : int
            Id of the player in playing object to delete.

        game_id : int
            Id of the game in playing object to delete.

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
        if not isinstance(player_id, int):
            raise TypeError(f"Illegal type of argument. Player id could be only int not {type(player_id)}")

        if not isinstance(game_id, int):
            raise TypeError(f"Illegal type of argument. Game id could be only int not {type(game_id)}")

        playing = Playing.query.filter_by(player_id=player_id, game_id=game_id).first()
        if not playing:
            return success_return_value

        result = PlayingRepository.delete(playing.id)
        if result != PlayingRepository.SUCCESS_RETURN_VALUE:
            return fail_return_value
        else:
            return success_return_value

    @staticmethod
    @log_info()
    def update(playing,
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

        result = PlayingRepository.update(playing)
        if result == PlayingRepository.SUCCESS_RETURN_VALUE:
            return success_return_value
        elif result == PlayingRepository.FAIL_RETURN_VALUE:
            return fail_return_value
