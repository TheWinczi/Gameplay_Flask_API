from api_accounts.src.account.models.models import Account
from api_accounts.src.account.roles.account_roles import Roles
from api_accounts.src.account.service.account_service import AccountService


def _initialize_accounts():
    """ Initialize accounts models.

    Notes
    -----
    Function creates 3 random Accounts in different
    configuration and adds these to database.
    """
    accounts = [
        Account(login='admin', password='admin', role=Roles.ADMIN.to_int),
    ]

    for account in accounts:
        AccountService.create(account)


def initialize_models():
    """ Initialize all needed models.

    Notes
    -----
    Function executes functions responsible for initialization
    different type of models inside the module.
    It is recommended to use that function to not worrying about function execution order.

    Function initializes:
        1. accounts
    """
    _initialize_accounts()
