from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, BooleanField, SubmitField, TextAreaField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import Length, DataRequired, ValidationError, Email
from rrumble.models import User
from flask_login import current_user


class SignUp(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired(), Email(
        'make sure you typed a correct email')])
    password = PasswordField('password', validators=[
                             DataRequired(), Length(min=8, max=20)])
    submit = SubmitField('add user')


class Login(FlaskForm):
    email = StringField('email', validators=[DataRequired(), Email(
        'make sure you typed a correct email')])
    password = PasswordField('password', validators=[
                             DataRequired(), Length(min=8, max=20)])
    submit = SubmitField('login')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if not user:
            raise ValidationError('this user does not exist')


class MakeRequest(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired(), Email()])
    telephone = IntegerField('phone number', validators=[DataRequired()])
    subject = StringField('subject', validators=[DataRequired()])
    text = TextAreaField('message', validators=[Length(max=250)])
    file = FileField('attachment', validators=[FileAllowed(
        ['jpg', 'png', 'pdf', 'doc', 'docx', 'xls'])])
    submit = SubmitField('submit')

    def validate_email(self, email):
        if email.errors:
            raise ValidationError('make sure you typed a correct email')


class UpdateProf(FlaskForm):
    post = StringField('post')
    email = StringField('email', validators=[Email()])
    expertise = StringField('expertise')
    durat = IntegerField('duration of experience')
    photo = FileField('update photo', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('update profile')

    def validate_photo(self, photo):
        if photo.errors:
            raise ValidationError('make sure photo is jpg or png format')

    def validate_durat(self, durat):
        if durat.errors:
            raise ValidationError('enter a number instead of words')

    def validate_email(self, email):
        if email.data != current_user.email:
            check = User.query.filter_by(email=email.data)
            if check:
                raise ValidationError(
                    'this is either your old email or someone else is using it')
            elif email.errors:
                raise ValidationError('make sure you entered a correct email')


class PicMod(FlaskForm):
    photo = FileField('photo', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('ok')
