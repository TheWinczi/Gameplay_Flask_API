from flask_restful import reqparse
from werkzeug.datastructures import FileStorage


account_post_args = reqparse.RequestParser()
account_post_args.add_argument("login", type=str, help="Login of account", required=True)
account_post_args.add_argument("password", type=str, help="Password of account", required=True)
account_post_args.add_argument("role", type=str, help="Role of account", required=False)

account_put_args = reqparse.RequestParser()
account_put_args.add_argument("password", type=str, help="Password of account", required=False)
account_put_args.add_argument("role", type=str, help="Role of account", required=False)

account_authentication_post_args = reqparse.RequestParser()
account_authentication_post_args.add_argument("login", type=str, help="Login of account", required=True)
account_authentication_post_args.add_argument("password", type=str, help="Password of account", required=True)
