from api_players.src.player.service.player_service import PlayerService
from api_players.src.player.event.player_event import PlayerEvent
from api_players.src.player.requests_parsers.requests_parsers import *
from api_players.src.player.models.models import Player
from api_players.src.decorators.logging import log_info
from api_players.src.modules.utils import save_image, remove_file
from api_players.src import app

from flask import Response, send_file
from flask_restful import Resource
import os


class PlayersAPI(Resource):
    """ Players API controller.
    Responsible for getting all existing players and adding new players.

    Source url is /api/players
    """

    @log_info()
    def get(self):
        players = PlayerService.find_all()
        return {
            "players": list(
                map(lambda player: player.to_short_dict(), players)
            )
        }, 200

    @log_info()
    def post(self):
        args = player_post_args.parse_args()

        image_file = args.get("image_file", {})
        image_data = args.get("image", None)
        if image_file and image_data:
            image_data.filename = image_file
            image_fn = save_image(image_data, app.config.get("PLAYERS_IMAGES_DIR", "."))
        else:
            image_fn = "default_player_image.png"

        player = Player(username=args["username"], image_file=image_fn)
        result = PlayerService.create(player)
        if result != PlayerService.FAIL_RETURN_VALUE:
            PlayerEvent.create(player)
            return {"location": f"/api/players/{result}"}, 201
        else:
            return Response(status=500)


class PlayersByIdAPI(Resource):
    """ Players by id API controller.
    Responsible for getting, updating and deleting players with provided id.

    Source url is /api/players/<int:player_id>
    """

    @log_info()
    def get(self, player_id):
        player = PlayerService.find(player_id)
        if player:
            player_dict = player.to_full_dict()
            player_dict["image_url"] = f"api/players/{player.id}/image"
            return player_dict
        else:
            return Response(status=404)

    @log_info()
    def put(self, player_id: int):
        args = player_put_args.parse_args()
        player = PlayerService.find(player_id)
        if player:
            if "username" in args and args["username"] is not None:
                player.username = args["username"]
            if "image_file" in args and args["image_file"] is not None:
                player.image_file = args["image_file"]
            if "image" in args and args["image"] is not None:
                image_fn = save_image(args["image"], app.config.get("PLAYERS_IMAGES_DIR", "."))
                player.image_file = image_fn

            result = PlayerService.update(player)
            if result == PlayerService.SUCCESS_RETURN_VALUE:
                return Response(status=202)
            else:
                return Response(status=500)
        else:
            return Response(status=404)

    @log_info()
    def delete(self, player_id: int):
        player = PlayerService.find(player_id)
        if player:
            result = PlayerService.delete(player_id)
            if result == PlayerService.SUCCESS_RETURN_VALUE:
                PlayerEvent.delete(player_id)
                return Response(status=202)
            else:
                return Response(status=500)
        else:
            return Response(status=404)


class PlayerByIdImageAPI(Resource):
    """ Players by id API controller.
    Responsible for getting, updating and deleting players with provided id.

    Source url is /api/players/<int:player_id>/image
    """

    def get(self, player_id: int):
        player = PlayerService.find(player_id)
        if player:
            image_path = os.path.join(app.config.get("PLAYERS_IMAGES_DIR", "."), player.image_file)
            if os.path.exists(image_path):
                return send_file(image_path)
            else:
                return Response(status=404)
        else:
            return Response(status=404)

    def put(self, player_id):
        args = player_image_put_args.parse_args()
        player = PlayerService.find(player_id)
        if player:
            image_path = os.path.join(app.config.get("PLAYERS_IMAGES_DIR", "."), player.image_file)
            remove_file(image_path)
            image_fn = save_image(args.get("image", None), app.config.get("PLAYERS_IMAGES_DIR", "."))
            player.image_file = image_fn
            return Response(status=202)
        else:
            return Response(status=404)
