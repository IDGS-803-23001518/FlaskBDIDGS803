from . import alumnosr
from flask import Flask, render_template, request, redirect, url_for
from flask import flash
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
from flask_migrate import Migrate
from flask import g
import forms

from models import db
from models import Alumnos
from models import Curso

@alumnosr.route("/index", methods=['GET','POST'])
def listado_alumnos():
	create_form=forms.UserForm(request.form)
	alumno=Alumnos.query.all()
	return render_template("alumnos/index.html",form=create_form,alumno=alumno)

@alumnosr.route("/alumnos", methods=['GET','POST'])
def alumnos():
	create_form=forms.UserForm(request.form)
	if request.method=='POST':
		alum=Alumnos(nombre=create_form.nombre.data,
			   apellidos=create_form.apellidos.data,
			   email=create_form.email.data,
			   telefono=create_form.telefono.data)
		db.session.add(alum)
		db.session.commit()
		return redirect(url_for('alumnos.listado_alumnos'))
	return render_template("alumnos/Alumnos.html",form=create_form)


@alumnosr.route("/detalles", methods=['GET','POST'])
def detalles():
	create_form=forms.UserForm(request.form)
	if request.method=='GET':
		id=request.args.get('id')
		alum1=db.session.query(Alumnos).filter(Alumnos.id==id).first()
		id=request.args.get('id')
		nombre=alum1.nombre
		apellidos=alum1.apellidos
		email=alum1.email
		telefono=alum1.telefono
	return render_template("alumnos/detalles.html",nombre=nombre,apellidos=apellidos,email=email,telefono=telefono)


@alumnosr.route("/modificar", methods=['GET','POST'])
def modificar():
	create_form=forms.UserForm(request.form)
	if request.method=='GET':
		id=request.args.get('id')
		alum1=db.session.query(Alumnos).filter(Alumnos.id==id).first()
		create_form.id.data=request.args.get('id')
		create_form.nombre.data=alum1.nombre
		create_form.apellidos.data=alum1.apellidos
		create_form.email.data=alum1.email
		create_form.telefono.data=alum1.telefono
	if request.method=='POST':
		id=create_form.id.data
		alum1=db.session.query(Alumnos).filter(Alumnos.id==id).first()
		alum1.nombre=create_form.nombre.data
		alum1.apellidos=create_form.apellidos.data
		alum1.email=create_form.email.data
		alum1.telefono=create_form.telefono.data
		db.session.add(alum1)
		db.session.commit()
		return redirect(url_for('alumnos.listado_alumnos'))
	return render_template("alumnos/modificar.html",form=create_form)


@alumnosr.route("/eliminar", methods=['GET','POST'])
def eliminar():
	create_form=forms.UserForm(request.form)
	if request.method=='GET':
		id=request.args.get('id')
		alum1=db.session.query(Alumnos).filter(Alumnos.id==id).first()
		create_form.id.data=request.args.get('id')
		create_form.nombre.data=alum1.nombre
		create_form.apellidos.data=alum1.apellidos
		create_form.email.data=alum1.email
		create_form.telefono.data=alum1.telefono
	if request.method=='POST':
		id=create_form.id.data
		alum = Alumnos.query.get(id)
		db.session.delete(alum)
		db.session.commit()
		return redirect(url_for('alumnos.listado_alumnos'))
	return render_template("alumnos/eliminar.html",form=create_form)

@alumnosr.route("/alumnoCursos")
def cursos():
    id = request.args.get("id")
    alumnos = Alumnos.query.get_or_404(id)
    form = forms.InscripcionForm()
    curso = Curso.query.all()
    form.alumno_id.data = Alumnos.id
    return render_template("alumnos/cursosAlumno.html",curso=curso,form=form,alumnos=alumnos)