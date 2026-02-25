from wtforms import Form
from wtforms import IntegerField, StringField, EmailField
from wtforms import validators


class UserForm(Form):

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

    correo = EmailField("Correo", [
        validators.Email(message="Ingresa un correo válido")
    ])


class UserForm2(Form):

    id = IntegerField("ID", [
        validators.DataRequired(message="El campo es requerido"),
        validators.NumberRange(min=1)
    ])

    nombre = StringField("Nombre", [
        validators.DataRequired(message="El campo es requerido")
    ])

    apellidos = StringField("Apellidos", [
        validators.DataRequired(message="El campo es requerido")
    ])

    telefono = StringField("Telefono", [
        validators.DataRequired(message="El campo es requerido")
    ])

    email = EmailField("Correo", [
        validators.Email(message="Ingresa un correo válido")
    ])