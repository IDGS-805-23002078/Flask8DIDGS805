from flask_wtf import FlaskForm  
from wtforms import StringField, IntegerField, EmailField, HiddenField, validators

class UserForm(FlaskForm): 
    id = HiddenField('id') 

    nombre = StringField("Nombre", [
        validators.DataRequired(message="El campo es requerido"),
        validators.Length(min=4, max=50)
    ])

    apellidos = StringField("Apellidos", [
        validators.DataRequired(message="El campo es requerido")
    ])

    telefono = StringField("Telefono", [
        validators.DataRequired(message="El campo es requerido"),
        validators.Length(min=10, max=15)
    ])

    email = EmailField("Correo", [
        validators.Email(message="Ingresa un correo válido")
    ])

class UserForm2(FlaskForm): 
    id = IntegerField("ID", [
        validators.Optional() 
    ])

    nombre = StringField("Nombre", [
        validators.DataRequired(message="El campo es requerido")
    ])

    apellidos = StringField("Apellidos", [
        validators.DataRequired(message="El campo es requerido")
    ])

    especialidad = StringField("Especialidad", [
        validators.Optional()
    ])

    email = EmailField("Correo", [
        validators.DataRequired(message="El campo es requerido"),
        validators.Email(message="Ingresa un correo válido")
    ])