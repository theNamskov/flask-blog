from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from blog.database_structure import User

class RegistrationForm(FlaskForm):
     """
     Controls registration form and user sign up. 
     Inherits form properties and methods from flask_wtf.FlaskForm
     """   
  #language = SelectField('Language', validators=[DataRequired()], coerce='French')

     '''
          username field of type StringField
          formfield validators by wtforms.validators
          Data is required
          Minimum of 2 and maximum of 20 characters required

     '''
     username = StringField('Username', validators=[DataRequired(),Length(min=2, max=20)])

     '''
          email field of type StringField
          formfield validators by wtforms.validators
          Data is required

     '''
     email = StringField('Email', validators=[DataRequired(), Email()])

     '''
          password field of type PasswordField
          formfield validators by wtforms.validators
          Data is required

     '''
     password = PasswordField('Password', validators=[DataRequired()])

     '''
          confirm_password field of type PasswordField
          formfield validators by wtforms.validators
          Data is required
          EqualTo validator employed as this must equal password field for success

     '''
     confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password',message='Inconsistent password confirmation!')])

     '''
          submit field of type SumbitField

     '''
     submit = SubmitField('Sign Up')

     def validate_username(self, username):
          user = User.query.filter_by(username=username.data).first()

          if user:
               raise ValidationError('Username taken!')

     def validate_email(self, email):
          user = User.query.filter_by(email=email.data).first()

          if user:
               raise ValidationError('Email already taken!')            


class LoginForm(FlaskForm):

     email = StringField('Email', validators=[DataRequired(), Email()])

     password = PasswordField('Password', validators=[DataRequired()])
     
     remember = BooleanField('Remember Me')

     submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
     #language = SelectField('Language', validators=[DataRequired()], coerce='French')

     username = StringField('Username', validators=[
     DataRequired(),Length(min=2, max=20)
     ])

     email = StringField('Email', validators=[DataRequired(), Email()])

     picture = FileField('Update profile picture', validators=[FileAllowed('jpg','png')])

     submit = SubmitField('Update')

     def validate_username(self, username):
          if username.data != current_user.username:
               user = User.query.filter_by(username=username.data).first()
               if user:
                    raise ValidationError('Username taken!')
          else:
               raise ValidationError('No change detected!')
               

     def validate_email(self, email):
          if email.data != current_user.email:           
               user = User.query.filter_by(email=email.data).first()
               if user:
                    raise ValidationError('Email already taken!')
          else:
               raise ValidationError('No change detected!')
          
