# Import db from root src module
from api_games.src import db


class Player(db.Model):
    """ Class represents player of the game in database. Table name is set to 'player'.

    Player model contains:
    id - id of the player in database.
    username - username of the player,
    """

    __tablename__ = "player"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey("game.id"), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "game_id": self.game_id
        }

    def __repr__(self):
        return f"Player(id={self.id}, username={self.username})"
