from distutils.core import setup
import py2exe

setup(name="Compiladores 2009-2010",
	version="1.5",
	description="Entrega final Compiladores",
	author="Grupo 27",
	console=["sintactico.py"],
	script=["sintactico.py"]
)