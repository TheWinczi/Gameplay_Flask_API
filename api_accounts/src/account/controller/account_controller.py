import json

from api_accounts.src.account.service.account_service import AccountService
from api_accounts.src.account.requests_parsers.requests_parsers import *
from api_accounts.src.account.roles.account_roles import Roles
from api_accounts.src.account.models.models import Account
from api_accounts.src.decorators.logging import log_info

from flask import Response
from flask_restful import Resource


class AccountsAPI(Resource):
    """ Accounts API controller.
    Responsible for getting all existing accounts and adding new accounts.

    Source url is /api/accounts
    """

    @log_info()
    def get(self):
        accounts = AccountService.find_all()
        return {
            "accounts": list(
                map(lambda account: account.short_dict, accounts)
            )
        }, 200

    @log_info()
    def post(self):
        args = account_post_args.parse_args()

        login = args.get('login', None)
        password = args.get('password', None)
        if (login and password) is None:
            return Response(status=400)

        account = Account(login=login, password=password)
        if (role := args.get('role', None)) is not None:
            account.role = Roles.from_str(role)

        result = AccountService.create(account)
        if result != AccountService.FAIL_RETURN_VALUE:
            return {"location": f"/api/accounts/{result}"}, 201
        else:
            return Response(status=500)


class AccountsByLoginAPI(Resource):
    """ Accounts by login API controller.
    Responsible for getting, updating and deleting accounts with provided login.

    Source url is /api/accounts/<login>
    """
    @log_info()
    def get(self, login: str):
        account = AccountService.find_by_login(login)
        if account:
            account_dict = account.full_dict
            return account_dict
        else:
            return Response(status=404)

    @log_info()
    def put(self, login: str):
        args = account_put_args.parse_args()
        account = AccountService.find_by_login(login)
        if not account:
            return Response(status=404)

        if "password" in args and args["password"] is not None:
            account.password = args["password"]
        if "role" in args and args["role"] is not None:
            account.role = Roles.from_str(args['role'])

        result = AccountService.update(account)
        if result == AccountService.SUCCESS_RETURN_VALUE:
            return Response(status=202)
        else:
            return Response(status=500)

    @log_info()
    def delete(self, login: str):
        account = AccountService.find_by_login(login)
        if not account:
            return Response(status=404)

        result = AccountService.delete(account.id)
        if result == AccountService.SUCCESS_RETURN_VALUE:
            return Response(status=202)
        else:
            return Response(status=500)


class AccountsAuthenticationAPI(Resource):
    """ Accounts API controller for accounts authentication.

    Source url is /api/accounts/authentication
    """
    def post(self):
        args = account_authentication_post_args.parse_args()

        login = args.get('login', None)
        password = args.get('password', None)
        if (login and password) is None:
            return Response(status=400)

        account = AccountService.find_by_login(login)
        if account is None:
            return Response(status=404)

        if account.password != password:
            return Response(status=401)

        response = {
            'role': Roles.to_str(account.role)
        }
        return Response(json.dumps(response), status=200)
