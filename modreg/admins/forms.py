import flask_wtf
import wtforms
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError

class AddLectureForm(flask_wtf.FlaskForm):
    #Login required
    lnum = wtforms.IntegerField("Lecture Number", validators=[DataRequired()])
    quota = wtforms.IntegerField("Quota", validators=[DataRequired()])
    deadline = wtforms.StringField("Deadline (in YYYY-MM-DD HH:MM:SS)", validators=[DataRequired()])
    submit = wtforms.SubmitField("Register")

class AddSlotForm(flask_wtf.FlaskForm):
    #Login required
    t_start = wtforms.StringField("Lecture Start Time (in HH:MM:SS)", validators=[DataRequired()])
    t_end = wtforms.StringField("Lecture End Time (in HH:MM:SS)", validators=[DataRequired()])
    day = wtforms.StringField("Day", validators=[DataRequired()])
    submit = wtforms.SubmitField("Register")