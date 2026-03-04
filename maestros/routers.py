from flask import render_template, request, redirect, url_for, Blueprint
import forms
from models import db, Maestros 


maestros_bp = Blueprint('maestros', __name__)

@maestros_bp.route('/Maestros', methods=['GET', 'POST'])
def lista_maestros():
    create_form = forms.UserForm(request.form)
    todos_maestros = Maestros.query.all() 
    return render_template("maestros/listadoMaestros.html", 
                           form=create_form, 
                           maestros=todos_maestros)

@maestros_bp.route('/Maestros/agregar', methods=['GET', 'POST'])
def insertar():  
    form = forms.UserForm2(request.form)
    
    if request.method == 'POST' and form.validate():
        nuevo_maes = Maestros(
            nombre=form.nombre.data,
            apellidos=form.apellidos.data,
            email=form.email.data,
            especialidad=form.especialidad.data
        )
        db.session.add(nuevo_maes)
        db.session.commit()
        return redirect(url_for('maestros.lista_maestros'))
    
    return render_template("maestros/insertar.html", form=form)

@maestros_bp.route('/Maestros/editar', methods=['GET', 'POST'])
def modificar_maestro():
    form = forms.UserForm2(request.form)
    
    if request.method == 'GET':
        id = request.args.get('id')
        maes = Maestros.query.get(id) 
        if maes:
            form.id.data = maes.matricula
            form.nombre.data = maes.nombre
            form.apellidos.data = maes.apellidos
            form.email.data = maes.email
            form.especialidad.data = maes.especialidad 

    if request.method == 'POST' and form.validate():
        id = form.id.data
        maes = Maestros.query.get(id)
        
        maes.nombre = form.nombre.data
        maes.apellidos = form.apellidos.data
        maes.email = form.email.data
        maes.especialidad = form.especialidad.data 

        db.session.commit() 
        return redirect(url_for('maestros.lista_maestros'))

    return render_template("maestros/editarMaestros.html", form=form)

@maestros_bp.route('/Maestros/detalles')
def detalles_maestro():
    id = request.args.get('id')
    maes = Maestros.query.get(id)
    if maes:
        return render_template("maestros/detallesMaestros.html", 
                               nombre=maes.nombre, 
                               apellidos=maes.apellidos, 
                               email=maes.email,
                               especialidad=maes.especialidad)
    return redirect(url_for('maestros.lista_maestros'))

@maestros_bp.route('/Maestros/eliminar', methods=['GET', 'POST'])
def eliminar_maestro():
    form = forms.UserForm2(request.form)
    if request.method == 'GET':
        id = request.args.get('id')
        maes = Maestros.query.get(id)
        if maes:
            form.id.data = maes.matricula
            form.nombre.data = maes.nombre
            form.apellidos.data = maes.apellidos
            form.email.data = maes.email
            form.especialidad.data = maes.especialidad 

    if request.method == 'POST':
        id = form.id.data
        maes = Maestros.query.get(id)
        if maes:
            db.session.delete(maes)
            db.session.commit()
        return redirect(url_for('maestros.lista_maestros'))

    return render_template("maestros/eliminarMaestros.html", form=form)