from distutils.core import setup
from setuptools import find_packages
import py2exe

setup(name='Rosario Plasticos',
version='1.0',
description='Control de Stock ',
author='Fusa Desarrolos',
author_email='fusadesarrollos@gmail.com',
license='GPL',
windows=[ {'script': 'venta_principal.py'
} ],
options={'py2exe': {
'bundle_files': 3,
'includes': 'cairo, pango, pangocairo, atk, gobject, gio, gtk, pygtk,gtk.keysyms',} },
data_files=['ventana_principal.glade','recordatorios.txt'],

packages = find_packages(),
zipfile=None
)