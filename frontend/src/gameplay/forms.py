import requests

from frontend.config import PLAYERS_SERVER_URL

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed

from wtforms import StringField, SubmitField, TextAreaField, PasswordField
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired, Length, Optional, ValidationError


# ---------- ---------- ----------
#          ADDING FORMS
# ---------- ---------- ----------

class AddPlayerForm(FlaskForm):
    """ Form allows to create new Player object.

    Player object fields possible to fill:
    - username (required)
    - image_file (optional)
    """
    username = StringField("Username",
                           validators=[DataRequired(), Length(min=2, max=50)])
    image_file = FileField("Image File",
                           validators=[FileAllowed(['jpg', 'jpeg', 'png', 'bmp'])])
    submit = SubmitField("Add")

    def validate_username(self, username):
        if not isinstance(username.data, str):
            raise ValidationError('Invalid username. Could be only string.')
        if not (2 <= len(username.data) <= 50):
            raise ValidationError('Invalid username length. Could be only between 2 and 50 signs.')

        players = requests.get(f'{PLAYERS_SERVER_URL}api/players')
        players = players.json().get('players', [])
        usernames = list(map(
            lambda player: player['username'], players
        ))
        if username.data in usernames:
            raise ValidationError('That username is taken. Please choose different username.')


class AddGameForm(FlaskForm):
    """ Form allows to edit Game objects

    Game object fields possible to edit:
    - description (optional)
    """
    description = TextAreaField("Description",
                                widget=TextArea(),
                                validators=[Optional(), Length(min=1, max=400)])
    submit = SubmitField("Add")

    def validate_description(self, description):
        if not isinstance(description.data, str):
            raise ValidationError('Invalid description. Could be only string.')
        if not (1 <= len(description.data) <= 400):
            raise ValidationError('Invalid description length. Could be only between 1 and 400 signs.')


# ---------- ---------- ----------
#          EDITING FORMS
# ---------- ---------- ----------

class EditPlayerForm(FlaskForm):
    """ Form allows to edit Player objects

    Player object fields possible to edit:
    - username (required)
    - image_file (optional)
    """
    username = StringField("Username",
                           validators=[DataRequired(), Length(min=2, max=50)])
    image_file = FileField("Image File",
                           validators=[DataRequired(), FileAllowed(['jpg', 'jpeg', 'png', 'bmp'])])
    submit = SubmitField("Save")

    def validate_username(self, username):
        if not isinstance(username.data, str):
            raise ValidationError('Invalid username. Could be only string.')
        if not (2 <= len(username.data) <= 50):
            raise ValidationError('Invalid username length. Could be only between 2 and 50 signs.')

        players = requests.get(f'{PLAYERS_SERVER_URL}api/players')
        players = players.json().get('players', [])
        usernames = list(map(
            lambda player: player['username'], players
        ))
        if username.data in usernames:
            raise ValidationError('That username is taken. Please choose different username.')


class EditGameForm(FlaskForm):
    """ Form allows to edit Game objects

    Game object fields possible to edit:
    - description (optional)
    """
    description = TextAreaField("Description",
                                widget=TextArea(),
                                validators=[Optional(), Length(min=1, max=400)])
    submit = SubmitField("Save")

    def validate_description(self, description):
        if not isinstance(description.data, str):
            raise ValidationError('Invalid description. Could be only string.')
        if not (1 <= len(description.data) <= 400):
            raise ValidationError('Invalid description length. Could be only between 1 and 400 signs.')


# ---------- ---------- ----------
#           SIGNING FORMS
# ---------- ---------- ----------

class AccountSignInForm(FlaskForm):
    """ Form allows to sign in.
    """
    login = StringField("Login",
                        validators=[DataRequired(), Length(min=1, max=50)])
    password = PasswordField("Password",
                             validators=[DataRequired(), Length(min=1, max=256)])
    submit = SubmitField("Sing in")

    def validate_login(self, login: str):
        if not isinstance(login, str):
            raise ValidationError('Invalid login. Could be only string.')
        if not (1 <= len(login) <= 50):
            raise ValidationError('Invalid login length. Could be only between 1 and 50 signs.')

    def validate_password(self, password: str):
        if not isinstance(password, str):
            raise ValidationError('Invalid password. Could be only string.')
        if not (1 <= len(password) <= 256):
            raise ValidationError('Invalid password length. Could be only between 1 and 256 signs.')
