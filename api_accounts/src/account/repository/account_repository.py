from api_accounts.src import db
from api_accounts.src.account.models.models import Account
from api_accounts.src.decorators.logging import log_info

from datetime import datetime

from sqlalchemy import exc


class AccountRepository(object):
    """ Class responsible for adding, saving, deleting and
    updating accounts models directly in database. """

    SUCCESS_RETURN_VALUE = 1
    FAIL_RETURN_VALUE = 0

    @staticmethod
    @log_info()
    def find_all():
        """ Find all existing Account objects in database.

        Returns
        -------
        accounts : list[Account]
            List of founded Account objects.
        """
        return list(Account.query.all())

    @staticmethod
    @log_info()
    def find_by_login(login: str):
        """ Find account model with a provided id.

        Parameters
        ----------
        login : str
            Login of the account to find.

        Returns
        -------
        account : Account
            Founded account object. None otherwise.

        Raises
        ------
        TypeError
            If type of provided login is different than allowed.
        """
        if not isinstance(login, str):
            raise TypeError(f"Illegal type of argument. Login could be only str not {type(login)}")

        account = Account.query.filter_by(login=login).first()
        if account:
            return account
        else:
            return None

    @staticmethod
    @log_info()
    def find(id: int):
        """ Find account model with a provided id.

        Parameters
        ----------
        id : int
            Id of the account to find.

        Returns
        -------
        account : Account
            Founded account object. None otherwise.

        Raises
        ------
        TypeError
            If type of provided id is different than allowed.
        """
        if not isinstance(id, int):
            raise TypeError(f"Illegal type of argument. Id could be only int not {type(id)}")

        account = Account.query.filter_by(id=id).first()
        if account:
            return account
        else:
            return None

    @staticmethod
    @log_info()
    def create(account: Account,
               fail_return_value=FAIL_RETURN_VALUE):
        """ Create new instance of Account object in database.

        Parameters
        ----------
        account : Account
            Account object to add.

        fail_return_value : Any
            Optional. Value returned when creating failed.

        Returns
        -------
        id : int
            Id of created account. However when creating failed `fail_return_value` is returned.

        Raises
        ------
        TypeError
            If type of provided account is different than allowed. Default = `FAIL_RETURN_VALUE`
        """
        if not isinstance(account, Account):
            raise TypeError(f"Illegal type of argument. Account could be only Account not {type(account)}")

        try:
            db.session.add(account)
            db.session.commit()
            return account.id
        except exc.SQLAlchemyError:
            return fail_return_value

    @staticmethod
    @log_info()
    def delete(id: int,
               success_return_value=SUCCESS_RETURN_VALUE,
               fail_return_value=FAIL_RETURN_VALUE):
        """ Delete Account object  containing provided id from database.

        Parameters
        ----------
        id : int
            Id of the account to delete.

        success_return_value : Any
            Optional. Value returned when deleting succeed.

        fail_return_value : Any
            Optional. Value returned when deleting failed.

        Returns
        -------
        result : Any
            When deleting succeed `success_return_value` is returned.
            When deleting failed `fail_return_value` is returned.

        Raises
        ------
        TypeError
            If type of provided id is different than allowed.
        """
        if not isinstance(id, int):
            raise TypeError(f"Illegal type of argument. Id could be only int not {type(id)}")

        account = Account.query.filter_by(id=id).first()
        if account:
            try:
                db.session.query(Account).filter_by(id=id).delete(synchronize_session='fetch')
                db.session.commit()
                return success_return_value
            except exc.SQLAlchemyError:
                return fail_return_value
        else:
            return fail_return_value

    @staticmethod
    @log_info()
    def update(account: Account,
               success_return_value=SUCCESS_RETURN_VALUE,
               fail_return_value=FAIL_RETURN_VALUE):
        """ Update existing account with provided account object

        Parameters
        ----------
        account : Account
            Account object to add.

        success_return_value : Any
            Optional. Value returned when updating succeed.

        fail_return_value : Any
            Optional. Value returned when updating failed.

        Returns
        -------
        result : Any
            When deleting succeed `success_return_value` is returned.
            When deleting failed `fail_return_value` is returned.

        Raises
        ------
        TypeError
            If type of provided account is different than allowed.
        """
        if not isinstance(account, Account):
            raise TypeError(f"Illegal type of argument. Account could be only Account not {type(account)}")

        existing_account = Account.query.filter_by(id=account.id).first()
        if existing_account:
            existing_account.date_modified = datetime.now()
            try:
                db.session.add(account)
                db.session.commit()
                return success_return_value
            except exc.SQLAlchemyError:
                return fail_return_value
        else:
            return fail_return_value
