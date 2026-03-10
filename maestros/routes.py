from . import maestros
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

@maestros.route('/maestros', methods=['GET','POST'])
def listado_maestros():
    create_form = forms.MaestroForm(request.form)
    lista_maestros = Maestros.query.all()
    return render_template("maestros/listadoMaes.html",
                           form=create_form,
                           maestros=lista_maestros)

@maestros.route("/addmaestro", methods=['GET','POST'])
def addmaestro():
	create_form=forms.MaestroForm(request.form)
	if request.method=='POST':
		maes=Maestros(nombre=create_form.nombre.data,
			   apellidos=create_form.apellidos.data,
               especialidad=create_form.especialidad.data,
			   email=create_form.email.data)
		db.session.add(maes)
		db.session.commit()
		return redirect(url_for("maestros.listado_maestros"))
	return render_template("maestros/maestros.html",form=create_form)

@maestros.route("/detallesMaes", methods=['GET','POST'])
def detalles():
	create_form=forms.UserForm(request.form)
	if request.method=='GET':
		matricula=request.args.get('matricula')
		maes=db.session.query(Maestros).filter(Maestros.matricula==matricula).first()
		matricula=request.args.get('matricula')
		nombre=maes.nombre
		apellidos=maes.apellidos
		email=maes.email
		matricula=maes.matricula
	return render_template("maestros/detallesMaes.html",nombre=nombre,apellidos=apellidos,email=email,matricula=matricula)

@maestros.route("/modificarMaes", methods=['GET','POST'])
def modificar():
	create_form=forms.MaestroForm(request.form)
	if request.method=='GET':
		matricula=request.args.get('matricula')
		maes=db.session.query(Maestros).filter(Maestros.matricula==matricula).first()
		create_form.matricula.data=request.args.get('matricula')
		create_form.nombre.data=maes.nombre
		create_form.apellidos.data=maes.apellidos
		create_form.especialidad.data=maes.especialidad
		create_form.email.data=maes.email
	if request.method=='POST':
		matricula=create_form.matricula.data
		maes=db.session.query(Maestros).filter(Maestros.matricula==matricula).first()
		maes.nombre=create_form.nombre.data
		maes.apellidos=create_form.apellidos.data
		maes.especialidad=create_form.especialidad.data
		maes.email=create_form.email.data
		db.session.add(maes)
		db.session.commit()
		return redirect(url_for('maestros.listado_maestros'))
	return render_template("maestros/modificarMaes.html",form=create_form)

@maestros.route("/eliminarMaes", methods=['GET','POST'])
def eliminar():
	create_form=forms.MaestroForm(request.form)
	if request.method=='GET':
		matricula=request.args.get('matricula')
		maes=db.session.query(Maestros).filter(Maestros.matricula==matricula).first()
		create_form.matricula.data=request.args.get('matricula')
		create_form.nombre.data=maes.nombre
		create_form.apellidos.data=maes.apellidos
		create_form.especialidad.data=maes.especialidad
		create_form.email.data=maes.email
	if request.method=='POST':
		matricula=create_form.matricula.data
		maes = Maestros.query.get(matricula)
		db.session.delete(maes)
		db.session.commit()
		return redirect(url_for('maestros.listado_maestros'))
	return render_template("maestros/eliminarMaes.html",form=create_form)

@maestros.route('/perfil/<nombre>')
def perfil(nombre):
    return f"Perfil de {nombre}"