from api_games.src.player.service.player_service import PlayerService
from api_games.src.playing.service.playing_service import PlayingService
from api_games.src.game.service.game_service import GameService
from api_games.src.decorators.logging import log_info
from api_games.src.playing.requests_parsers.requests_parsers import *

from flask import Response
from flask_restful import Resource


class GamesByIdPlayersByIdAPI(Resource):
    """ Games by id players API controller.
    Responsible for management of players of games with provided ids.

    Source url is /api/games/<int:game_id>/players/<int:player_id>
    """

    @staticmethod
    @log_info()
    def get(game_id, player_id):
        player = PlayerService.find(player_id)
        if player is None:
            return Response(status=404)

        playing = PlayingService.find(player_id, game_id)
        if playing is None:
            return Response(status=404)

        player = player.to_dict()
        player['score'] = playing.score
        return player

    @staticmethod
    @log_info()
    def delete(game_id: int, player_id: int):
        player = PlayerService.find(player_id)
        if player is None:
            return Response(status=404)

        game = GameService.find(game_id)
        if game is None:
            return Response(status=404)

        result = PlayingService.delete(player_id, game_id)
        if result != PlayingService.SUCCESS_RETURN_VALUE:
            return Response(status=500)
        else:
            return Response(status=202)

    @staticmethod
    @log_info()
    def put(game_id: int, player_id: int):
        args = playing_put_args.parse_args()

        print(player_id, game_id)

        player = PlayerService.find(player_id)
        if player is None:
            return Response(status=404)

        game = GameService.find(game_id)
        if game is None:
            return Response(status=404)

        playing = PlayingService.find(player_id, game_id)
        if playing is None:
            return Response(status=404)

        if (score := args.get('score', None)) is not None:
            playing.score = score

        result = PlayingService.update(playing)
        if result != PlayingService.SUCCESS_RETURN_VALUE:
            return Response(status=500)
        else:
            return Response(status=202)

    @staticmethod
    @log_info()
    def post(game_id: int, player_id: int):
        args = playing_post_args.parse_args()

        player = PlayerService.find(player_id)
        if player is None:
            return Response(status=404)

        game = GameService.find(game_id)
        if game is None:
            return Response(status=404)

        if (score := args.get('score', None)) is not None:
            playing_result = PlayingService.connect_player_and_game(player, game, score)
        else:
            playing_result = PlayingService.connect_player_and_game(player, game)

        game_result = GameService.update(game)

        if playing_result != PlayingService.SUCCESS_RETURN_VALUE or game_result != GameService.SUCCESS_RETURN_VALUE:
            return Response(status=500)
        else:
            return Response(status=201)
