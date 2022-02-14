from datetime import datetime

# Import db object from root src module
from api_players.src import db


class Base(db.Model):
    """ Base class implements default fields needed in all models """
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=datetime.now)
    date_modified = db.Column(db.DateTime, default=datetime.now)


class Player(Base):
    """ Class represents player of the game in database. Table name is set to 'player'.

    Player model contains:
    username - username of the player,
    image_file - image file name of the player.
    """
    __tablename__ = "player"

    username = db.Column(db.String(50), nullable=False)
    image_file = db.Column(db.String(30), nullable=True, default="default_player_image.png")

    def to_full_dict(self):
        """ Convert full Player object to dictionary

        Returns
        -------
        player : dict
            Converted Player object to dictionary
        """
        return {
            "id": self.id,
            "date_created": self.date_created.isoformat(),
            "date_modified": self.date_modified.isoformat(),
            "username": self.username,
            "image_file": self.image_file
        }

    def to_short_dict(self):
        """ Convert short Player object to dictionary

        Returns
        -------
        player : dict
            Converted Player object to dictionary
        """
        return {
            "id": self.id,
            "username": self.username
        }

    def __repr__(self):
        return f"Player(id={self.id}, username={self.username}, image_file={self.image_file})"
