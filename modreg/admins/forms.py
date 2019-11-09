import flask_wtf
import wtforms
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError

class AddLectureForm(flask_wtf.FlaskForm):
    #Login required
    lnum = wtforms.IntegerField("Lecture Number", validators=[DataRequired()])
    quota = wtforms.IntegerField("Quota", validators=[DataRequired()])
    deadline = wtforms.StringField("Deadline (in YYYY-MM-DD HH:MM:SS)", validators=[DataRequired()])
    submit = wtforms.SubmitField("Register")