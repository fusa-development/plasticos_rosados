#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sqlite3 as bdapi
import os
def caracteres_validos(palabra):
	correcto=True
	try:
		for letra in range(len(palabra)):
			#si no es mayuscula y no es miniscula y no es espacio
			if not ( 65 <=ord(palabra[letra]) <=90 )and not (97<=ord(palabra[letra])<= 122) and not ord(palabra[letra]) == 32:
				#si no es numero,si no es   , - . /  y no es ( )
				if not ( 48 <=ord(palabra[letra]) <=57 ) and not ( 44 <=ord(palabra[letra]) <=47 ) and not ( 40 <=ord(palabra[letra]) <=41 ):
					correcto=False
					break
		return correcto
	except:
		return False

def codigo_no_repetido(liststore_elejido,entry):
	repetido=False
	for fila in range(len(liststore_elejido) ):
		if liststore_elejido[fila][0] == int(entry.get_text()):
			repetido=True
			break
	if repetido:
		return True
	else:
		return False

def articulo_no_repetido(rubro,nro_art,marca):
	ruta = os.getcwd()
	bbdd=bdapi.connect(ruta+'/Base_Datos/stock_rosarino.db')
	cursor=bbdd.cursor()
	cursor.execute("SELECT codigo FROM "+rubro+" WHERE nro_art=? AND marca=?",(nro_art,marca))
	nro_art = cursor.fetchone()
	cursor.close()
	bbdd.close()
	if nro_art == None:
		return True
	else:
		return False


def verificar_marca_existente(rubro,marca):
	ruta = os.getcwd()
	bbdd=bdapi.connect(ruta+'/Base_Datos/marcas_rosarinas.db')
	cursor=bbdd.cursor()
	cursor.execute("SELECT nombre FROM marca WHERE  nombre=? AND rubro=?",(marca,rubro))
	marca = cursor.fetchone()
	cursor.close()
	bbdd.close()
	if marca != None:
		return True
	else:
		return False

def es_int(valor):
	try:
		int(valor)
		return True
	except:
		return False

def es_float(valor):
	try:
		float(valor)
		return True
	except:
		return False


def codigo_no_repetido_modificado(liststore_elejido,entry,id_codigo):
	repetido=False
	for fila in range(len(liststore_elejido) ):
		if liststore_elejido[fila][0] == int(entry.get_text()) and int(entry.get_text()) != id_codigo :
			repetido=True
			break
	if repetido:
		return True
	else:
		return False

def articulo_no_repetido_modificado(liststore_elejido,entry,id_nro_art,entry_marca):
	marca = entry_marca.get_text()
	repetido=False
	for fila in range(len(liststore_elejido) ):
		if marca != liststore_elejido[fila][3] :
			if liststore_elejido[fila][1] == int(entry.get_text()) :
				repetido=True
				break
	if repetido:
		return True
	else:
		return False
