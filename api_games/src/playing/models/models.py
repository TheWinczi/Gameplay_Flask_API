from api_games.src import db


class Playing(db.Model):
    """ Class represents playing in game being player.
    Class is additional table needed to handle many-to-many relationship between
    Player and Game objects.

    Additional fields of model:
        score - score of the player in the game.
    """
    __tablename__ = 'playing'

    id = db.Column(db.Integer, primary_key=True)

    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'))

    # Additional fields for many-to-many table
    score = db.Column(db.Integer, nullable=False, default=0)

    # fields for back populates relation
    game = db.relationship('Game', back_populates='players')
    player = db.relationship('Player', back_populates='games')

    def __repr__(self):
        return f"Playing(player_id={self.player_id}, game_id={self.game_id}, score={self.score})"
