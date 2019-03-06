from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, SubmitField, TextAreaField, IntegerField, FloatField, FieldList, FormField, RadioField
from wtforms.validators import DataRequired, Optional

class ValuationForm(FlaskForm):
    param = StringField('Parametre : ')
    valua = FloatField('Valuation : ')

class ModuleFileForm(FlaskForm):
    file = FileField("File : ", validators=[DataRequired()])
    submit = SubmitField('Load file')

class ModuleForm(FlaskForm):
    text = TextAreaField("Text : ", validators=[DataRequired()])
    nb_run = IntegerField("Number of run : ", validators=[Optional()])
    len_run = IntegerField("Length of run : ", validators=[Optional()])
    params = StringField("Params Valuation (Optional) : ", validators=[Optional()])
    #radio = RadioField("Number of params : ", choices=[('2d','Une dimension'),('3d','Deux dimensions')])
    submit = SubmitField('Send')
