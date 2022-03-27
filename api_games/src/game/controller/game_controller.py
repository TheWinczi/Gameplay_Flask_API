from api_games.src.game.service.game_service import GameService
from api_games.src.player.service.player_service import PlayerService
from api_games.src.game.requests_parsers.requests_parsers import *
from api_games.src.game.models.models import Game
from api_games.src.decorators.logging import log_info

from flask import Response, request
from flask_restful import Resource


class GamesAPI(Resource):
    """ Games API controller.
    Responsible for getting all existing games and adding new games.

    Source url is /api/games
    """

    @log_info()
    def get(self):
        games = GameService.find_all()
        return {
            "games": list(
                map(lambda game: game.to_short_dict(), games)
            )
        }, 200

    @log_info()
    def post(self):
        args = game_post_args.parse_args()
        game = Game(description=args["description"])
        result = GameService.create(game)
        if result != GameService.FAIL_RETURN_VALUE:
            return {"location": f"/api/games/{result}"}, 201
        else:
            return Response(status=500)


class GamesByIdAPI(Resource):
    """ Games by id API controller.
    Responsible for getting, updating and deleting games with provided id.

    Source url is /api/games/<int:game_id>
    """

    @log_info()
    def get(self, game_id: int):
        game = GameService.find(game_id)
        if game:
            return game.to_full_dict()
        else:
            return Response(status=404)

    @log_info()
    def put(self, game_id: int):
        args = game_put_args.parse_args()
        game = GameService.find(game_id)
        if game:
            if "description" in args and args["description"] is not None:
                game.description = args["description"]
            result = GameService.update(game)
            if result == GameService.SUCCESS_RETURN_VALUE:
                return Response(status=202)
            else:
                return Response(status=500)
        else:
            return Response(status=404)

    @log_info()
    def delete(self, game_id: int):
        game = GameService.find(game_id)
        if game:
            result = GameService.delete(game_id)
            if result == GameService.SUCCESS_RETURN_VALUE:
                return Response(status=202)
            else:
                return Response(status=500)
        else:
            return Response(status=404)


class GamesByIdPlayersAPI(Resource):
    """ Games by id players API controller.
    Responsible for getting players of the game with provided id.

    Source url is /api/games/<int:game_id>/players
    """

    @log_info()
    def get(self, game_id: int):
        game = GameService.find(game_id)
        if game:
            game_players = game.players
            return {
                "players": list(
                    map(lambda player: player.to_dict(), game_players)
                )
            }, 200
        else:
            return Response(status=404)


class GamesByIdPlayersByIdAPI(Resource):
    """ Games by id players API controller.
    Responsible for management of players of the game with provided id.

    Source url is /api/games/<int:game_id>/players/<int:player_id>
    """

    @log_info()
    def delete(self, game_id: int, player_id: int):
        game = GameService.find(game_id)
        if game:
            game_players = game.players
            player = list(
                filter(lambda p: p.id == player_id, game_players)
            )
            if player:
                for p in player:
                    p.game_id = None
                    PlayerService.update(p)
                return Response(status=202)
            else:
                return Response(status=404)
        else:
            return Response(status=404)

    @log_info()
    def put(self, game_id: int):
        pass
