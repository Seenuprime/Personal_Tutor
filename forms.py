from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import Length

class Query(FlaskForm):
    query = StringField('Query', validators=[Length(min=2, max=1000)])
    submit = SubmitField("Ask")

class Topic_Query(FlaskForm):
    query = TextAreaField('Topic_Query', validators=[Length(min=2, max=1000)])
    submit = SubmitField("Ask")