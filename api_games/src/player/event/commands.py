from abc import ABC, abstractmethod

from api_games.src.player.models.models import Player
from api_games.src.player.service.player_service import PlayerService


class Command(ABC):
    """ Abstract interface of Command object."""
    @abstractmethod
    def execute(self, data):
        pass


class CreatePlayerCommand(Command):
    """ Child of abstract Command interface.
    Responsible for creating new players.
    """

    def execute(self, data: dict):
        username = data.get('username', None)
        if username is not None:
            player = Player(username=username)
            PlayerService.create(player)


class DeletePlayerCommand(Command):
    """ Child of abstract Command interface.
    Responsible for deleting existing players.
    """

    def execute(self, data: dict):
        player_id = data.get('id', None)
        if player_id is not None:
            PlayerService.delete(player_id)


class UpdatePlayerCommand(Command):
    """ Child of abstract Command interface.
    Responsible for updating existing players.
    """

    def execute(self, data: dict):
        username = data.get('username', None)
        player_id = data.get('id', None)

        if (username and player_id) is not None:
            player = PlayerService.find(player_id)
            if player is None:
                return

            player.username = username
            PlayerService.update(player)
