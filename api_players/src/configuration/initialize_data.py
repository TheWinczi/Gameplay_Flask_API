from src.player.models.models import Player
from src.player.repository.player_repository import PlayerRepository


def _initialize_players():
    """ Initialize players models.

    Notes
    -----
    Function creates 3 random Players in different
    configuration and adds these to database.
    """
    players = [
        Player("Player 1", "the_best.png"),
        Player("Player 2"),
        Player("Player 3", "def.png")
    ]

    for player in players:
        PlayerRepository.create(player)



def initialize_models():
    """ Initialize all needed models.

    Notes
    -----
    Function executes functions responsible for initialization
    different type of models inside the module.
    It is recommended to use that function to not worrying about function execution order.

    Function initializes:
        1. players
    """
    _initialize_players()
