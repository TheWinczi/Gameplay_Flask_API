from api_games.src.player.models.models import Player
from api_games.src.player.service.player_service import PlayerService

from api_games.src.game.models.models import Game
from api_games.src.game.service.game_service import GameService


def _initialize_players():
    """ Initialize players models.

    Returns
    -------
    players_ids : list[int]
        Created players ids list.

    Notes
    -----
    Function creates 3 random Players in different
    configuration and adds these to database.
    """
    players = [
        Player(username="Player 1", game_id=1),
        Player(username="Player 2", game_id=1),
        Player(username="Player 3", game_id=2)
    ]

    players_ids = []

    for player in players:
        players_ids.append(PlayerService.create(player))

    return players_ids


def _initialize_games():
    """ Initialize games models.

    Returns
    -------
    games_ids : list[int]
        Created games ids list.

    Notes
    -----
    Function creates 2 random Games in different
    configuration and adds these to database.
    """
    games = [
        Game(description="This is game number 1"),
        Game(description="This is game number 2")
    ]

    games_ids = []

    for game in games:
        games_ids.append(GameService.create(game))

    return games_ids


def initialize_models():
    """ Initialize all needed models.

    Notes
    -----
    Function executes functions responsible for initialization
    different type of models inside the module.
    It is recommended to use that function to not worrying about function execution order.

    Function initializes:
        1. Games
        2. players
    """
    _initialize_games()
    _initialize_players()
