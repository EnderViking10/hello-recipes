from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms.fields.numeric import IntegerField
from wtforms.fields.simple import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


class RecipeForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    time = IntegerField('Time', validators=[DataRequired()])
    ingredients = TextAreaField('Ingredients (one per line)', validators=[DataRequired()])
    instructions = TextAreaField('Instructions (one step per line)', validators=[DataRequired()])
    image = FileField('Image', validators=[
        FileAllowed(['jpg', 'png'], 'Images only!')
    ])
    submit = SubmitField('Create Recipe')
