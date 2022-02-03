from ..service.player_service import PlayerService
from ..requests_parsers.requests_parsers import *
from ..models.models import Player

from flask import Response
from flask_restful import Resource


class PlayersAPI(Resource):
    """ Players API controller.
    Responsible for getting all existing players and adding new players.

    Source url is /api/players
    """
    def get(self):
        players = PlayerService.find_all()
        return {
            "players": list(
                map(lambda player: player.to_short_dict(), players)
            )
        }

    def post(self):
        args = player_post_args.parse_args()
        player = Player(args["username"], args["image_file"])
        player_id = PlayerService.create(player)
        return {"location": f"/api/players/{player_id}"}, 201


class PlayersByIdAPI(Resource):
    """ Players by id API controller.
    Responsible for getting, updating and deleting player with provided id.

    Source url is /api/players/<int:id>
    """
    def get(self, id):
        player = PlayerService.find(id)
        if player:
            return player.to_full_dict()
        else:
            return Response(status=404)

    def put(self, id):
        args = player_put_args.parse_args()
        player = PlayerService.find(id)
        if player:
            if "username" in args and args["username"] is not None:
                player.username = args["username"]
            if "image_file" in args and args["image_file"] is not None:
                player.image_file = args["image_file"]
            PlayerService.update(player)
            return Response(status=202)
        else:
            return Response(status=404)

    def delete(self, id):
        player = PlayerService.find(id)
        if player:
            PlayerService.delete(id)
            return Response(status=202)
        else:
            return Response(status=404)
