from flask_restful import reqparse

# ==============================
# PUT PLAYING REQUEST ARGUMENTS

playing_put_args = reqparse.RequestParser()
playing_put_args.add_argument('score', type=int, help='Score of the player in the game', required=False)

# ==============================
# POST PLAYING REQUEST ARGUMENTS

playing_post_args = reqparse.RequestParser()
playing_post_args.add_argument('score', type=int, help='Score of the player in the game', required=False)
