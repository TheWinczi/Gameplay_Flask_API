from api_players.config import GAME_SERVER_URL

import requests


class PlayerEvent(object):
    """ Class responsible for adding and deleting
    players in other Microservices"""

    @staticmethod
    def create(player):
        url = GAME_SERVER_URL + "api/players"
        data = {
            "username": player.username
        }
        requests.post(url, data)

    @staticmethod
    def delete(id):
        url = GAME_SERVER_URL + f"api/players/{id}"
        requests.delete(url)