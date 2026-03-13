from wtforms import Form
from wtforms import StringField,IntegerField,PasswordField, SelectField, HiddenField
from wtforms import EmailField
from wtforms import validators
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired

class UserForm(Form):
    id=IntegerField('id')
    nombre=StringField('Nombre',[
        validators.DataRequired(message='El campo es requerido'),
        validators.length(min=4,max=10,message='Ingrese nombre valido')
    ])
    apellidos=StringField('Apellidos',[
        validators.DataRequired(message='El campo es requerido')
    ])
    email=EmailField('Correo',[
        validators.DataRequired(message='El campo es requerido'),
        validators.Email(message='Ingrese un correo valido')
    ])
    telefono=StringField('Telefono',[
        validators.DataRequired(message='El campo es requerido')
    ])

class MaestroForm(Form):
    matricula=IntegerField('matricula')
    nombre=StringField('Nombre',[
        validators.DataRequired(message='El campo es requerido'),
        validators.length(min=4,max=10,message='Ingrese nombre valido')
    ])
    apellidos=StringField('Apellidos',[
        validators.DataRequired(message='El campo es requerido')
    ])
    especialidad=StringField('Especialidad',[
        validators.DataRequired(message='El campo es requerido')
    ])
    email=EmailField('Correo',[
        validators.DataRequired(message='El campo es requerido'),
        validators.Email(message='Ingrese un correo valido')
    ])

class CursoForm(Form):
    id=IntegerField('')
    nombre=StringField('Nombre',[
        validators.DataRequired(message='El campo es requerido'),
        validators.length(min=4,max=30,message='Ingrese nombre valido')
    ])
    descripcion=StringField('Descripción',[
        validators.DataRequired(message='El campo es requerido')
    ])
    maestro_id = SelectField(
        'Maestro',
        choices=[],
        coerce=int,
        validators=[DataRequired()]
    )
class InscripcionForm(FlaskForm):
    curso_id = HiddenField(validators=[DataRequired()])
    alumno_id = SelectField("Alumno", coerce=int)