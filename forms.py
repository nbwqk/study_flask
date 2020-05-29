from wtforms import Form,StringField,PasswordField,BooleanField,SubmitField
from wtforms.validators import DataRequired,Length
from flask_wtf import FlaskForm

class LoginForm(FlaskForm):
    username=StringField('Usename',validators=[DataRequired()])
    password=PasswordField('Password',validators=[DataRequired(),Length(8,128)])
    remember=BooleanField('Remember me')
    submit=SubmitField('Log in')