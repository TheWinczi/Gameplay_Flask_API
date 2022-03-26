from flask_restful import reqparse

player_post_args = reqparse.RequestParser()
player_post_args.add_argument("username", type=str, help="Username of player", required=False)
player_post_args.add_argument("game_id", type=int, help="Game id of player", required=False)

player_put_args = reqparse.RequestParser()
player_put_args.add_argument("username", type=str, help="Username of player", required=False)
player_put_args.add_argument("score", type=int, help="Game score of player", required=False)
player_put_args.add_argument("game_id", type=int, help="Game id of player", required=False)
