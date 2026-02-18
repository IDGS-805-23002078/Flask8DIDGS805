from wtforms import Form
from wtforms import IntegerField, StringField, PasswordField
from wtforms import EmailField
from wtforms import validators

class UserForm(Form):
    id=IntegerField("id",[
        validators.DataRequired(message="El campo es requerido"),
        validators.NumberRange(min=100, max=1000, message="Ingrese valor valido")
    ])
    nombre=StringField("nombre",
    [validators.DataRequired(message="El campo es requerido"),
     validators.length(min=4, max=10, message="El campo es requerido")])
    
    apaterno=StringField("apellido Paterno",
    [validators.DataRequired(message="El campo es requerido")])

    correo=EmailField("coreo",
    [validators.Email(message="Ingresa un correo valido")])