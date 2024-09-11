from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo


class RegistrationForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[
            DataRequired(message="Username is required."),
            Length(min=4, max=20),
        ],
    )
    email = EmailField("Email", validators=[DataRequired(message="Email is required.")])
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(message="Password is required."),
            EqualTo("confirm_password", message="Confirm password doesn't match."),
        ],
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[DataRequired(message="Confirm password is required.")],
    )


class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(message="Email is required.")])
    password = PasswordField(
        "Password", validators=[DataRequired(message="Password is required.")]
    )
