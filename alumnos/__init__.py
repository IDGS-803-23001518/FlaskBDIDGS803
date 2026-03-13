from flask import Blueprint

alumnosr=Blueprint(
    'alumnos',
    __name__,
    template_folder='templates',
    static_folder='static')
from . import routes