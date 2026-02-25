from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

class Alumnos(db.Model):
    __tablename__ = 'alumnos'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    apellidos = db.Column(db.String(50))
    telefono = db.Column(db.VARCHAR(15))  # telefono como string
    email = db.Column(db.String(120))
    create_date = db.Column(
        db.DateTime,
        default=datetime.datetime.now
    )