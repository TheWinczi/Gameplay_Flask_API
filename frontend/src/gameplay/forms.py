from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField, PasswordField
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired, Length, Optional


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


class AddGameForm(FlaskForm):
    """ Form allows to edit Game objects

    Game object fields possible to edit:
    - description (optional)
    """
    description = TextAreaField("Description",
                                widget=TextArea(),
                                validators=[Optional(), Length(min=1, max=400)])
    submit = SubmitField("Add")


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


class EditGameForm(FlaskForm):
    """ Form allows to edit Game objects

    Game object fields possible to edit:
    - description (optional)
    """
    description = TextAreaField("Description",
                                widget=TextArea(),
                                validators=[Optional(), Length(min=1, max=400)])
    submit = SubmitField("Save")


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
