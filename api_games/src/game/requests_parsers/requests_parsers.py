from flask_restful import reqparse

game_post_args = reqparse.RequestParser()
game_post_args.add_argument("description", type=str, help="Description of game", required=False)

game_put_args = reqparse.RequestParser()
game_put_args.add_argument("description", type=str, help="Description of game", required=False)
