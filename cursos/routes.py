from . import cursos
from flask import render_template, request, redirect, url_for, flash
from models import db, Curso, Maestros, Alumnos 


@cursos.route("/cursos")
def listar_cursos():
    cursos_lista = Curso.query.all()
    return render_template("cursos/listadoCursos.html", cursos=cursos_lista)

@cursos.route("/cursos/<int:curso_id>/agregar_alumno", methods=['GET', 'POST'])
def agregar_alumno(curso_id):

    curso = Curso.query.get_or_404(curso_id)
    alumnos = Alumnos.query.all()

    if request.method == 'POST':

        alumno_id = request.form.get('alumno_id')

        if not alumno_id:
            flash("Selecciona un alumno", "danger")
            return redirect(url_for('cursos.agregar_alumno', curso_id=curso_id))

        alumno = Alumnos.query.get(int(alumno_id))

        if alumno in curso.alumnos:
            flash("El alumno ya está inscrito en este curso", "warning")
        else:
            curso.alumnos.append(alumno)
            db.session.commit()
           

        return redirect(url_for('cursos.ver_alumnos', curso_id=curso_id))

    return render_template(
        "cursos/agregarAlum.html",
        curso=curso,
        alumnos=alumnos
    )

@cursos.route("/cursos/<int:curso_id>/alumnos")
def ver_alumnos(curso_id):

    curso = Curso.query.get_or_404(curso_id)

    return render_template(
        "cursos/verAlum.html",
        curso=curso
    )

@cursos.route("/cursos/nuevo", methods=['GET', 'POST'])
def nuevo_curso():

    if request.method == 'POST':

        maestro_id = request.form.get('maestro_id')

        if not maestro_id:
            flash("Debes seleccionar un maestro", "danger")
            return redirect(url_for('cursos.nuevo_curso'))

        curso = Curso(
            nombre=request.form['nombre'],
            descripcion=request.form['descripcion'],
            maestro_id=int(maestro_id)
        )

        db.session.add(curso)
        db.session.commit()

        return redirect(url_for('cursos.listar_cursos'))

    return render_template(
        "cursos/crear.html",
        maestros=Maestros.query.all()
    )


@cursos.route("/cursos/eliminar/<int:id>", methods=['GET', 'POST'])
def eliminar_curso(id):

    curso = Curso.query.get_or_404(id)

    if request.method == 'POST':
        db.session.delete(curso)
        db.session.commit()
        return redirect(url_for('cursos.listar_cursos'))

    return render_template("cursos/eliminar.html", curso=curso)


@cursos.route("/cursos/editar/<int:id>", methods=['GET', 'POST'])
def editar_curso(id):

    curso = Curso.query.get_or_404(id)

    if request.method == 'POST':

        maestro_id = request.form.get('maestro_id')

        if not maestro_id:
            flash("Debes seleccionar un maestro", "danger")
            return redirect(url_for('cursos.editar_curso', id=id))

        curso.nombre = request.form['nombre']
        curso.descripcion = request.form['descripcion']
        curso.maestro_id = maestro_id  # SIN int()

        db.session.commit()

        return redirect(url_for('cursos.listar_cursos'))

    return render_template(
        "cursos/editar.html",
        curso=curso,
        maestros=Maestros.query.all()
    )

@cursos.route("/cursos/detalles/<int:id>")
def detalles_curso(id):
    # Obtenemos el objeto completo con sus relaciones (maestro y alumnos)
    curso = Curso.query.get_or_404(id)

    return render_template(
        "cursos/detalles.html",
        curso=curso # Pasamos el objeto completo
    )

@cursos.route("/cursos/<int:curso_id>/alumnos/buscar", methods=['GET'])
def buscar_alumno_en_curso(curso_id):
    curso = Curso.query.get_or_404(curso_id)
    matricula = request.args.get('matricula')
    
    # Si hay una matrícula, filtramos los alumnos del curso que coincidan con ese ID
    if matricula:
        # Filtramos en la relación de alumnos del curso
        resultados = [a for a in curso.alumnos if str(a.id) == matricula]
    else:
        resultados = curso.alumnos

    return render_template(
        "cursos/verAlum.html", 
        curso=curso, 
        alumnos=resultados,
        busqueda=matricula
    )