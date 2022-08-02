from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, EqualTo, ValidationError
from flask_login import current_user
import main


class SignUpForm(FlaskForm):
    email_address = StringField("Email Address", [DataRequired()])
    first_name = StringField("First Name", [DataRequired()])
    last_name = StringField("Last Name", [DataRequired()])
    password1 = PasswordField("Password", [DataRequired()])
    password2 = PasswordField(
        "Password confirm",
        [DataRequired(), EqualTo("password1", "Passwords must match")],
    )
    submit = SubmitField("Sign Up")

    def validate_email_address(self, email_address):
        user = main.User.query.filter_by(email_address=self.email_address.data).first()
        if user:
            raise ValidationError(
                "Email already exists. Sign in or use another email address."
            )


class SignInForm(FlaskForm):
    email_address = StringField("Email Address", [DataRequired()])
    password = PasswordField("Password", [DataRequired()])
    submit = SubmitField("Sign In")


class UpdateAccountInformationForm(FlaskForm):
    email_address = StringField("Email Address", [DataRequired()])
    first_name = StringField("First Name", [DataRequired()])
    last_name = StringField("Last Name")
    submit = SubmitField("Update Info")

    def validate_email_address(self, email_address):
        if current_user.email_address != self.email_address.data:
            user = main.User.query.filter_by(
                email_address=self.email_address.data
            ).first()
            if user:
                raise ValidationError(
                    "Email already exists. Sign in or use another email address."
                )


class BookAdditionForm(FlaskForm):
    title = StringField("Title", [DataRequired()])
    author = StringField("Author", [DataRequired()])
    submit = SubmitField("Submit")
