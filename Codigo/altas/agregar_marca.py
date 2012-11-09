#!/usr/bin/env python
# -*- coding: utf-8 -*-
import gtk,os

from validaciones.validacion import caracteres_validos
from validaciones.validacion import es_float
from altas.question import question

import sqlite3 as bdapi

class nueva_marca:

	def ganancia_marca(self,marca):
		ruta = os.getcwd()
		bbdd=bdapi.connect(ruta+'/Base_Datos/marcas_rosarinas.db')
		cursor=bbdd.cursor()
		cursor.execute("SELECT * FROM marca")
		for tupla in cursor.fetchall():
			if tupla[1] == marca:
				ganancia = tupla[4]
		cursor.close()
		bbdd.close()
		return ganancia

	def agregar_producto(self,self_altas):
		model = self_altas.combobox.get_model()
		index = self_altas.combobox.get_active()
		tabla=model[index][0]
		codigo=self_altas.entry_codigo.get_text()
		if codigo == "":
			codigo=0
		try:
			nro_art=int ( self_altas.entry_nro_art.get_text() )
		except ValueError:
			nro_art=0
		descripcion=self_altas.entry_descripcion.get_text()
		marca=self_altas.entry_marca.get_text()
		costo=float (self_altas.entry_costo.get_text() )
		ganancia=self.ganancia_marca(marca)
		precio= costo*( 1+ganancia/100)
		ruta = os.getcwd()
		bbdd=bdapi.connect(ruta+'/Base_Datos/stock_rosarino.db')
		cursor=bbdd.cursor()
		cursor.execute(" INSERT INTO "+tabla.lower()+" (codigo,nro_art,descripcion,marca,costo,precio,stk_disp,pnt_rep,aviso,sw) VALUES(?,?,?,?,?,?,?,?,?,?)",(codigo,nro_art,descripcion,marca,costo,precio,0,0,False,True ) )
		bbdd.commit()
		cursor.close()
		bbdd.close()
		self_altas.liststore_elejido.append( [int(codigo),nro_art,descripcion,marca,costo,precio,0,0,False] )


	def add_marca(self,widget,self_altas,self_padre):
		rubro=self.entry_rubro.get_text().lower()
		descripcion=self.entry_descripcion.get_text()
		marca=self.entry_marca.get_text()
		ganancia=float(self.entry_ganancia.get_text() )
		ruta = os.getcwd()
		bbdd=bdapi.connect(ruta+'/Base_Datos/marcas_rosarinas.db')
		cursor=bbdd.cursor()
		cursor.execute(" INSERT INTO marca (nombre,descripcion,rubro,coeficiente) VALUES(?,?,?,?)",(marca,descripcion,rubro,ganancia ) )
		bbdd.commit()
		cursor.close()
		bbdd.close()
		self_altas.window.set_sensitive(True)
		self.window.destroy()

		self.agregar_producto(self_altas)

		question(self_altas,self_padre)

	def aceptar_with_enter(self,widget,event,self_altas,self_padre):
		if event.keyval ==gtk.keysyms.Return:
			self.add_marca(None,self_altas,self_padre)

	def validar_descripcion(self,widget):
		self.descripcion_ok=False
		descripcion=self.entry_descripcion.get_text()
		if caracteres_validos(descripcion) and descripcion != "":
			self.entry_descripcion.set_icon_from_stock(1,gtk.STOCK_APPLY)
			self.descripcion_ok=True
		else:
			self.entry_descripcion.set_icon_from_stock(1,gtk.STOCK_DIALOG_ERROR)

	def validar_marca(self,widget):
		self.marca_ok=False
		marca=self.entry_marca.get_text()
		if caracteres_validos(marca) and marca != "":
			self.entry_marca.set_icon_from_stock(1,gtk.STOCK_APPLY)
			self.marca_ok=True
		else:
			self.entry_marca.set_icon_from_stock(1,gtk.STOCK_DIALOG_ERROR)

	def validar_ganancia(self,widget):
		self.ganancia_ok=False
		ganancia=self.entry_ganancia.get_text()
		if es_float(ganancia):
			self.entry_ganancia.set_icon_from_stock(1,gtk.STOCK_APPLY)
			self.ganancia_ok=True
		else:
			self.entry_ganancia.set_icon_from_stock(1,gtk.STOCK_DIALOG_ERROR)
		if ganancia == "":
		 self.entry_ganancia.set_property("secondary-icon-stock",None)

	def desbloquear_aceptar(self,widget):
		self.btn_ok.set_sensitive(False)
		if self.marca_ok and self.descripcion_ok and self.ganancia_ok:
			self.btn_ok.set_sensitive(True)

	def cancelar(self,widget,self_altas):
		self_altas.window.set_sensitive(True)
		self.window.destroy()

	def delete_event(self,widget,event,self_altas):
		self_altas.window.set_sensitive(True)
		self.window.destroy()

	def __init__(self,self_altas,self_padre):
		self_altas.window.set_sensitive(False)
		self.archivo="./altas/agregar_marca.glade"
		self.glade=gtk.Builder()
		self.glade.add_from_file(self.archivo)

		self.window = self.glade.get_object("dialog1")
		self.btn_ok = self.glade.get_object("button_ok")
		self.button_no = self.glade.get_object("button_no")
		self.entry_descripcion = self.glade.get_object("entry_descripcion")
		self.entry_marca = self.glade.get_object("entry_marca")
		self.entry_ganancia = self.glade.get_object("entry_ganancia")
		self.entry_rubro=self.glade.get_object("entry_rubro")

		self.entry_marca.set_text( self_altas.entry_marca.get_text() )
		model = self_altas.combobox.get_model()
		index = self_altas.combobox.get_active()
		rubro=str(model[index][0])
		self.entry_rubro.set_text(rubro)
		self.marca_ok,self.descripcion_ok,self.ganancia_ok=True,False,False

		self.window.connect("delete-event",self.delete_event,self_altas)

		self.entry_marca.connect("changed",self.validar_marca)
		self.entry_descripcion.connect("changed",self.validar_descripcion)
		self.entry_ganancia.connect("changed",self.validar_ganancia)

		self.entry_marca.connect("changed",self.desbloquear_aceptar)
		self.entry_descripcion.connect("changed",self.desbloquear_aceptar)
		self.entry_ganancia.connect("changed",self.desbloquear_aceptar)

		self.btn_ok.connect("clicked",self.add_marca,self_altas,self_padre)
		self.button_no.connect("clicked",self.cancelar,self_altas)

		self.window.connect("key-press-event",self.aceptar_with_enter,self_altas,self_padre)
