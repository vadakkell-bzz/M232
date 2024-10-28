from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired

# Formular für die Buchhinzufügung
class BookForm(FlaskForm):
    title = StringField('Titel', validators=[DataRequired()])  # Titel des Buches
    author = StringField('Autor', validators=[DataRequired()])  # Autor des Buches
    year = IntegerField('Jahr', validators=[DataRequired()])  # Veröffentlichungsjahr
    submit = SubmitField('Buch hinzufügen')  # Button zum Hinzufügen
