from api_players.config import GAME_SERVER_URL
from api_players.src.player.models.models import Player

import requests


class PlayerEvent(object):
    """ Class responsible for adding and deleting
    players in other Microservices """

    @staticmethod
    def create(player: Player):
        url = GAME_SERVER_URL + "api/players"
        data = {
            "username": player.username
        }
        requests.post(url, data)

    @staticmethod
    def delete(id: int):
        url = GAME_SERVER_URL + f"api/players/{id}"
        requests.delete(url)
