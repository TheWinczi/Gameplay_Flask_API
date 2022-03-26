from flask_restful import reqparse
from werkzeug.datastructures import FileStorage


player_post_args = reqparse.RequestParser()
player_post_args.add_argument("username", type=str, help="Username of player", required=True)
player_post_args.add_argument("image_file", type=str, help="Image file of player", required=False)
player_post_args.add_argument("image", type=FileStorage, location="files", help="Image of player", required=False)

player_put_args = reqparse.RequestParser()
player_put_args.add_argument("username", type=str, help="Username of player", required=False)
player_put_args.add_argument("image_file", type=dict, help="Image file of player", required=False)
player_put_args.add_argument("image", type=FileStorage, location="files", help="Image of player", required=False)

player_image_put_args = reqparse.RequestParser()
player_image_put_args.add_argument("image", type=FileStorage, location="files", help="Image of player", required=True)
