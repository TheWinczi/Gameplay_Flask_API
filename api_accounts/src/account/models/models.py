from datetime import datetime

# Import db object from root src module
from api_accounts.src import db
from api_accounts.src.account.roles.account_roles import Roles


class Base(db.Model):
    """ Base class implements default fields needed in all models """
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=datetime.now)
    date_modified = db.Column(db.DateTime, default=datetime.now)


class Account(Base):
    """ Class represents user account.
    Table name is set to 'account'.
    """
    __tablename__ = "account"

    login = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(256), nullable=False)
    role = db.Column(db.Integer, nullable=False, default=Roles.GUEST.to_int)

    @property
    def short_dict(self):
        return {
            'id': self.id,
            'login': self.login,
            'role': Roles.to_str(self.role)
        }

    @property
    def full_dict(self):
        return {
            'id': self.id,
            'login': self.login,
            'role': Roles.to_str(self.role),
            'date_created': self.date_created.isoformat(),
            'date_modified': self.date_modified.isoformat()
        }

    def __repr__(self):
        return f"Account(id={self.id}, login={self.login}, role={self.role})"
