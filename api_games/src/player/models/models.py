from api_games.src import db


class Player(db.Model):
    """ Class represents player of the game in database. Table name is set to 'player'.

    Player model contains:
    id - id of the player in database.
    username - username of the player.
    score - score of the player in the game.
    """

    __tablename__ = "player"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    games = db.relationship('Playing', back_populates='player')

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username
        }

    def dict_with_score(self, game_id):
        dict_form = self.to_dict()
        game = list(
            filter(lambda playing: playing.game_id == game_id, self.games)
        )
        if not game:
            return dict_form

        dict_form['score'] = game[0].score
        return dict_form

    def __repr__(self):
        return f"Player(id={self.id}, username={self.username})"
