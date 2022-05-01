from collections import OrderedDict

from api_games.src.player.event.commands import Command, CreatePlayerCommand, DeletePlayerCommand, UpdatePlayerCommand


class PlayerEventsParser(object):
    """ Player events parser class responsible for
    parsing and executing proper commands
    pointed in parsed event.
    """

    def __init__(self):
        self._events_commands = OrderedDict({
            'POST': CreatePlayerCommand(),
            'PUT': UpdatePlayerCommand(),
            'DELETE': DeletePlayerCommand()
        })

    def parse(self, event: dict):
        """ Parse provided event and execute
        proper command pointed in event. """

        event_body = event.get('body', {})
        event_command = event.get('method', '').upper()

        command = self._events_commands.get(event_command, lambda h: h)
        if isinstance(command, Command):
            command.execute(event_body)
