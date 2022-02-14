from api_players.src.player.service.player_service import PlayerService
from api_players.src.player.event.player_event import PlayerEvent
from api_players.src.player.requests_parsers.requests_parsers import *
from api_players.src.player.models.models import Player

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
        }, 200

    def post(self):
        args = player_post_args.parse_args()
        player = Player(username=args["username"], image_file=args["image_file"])
        result = PlayerService.create(player)
        if result != PlayerService.FAIL_RETURN_VALUE:
            PlayerEvent.create(player)
            return {"location": f"/api/players/{result}"}, 201
        else:
            return Response(status=500)


class PlayersByIdAPI(Resource):
    """ Players by id API controller.
    Responsible for getting, updating and deleting players with provided id.

    Source url is /api/players/<int:id>
    """

    def get(self, id):
        player = PlayerService.find(id)
        if player:
            return player.to_full_dict()
        else:
            return Response(status=404)

    def put(self, id: int):
        args = player_put_args.parse_args()
        player = PlayerService.find(id)
        if player:
            if "username" in args and args["username"] is not None:
                player.username = args["username"]
            if "image_file" in args and args["image_file"] is not None:
                player.image_file = args["image_file"]

            result = PlayerService.update(player)
            if result == PlayerService.SUCCESS_RETURN_VALUE:
                return Response(status=202)
            else:
                return Response(status=500)
        else:
            return Response(status=404)

    def delete(self, id: int):
        player = PlayerService.find(id)
        if player:
            result = PlayerService.delete(id)
            if result == PlayerService.SUCCESS_RETURN_VALUE:
                PlayerEvent.delete(id)
                return Response(status=202)
            else:
                return Response(status=500)
        else:
            return Response(status=404)
