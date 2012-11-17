#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sqlite3 as bdapi
import gtk,os

class bajas():

	def press_btn_ok(self,widget,self_padre):
		ruta = os.getcwd()
		valor = str(self_padre.datos_seleccionados[0])
		if valor == '0':
			valor = str(self_padre.datos_seleccionados[1])
			filtro = "nro_art"
		else:
			filtro = "codigo"
		tipo = str(self_padre.datos_seleccionados[8])
		bbdd=bdapi.connect(ruta+'/Base_Datos/stock_rosarino.db')
		cursor=bbdd.cursor()
		bbdd.commit()
		cursor.execute("DELETE FROM "+tipo+" WHERE "+filtro+" = ?",(valor,))
		bbdd.commit()
		cursor.close()
		bbdd.close()
		if tipo == "bazar":
			self_padre.liststore_bazar.remove(self_padre.datos_seleccionados[9])
		elif tipo == "libreria":
			self_padre.liststore_libreria.remove(self_padre.datos_seleccionados[9])
		else:
			self_padre.liststore_jugueteria.remove(self_padre.datos_seleccionados[9])
		self_padre.window.set_sensitive(True)
		self_padre.btn_eliminar.set_sensitive(False)
		self_padre.btn_modificar.set_sensitive(False)
		self.window.destroy()

	def press_btn_no(self,widget,window):
		window.set_sensitive(True)
		self.window.destroy()

	def delete_event(self,widget,event,window):
		window.set_sensitive(True)
		self.window.destroy()

	def __init__(self,self_padre):
		self_padre.window.set_sensitive(False)
		self.archivo_glade = "./bajas/ventana_bajas.glade"
		self.glade = gtk.Builder()
		self.glade.add_from_file(self.archivo_glade)
		self.window = self.glade.get_object("window_bajas")
		self.entry_codigo = self.glade.get_object("entry_codigo")
		self.entry_nro_art = self.glade.get_object("entry_nro_art")
		self.entry_descripcion = self.glade.get_object("entry_descripcion")
		self.entry_marca = self.glade.get_object("entry_marca")
		self.entry_precio = self.glade.get_object("entry_precio")
		self.btn_ok = self.glade.get_object("button_ok")
		self.btn_no = self.glade.get_object("button_no")
		self.btn_ok.connect("clicked",self.press_btn_ok,self_padre,)
		self.btn_no.connect("clicked",self.press_btn_no,self_padre.window)
		self.window.connect("delete-event",self.delete_event,self_padre.window)
		self.entry_codigo.set_text(str(self_padre.datos_seleccionados[0]))
		self.entry_nro_art.set_text(str(self_padre.datos_seleccionados[1]))
		self.entry_descripcion.set_text(self_padre.datos_seleccionados[2])
		self.entry_marca.set_text(self_padre.datos_seleccionados[3])
		self.entry_precio.set_text(str(self_padre.datos_seleccionados[5]))
