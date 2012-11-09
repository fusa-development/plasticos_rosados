#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv
import sqlite3 as bdapi

def cargar_bd(lista):
	
	bbdd=bdapi.connect('stock_rosarino.db')
	cursor=bbdd.cursor()
	for x in lista:
		print x
		cursor.execute("INSERT INTO bazar(codigo, nro_art, descripcion, marca, costo, precio, stk_disp, pnt_rep, aviso, sw) VALUES (?,?,?,?,?,?,?,?,?,?)",(x))
	print "termine"
	bbdd.commit()
	cursor.close()
	bbdd.close()
	
def leer_csv():
	m1 = open("./listas/bazar/csv_bazar.csv","r")
	m1_csv = csv.reader(m1)
	lista= []
	for nro_art, descripcion, marca, costo in m1_csv:
		lista.append([0, nro_art, descripcion, marca, costo, costo,0,0,False,True])
	cargar_bd(lista)
	
def leer_bd():
		
	bbdd=bdapi.connect('productos.db')
	cursor=bbdd.cursor()
	cursor.execute("SELECT * FROM bombas")
	for tupla in cursor.fetchall():
		print tupla
	print "Me lei todo"
	bbdd.commit()
	cursor.close()
	bbdd.close()

#leer_bd()
leer_csv()
