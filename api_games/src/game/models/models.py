from datetime import datetime

from api_games.src import db


class Base(db.Model):
    """ Base class implements default fields needed in all models """
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, nullable=True, default=datetime.now)


class Game(Base):
    """ Class represents game in database. Table name is set to 'game'.

    Game model contains:
    description - description of the game,
    players - players of the game.
    """

    __tablename__ = "game"

    description = db.Column(db.String(400), nullable=True, default="")
    players = db.relationship('Playing', back_populates='game')

    def to_short_dict(self):
        return {
            "id": self.id,
            "description": self.description,
        }

    def to_full_dict(self):
        return {
            "id": self.id,
            "date_created": self.date_created.isoformat(),
            "description": self.description,
        }

    def __repr__(self):
        return f"Game(id={self.id}, description={self.description})"
