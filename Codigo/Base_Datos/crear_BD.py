#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sqlite3 as bdapi
import random
bbdd=bdapi.connect('stock_rosarino.db')
cursor=bbdd.cursor()

cursor.execute("""DROP TABLE IF EXISTS bazar""")
cursor.execute("""DROP TABLE IF EXISTS jugueteria""")
cursor.execute("""DROP TABLE IF EXISTS libreria""")

cursor.execute("""create table bazar (id INTEGER PRIMARY KEY,
				codigo text,
				nro_art int,
				descripcion text,
				marca text,
				costo float,
				precio float,
				stk_disp float,
				pnt_rep float,
				aviso bool,
				sw bool
				)""")
cursor.execute("""create table jugueteria (id INTEGER PRIMARY KEY,
				codigo text,
				nro_art int,
				descripcion text,
				marca text,
				costo float,
				precio float,
				stk_disp float,
				pnt_rep float,
				aviso bool,
				sw bool
				)""")
cursor.execute("""create table libreria (id INTEGER PRIMARY KEY,
				codigo text,
				nro_art int,
				descripcion text,
				marca text,
				costo float,
				precio float,
				stk_disp float,
				pnt_rep float,
				aviso bool,
				sw bool
				)""")

"""
aviso = False
lista_marca1=["almandoz","tramontina","florentina"]
lista_marca2=["daki","bloky","hasbro"]
lista_marca3=["rivadavia","exito","boligoma"]
for x in range(100): 
	
	lista1 = []
	lista2 = []
	lista3 = []

	lista1.append(str(x+40))
	lista2.append(str(x+200))
	lista3.append(str(x+1000))
	
	lista1.append(str(x+10))
	lista3.append(str(x+50))
	lista2.append(str(x+30))

	
	lista1.append("bazar "+str(x))
	lista2.append("jugueteria "+str(x))
	lista3.append("libreria "+str(x))
	
	lista1.append(random.choice(lista_marca1))
	lista2.append(random.choice(lista_marca2))
	lista3.append(random.choice(lista_marca3))
	
	lista1.append(random.randint(30,70))
	lista2.append(random.randint(30,70))
	lista3.append(random.randint(30,70))
	
	lista1.append(random.randint(30,50))
	lista2.append(random.randint(30,50))
	lista3.append(random.randint(30,50))
	
	lista1.append(random.randint(30,60))
	lista2.append(random.randint(30,60))
	lista3.append(random.randint(30,60))
	
	lista1.append(random.randint(30,60))
	lista2.append(random.randint(30,60))
	lista3.append(random.randint(30,60))
	
	
	lista1.append(aviso)
	lista2.append(aviso)
	lista3.append(aviso)
	
	lista1.append(True)
	lista2.append(True)
	lista3.append(True)

	
	print lista1
	print lista2
	print lista3

	cursor.execute(" INSERT INTO  bazar (codigo,nro_art, descripcion, marca, costo, precio, stk_disp, pnt_rep,aviso, sw) VALUES(?,?,?,?,?,?,?,?,?,?)",lista1)
	cursor.execute(" INSERT INTO  jugueteria (codigo,nro_art, descripcion, marca, costo, precio, stk_disp, pnt_rep,aviso, sw) VALUES(?,?,?,?,?,?,?,?,?,?)",lista2)
	cursor.execute(" INSERT INTO  libreria (codigo,nro_art, descripcion, marca, costo, precio, stk_disp, pnt_rep,aviso, sw) VALUES(?,?,?,?,?,?,?,?,?,?)",lista3)
	"""
bbdd.commit()

cursor.close()
bbdd.close()
