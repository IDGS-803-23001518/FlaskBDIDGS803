from . import cursos
from flask import Flask, render_template, request, redirect, url_for
from flask import flash
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
from flask_migrate import Migrate
from flask import g
import forms

from models import db
from models import Alumnos
from models import Maestros
from models import Curso
from models import Inscripcion

@cursos.route("/cursos", methods=['GET','POST'])
def lista_cursos():
	create_form=forms.UserForm(request.form)
	curso=Curso.query.all()
	return render_template("cursos/cursos.html",form=create_form,curso=curso)

@cursos.route("/addcursos", methods=['GET','POST'])
def add_cursos():
    create_form = forms.CursoForm(request.form)
    maestros = Maestros.query.all()
    create_form.maestro_id.choices = [(m.matricula, f"{m.nombre} ({m.matricula})") for m in maestros]
    if request.method == 'POST' and create_form.validate():
        curso = Curso(
            nombre=create_form.nombre.data,
            descripcion=create_form.descripcion.data,
            maestro_id=create_form.maestro_id.data
        )
        db.session.add(curso)
        db.session.commit()
        return redirect(url_for('cursos.lista_cursos'))
    return render_template("cursos/AgregarCurso.html", form=create_form)

@cursos.route("/detallesCurso", methods=['GET','POST'])
def detallesCurso():
	create_form=forms.CursoForm(request.form)
	if request.method=='GET':
		id=request.args.get('id')
		curso=db.session.query(Curso).filter(Curso.id==id).first()
		id=request.args.get('id')
		nombre=curso.nombre
		descripcion=curso.descripcion
		nombreM=curso.maestro.nombre
		apellidosM=curso.maestro.apellidos
		emailM=curso.maestro.email
		matriculaM=curso.maestro.matricula
	return render_template("cursos/DetallesCurso.html",nombre=nombre,descripcion=descripcion,nombreM=nombreM,apellidosM=apellidosM,emailM=emailM,matriculaM=matriculaM)

@cursos.route("/modificarCurso", methods=['GET','POST'])
def modificarCurso():
    create_form = forms.CursoForm(request.form)
    maestros = Maestros.query.all()
    create_form.maestro_id.choices = [(m.matricula, f"{m.nombre} ({m.matricula})") for m in maestros]
    if request.method == 'GET':
        id = request.args.get('id')
        curso = db.session.query(Curso).filter(Curso.id == id).first()
        create_form.id.data = curso.id
        create_form.nombre.data = curso.nombre
        create_form.descripcion.data = curso.descripcion
        create_form.maestro_id.data = curso.maestro_id
    if request.method == 'POST':
        id = create_form.id.data
        curso = db.session.query(Curso).filter(Curso.id == id).first()
        curso.nombre = create_form.nombre.data
        curso.descripcion = create_form.descripcion.data
        curso.maestro_id = create_form.maestro_id.data
        db.session.commit()
        return redirect(url_for('cursos.lista_cursos'))
    return render_template("cursos/ModificarCurso.html", form=create_form)

@cursos.route("/eliminarCurso", methods=['GET','POST'])
def eliminarCurso():
    create_form = forms.CursoForm(request.form)
    maestros = Maestros.query.all()
    create_form.maestro_id.choices = [(m.matricula, f"{m.nombre} ({m.matricula})") for m in maestros]
    if request.method == 'GET':
        id = request.args.get('id')
        curso = Curso.query.get_or_404(id)
        create_form.id.data = curso.id
        create_form.nombre.data = curso.nombre
        create_form.descripcion.data = curso.descripcion
        create_form.maestro_id.data = curso.maestro_id
    if request.method == 'POST':
        id = create_form.id.data
        curso = Curso.query.get_or_404(id)
        curso.alumnos.clear()
        db.session.delete(curso)
        db.session.commit()
        return redirect(url_for('cursos.lista_cursos'))
    return render_template("cursos/EliminarCurso.html", form=create_form)


@cursos.route("/inscripciones")
def inscripciones():
    id = request.args.get("id")
    curso = Curso.query.get_or_404(id)
    form = forms.InscripcionForm()
    alumnos = Alumnos.query.all()
    form.curso_id.data = curso.id
    form.alumno_id.choices = [(a.id, f"{a.nombre} {a.apellidos}") for a in alumnos]
    return render_template("cursos/Inscripciones.html",curso=curso,form=form,alumnos=alumnos)

@cursos.route("/agregarAlumnoCurso", methods=["POST"])
def agregarAlumnoCurso():
    form = forms.InscripcionForm()
    alumnos = Alumnos.query.all()
    form.alumno_id.choices = [(a.id, f"{a.nombre} {a.apellidos}") for a in alumnos]

    if form.validate_on_submit():
        curso = Curso.query.get_or_404(form.curso_id.data)
        alumno = Alumnos.query.get_or_404(form.alumno_id.data)
        if alumno in curso.alumnos:
            flash("El alumno ya está inscrito en este curso", "error")
        else:
            curso.alumnos.append(alumno)
            db.session.commit()
            flash("Alumno agregado correctamente", "success")
        return redirect(url_for("cursos.inscripciones", id=curso.id))
    flash("Error en el formulario", "error")
    return redirect(url_for("cursos.lista_cursos"))

@cursos.route("/eliminarAlumnoCurso", methods=["POST"])
def eliminarAlumnoCurso():
    form = forms.InscripcionForm()
    alumnos = Alumnos.query.all()
    form.alumno_id.choices = [(a.id, f"{a.nombre} {a.apellidos}") for a in alumnos]
    
    if form.validate_on_submit():
        curso = Curso.query.get_or_404(form.curso_id.data)
        alumno = Alumnos.query.get_or_404(form.alumno_id.data)
        if alumno not in curso.alumnos:
            flash("El alumno no está inscrito en este curso", "error")
        else:
            curso.alumnos.remove(alumno)
            db.session.commit()
            flash("Alumno eliminado correctamente", "success")
        return redirect(url_for("cursos.inscripciones", id=curso.id))
    flash("Error en el formulario", "error")
    return redirect(url_for("cursos.lista_cursos"))