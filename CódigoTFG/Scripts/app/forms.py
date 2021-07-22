from wtforms import Form
from wtforms import StringField, TextField
from wtforms.fields.html5 import EmailField


class CommentForm(Form):
    calle = StringField('Calle')
    distrito = StringField('Distrito')
    propietario = StringField('Propietario')
    alarma = StringField('Alarma')
    