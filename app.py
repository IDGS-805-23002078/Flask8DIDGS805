from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate
from config import DevelopmentConfig
import forms
from models import db, Alumnos
from maestros.routers import maestros_bp 
from cursos import cursos


app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

app.register_blueprint(maestros_bp)

db.init_app(app)
csrf = CSRFProtect(app)
migrate = Migrate(app, db)
app.register_blueprint(cursos)

@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404

@app.route("/index")
def index():
    alumnos = Alumnos.query.all()
    return render_template("index.html", alumnos=alumnos)

@app.route("/alumno/<int:id>/cursos")
def cursos_alumno(id):

    alumno = Alumnos.query.get_or_404(id)

    return render_template(
        "alumno_cursos.html",
        alumno=alumno
    )


@app.route('/Alumnos', methods=['GET', 'POST'])
def alumnos():
    create_form = forms.UserForm(request.form)

    if request.method == 'POST' and create_form.validate():
        alum = Alumnos(
            nombre=create_form.nombre.data,
            apellidos=create_form.apellidos.data,
            telefono=create_form.telefono.data,
            email=create_form.email.data  )

        db.session.add(alum)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template("Alumnos.html", form=create_form)


@app.route("/detalles")
def detalles():
    id = request.args.get('id')
    alum1 = Alumnos.query.get(id)

    return render_template("detalles.html",
                           id=alum1.id,
                           nombre=alum1.nombre,
                           apellidos=alum1.apellidos,
                           email=alum1.email,
                           telefono=alum1.telefono)


@app.route("/modificar", methods=["GET", "POST"])
def modificar():
    create_form = forms.UserForm(request.form)

    if request.method == 'GET':
        id = request.args.get('id')
        alum1 = Alumnos.query.get(id)

        create_form.id.data = alum1.id
        create_form.nombre.data = alum1.nombre
        create_form.apellidos.data = alum1.apellidos
        create_form.telefono.data = alum1.telefono
        create_form.email.data = alum1.email

    if request.method == 'POST' and create_form.validate():
        id = create_form.id.data
        alum = Alumnos.query.get(id)

        alum.nombre = create_form.nombre.data
        alum.apellidos = create_form.apellidos.data
        alum.telefono = create_form.telefono.data
        alum.email = create_form.email.data

        db.session.commit()
        return redirect(url_for("index"))

    return render_template("modificar.html", form=create_form)


@app.route("/eliminar", methods=["GET", "POST"])
def eliminar():
    create_form = forms.UserForm(request.form)

    if request.method == 'GET':
        id = request.args.get('id')
        alum1 = Alumnos.query.get(id)

        create_form.id.data = alum1.id
        create_form.nombre.data = alum1.nombre
        create_form.apellidos.data = alum1.apellidos
        create_form.telefono.data = alum1.telefono
        create_form.email.data = alum1.email

    if request.method == 'POST':
        id = create_form.id.data
        alum = Alumnos.query.get(id)

        db.session.delete(alum)
        db.session.commit()

        return redirect(url_for("index"))

    return render_template("eliminar.html", form=create_form)

@app.route("/alumno/buscar", methods=['GET'])
def buscar_historial_alumno():
    matricula = request.args.get('matricula')
    
    if not matricula:
        flash("Por favor ingresa una matrícula", "warning")
        return redirect(url_for('index'))
    
    alumno = Alumnos.query.get(matricula)
    
    if not alumno:
        flash(f"No se encontró ningún alumno con la matrícula {matricula}", "danger")
        return redirect(url_for('index'))

    return render_template(
        "alumno_historial.html",
        alumno=alumno,
        cursos=alumno.cursos
    )


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)