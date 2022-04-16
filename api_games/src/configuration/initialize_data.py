import random

from api_games.src.game.models.models import Game
from api_games.src.game.service.game_service import GameService

from api_games.src.player.models.models import Player
from api_games.src.player.service.player_service import PlayerService

from api_games.src.playing.models.models import Playing
from api_games.src.playing.service.playing_service import PlayingService


def _initialize_players():
    """ Initialize players models.

    Returns
    -------
    players : list[Player]
        List of players added to database.

    Notes
    -----
    Function creates 3 random Players in different
    configuration and adds these to database.
    """
    players = [
        Player(username="Player 1"),
        Player(username="Player 2"),
        Player(username="Player 3")
    ]

    for player in players:
        PlayerService.create(player)

    return players


def _initialize_games():
    """ Initialize games models.

    Returns
    -------
    games : list[Game]
        List of games added to database.

    Notes
    -----
    Function creates 2 random Games in different
    configuration and adds these to database.
    """
    games = [
        Game(description="This is game number 1"),
        Game(description="This is game number 2")
    ]

    for game in games:
        GameService.create(game)

    return games


def _initialize_playings(games: list[Game], players: list[Player]):
    """ Initialize playings models.

    Returns
    -------
    playings : list[Playing]
        List of playings added to database.

    Notes
    -----
    Function adds provided players to games choose randomly.
    """
    if len(games) <= 0 or len(players) <= 0:
        return

    playings = []

    for player in players:
        game = random.choice(games)
        PlayingService.connect_player_and_game(player, game, score=100)

    return playings


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
    games = _initialize_games()
    players = _initialize_players()
    playings = _initialize_playings(games, players)
