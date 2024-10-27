from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Length

class Query(FlaskForm):
    query = StringField('Query', validators=[Length(min=2, max=1000)])
    submit = SubmitField("Ask")