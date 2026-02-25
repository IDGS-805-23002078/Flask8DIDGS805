from flask import Flask, render_template

from flask import Flask, render_template,request,redirect,url_for 
from flask_wtf.csrf import CSRFProtect
from flask import flash 
from config import DevelopmentConfig
import forms
from models import db,Alumnos
from flask_migrate import Migrate

app = Flask(__name__)

app.config.from_object(DevelopmentConfig)
db.init_app(app)
csrf=CSRFProtect(app)
migrate=Migrate(app,db)
@app.errorhandler(404) 
def page_not_fount(error):
 return render_template("404.html"),404

@app.route("/index")
def index():
    alumnos = Alumnos.query.all() 
    return render_template("index.html", alumnos=alumnos)

@app.route('/Alumnos', methods=['GET', 'POST'])
def alumnos():
    create_form = forms.UserForm(request.form)

    if request.method == 'POST' and create_form.validate():

        alum = Alumnos(
            nombre=create_form.nombre.data,
            apellidos=create_form.apellidos.data,
            telefono=create_form.telefono.data,
            email=create_form.correo.data
        )

        db.session.add(alum)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template("Alumnos.html", form=create_form)

@app.route("/detalles", methods=['GET', 'POST'])
def detalles():
    if request.method=='GET':
         id=request.args.get('id')
         #select * from alumnos where id=id
         alum1=db.session.query(Alumnos).filter(Alumnos.id==id).first()
         nombre=alum1.nombre
         apellidos=alum1.apellidos
         email=alum1.email     
    return render_template("detalles.html",
                       id=id,
                       nombre=nombre,
                       apellidos=apellidos,
                       email=email,
                       telefono=alum1.telefono)

@app.route("/modificar", methods=["GET", "POST"])
def modificar():
    create_form = forms.UserForm2(request.form)
    if request.method == 'GET':
        id = request.args.get('id')
        # select * from alumnos where id=id
        alum1 = db.session.query(Alumnos).filter(Alumnos.id == id).first()
        create_form.id.data = alum1.id
        create_form.nombre.data = alum1.nombre
        create_form.apellidos.data = alum1.apellidos
        create_form.telefono.data = alum1.telefono
        create_form.email.data = alum1.email
    if request.method == 'POST':
        id= create_form.id.data
        alum = db.session.query(Alumnos).filter(Alumnos.id==id).first()
        alum.nombre=create_form.nombre.data
        alum.apellidos=create_form.apellidos.data
        alum.telefono = create_form.telefono.data
        alum.email=create_form.email.data
        db.session.add(alum)
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("modificar.html", form=create_form)
 
@app.route("/eliminar", methods=["GET", "POST"])
def eliminar():
    create_form = forms.UserForm2(request.form)
    if request.method == 'GET':
        id = request.args.get('id')
        # select * from alumnos where id=id
        alum1 = db.session.query(Alumnos).filter(Alumnos.id == id).first()
        create_form.id.data = alum1.id
        create_form.nombre.data = alum1.nombre
        create_form.apellidos.data = alum1.apellidos
        create_form.email.data = alum1.email
    if request.method == 'POST':
        id= create_form.id.data
        alum=Alumnos.query.get(id)
        db.session.delete(alum)
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("eliminar.html", form=create_form)



if __name__ == '__main__':
	with app.app_context():
		db.create_all()
	app.run()
	
#insertar17-02-2026 comit 