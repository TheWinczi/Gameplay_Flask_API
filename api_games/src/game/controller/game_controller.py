from api_games.src.game.service.game_service import GameService
from api_games.src.game.requests_parsers.requests_parsers import *
from api_games.src.game.models.models import Game

from flask import Response
from flask_restful import Resource


class GamesAPI(Resource):
    """ Games API controller.
    Responsible for getting all existing games and adding new games.

    Source url is /api/games
    """

    def get(self):
        games = GameService.find_all()
        return {
            "games": list(
                map(lambda game: game.to_short_dict(), games)
            )
        }

    def post(self):
        args = game_post_args.parse_args()
        game = Game(description=args["description"])
        game_id = GameService.create(game)
        return {"location": f"/api/games/{game_id}"}, 201


class GamesByIdAPI(Resource):
    """ Games by id API controller.
    Responsible for getting, updating and deleting games with provided id.

    Source url is /api/games/<int:id>
    """

    def get(self, id):
        game = GameService.find(id)
        if game:
            return game.to_full_dict()
        else:
            return Response(status=404)

    def put(self, id):
        args = game_put_args.parse_args()
        game = GameService.find(id)
        if game:
            if "description" in args and args["description"] is not None:
                game.description = args["description"]
            GameService.update(game)
            return Response(status=202)
        else:
            return Response(status=404)

    def delete(self, id):
        game = GameService.find(id)
        if game:
            GameService.delete(id)
            return Response(status=202)
        else:
            return Response(status=404)


class GamesByIdPlayersAPI(Resource):
    """ Games by id players API controller.
    Responsible for getting players of the game with provided id.

    Source url is /api/games/<int:id>/players
    """

    def get(self, id):
        game = GameService.find(id)
        if game:
            game_players = game.players
            return {
                "players": list(
                    map(lambda player: player.to_dict(), game_players)
                )
            }
        else:
            return Response(status=404)
