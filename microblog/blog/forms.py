from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired


class BlogForm(FlaskForm):
    title = StringField(
        "Title", validators=[DataRequired(message="Title is required.")]
    )
    content = TextAreaField(
        "Content",
        validators=[DataRequired(message="Content is required.")],
        render_kw={"rows": 20, "cols": 11},
    )
