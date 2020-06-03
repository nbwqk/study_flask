from wtforms import Form,StringField,PasswordField,BooleanField,SubmitField,TextAreaField
from wtforms.validators import DataRequired,Length
from flask_wtf import FlaskForm

class LoginForm(FlaskForm):
    username=StringField('Usename',validators=[DataRequired()])
    password=PasswordField('Password',validators=[DataRequired(),Length(8,128)])
    remember=BooleanField('Remember me')
    submit=SubmitField('Log in')

class NewNoteForm(FlaskForm):
    body=TextAreaField('Body',validators=[DataRequired()])
    submit=SubmitField('Save')

class EditNoteForm(NewNoteForm):
    submit=SubmitField('Update')

class DeleteNoteForm(FlaskForm):
    submit=SubmitField('Delete')