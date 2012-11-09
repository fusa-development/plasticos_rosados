#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sqlite3 as bdapi
import gtk,os

from validaciones.validacion import caracteres_validos
from validaciones.validacion import codigo_no_repetido
from validaciones.validacion import articulo_no_repetido
from validaciones.validacion import es_int
from validaciones.validacion import es_float
from altas.agregar_marca import nueva_marca

from altas.question import question

class altas():

	def cargar_lista(self):
		self.liststore_marca.clear()
		ruta = os.getcwd()
		bbdd=bdapi.connect(ruta+'/Base_Datos/marcas_rosarinas.db')
		rubro = [self.combobox.get_active_text().lower()]
		cursor=bbdd.cursor()
		cursor.execute("SELECT * FROM marca WHERE rubro =?",rubro)
		for tupla in cursor.fetchall():
			self.liststore_marca.append([tupla[1]])
		cursor.close()
		bbdd.close()

	def verificar_marca(self,marca):
		esta=False
		model = self.combobox.get_model()
		index = self.combobox.get_active()
		rubro=model[index][0]
		ruta = os.getcwd()
		bbdd=bdapi.connect(ruta+'/Base_Datos/marcas_rosarinas.db')
		cursor=bbdd.cursor()
		cursor.execute("SELECT * FROM marca")
		for tupla in cursor.fetchall():
			if tupla[1] == marca and tupla[3] == rubro.lower():
				esta=True
		cursor.close()
		bbdd.close()
		return esta

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
		
	def aceptar(self,widget,self_padre):
		rubro = self.combobox.get_active_text()
		rubro = rubro.lower()
		codigo=self.entry_codigo.get_text()
		if codigo == "":
			codigo=0
		try:
			nro_art=int ( self.entry_nro_art.get_text() )
		except ValueError:
			nro_art=0
		descripcion=self.entry_descripcion.get_text()
		marca=self.entry_marca.get_text()
		costo= float(self.entry_costo.get_text() )
		if self.verificar_marca(marca):
			ganancia=self.ganancia_marca(marca)
			precio= costo*( 1+ganancia/100)
			ruta = os.getcwd()
			bbdd=bdapi.connect(ruta+'/Base_Datos/stock_rosarino.db')
			cursor=bbdd.cursor()
			if rubro == "libreria":
				precio= round(costo*( 1+ganancia/100),1)
				cursor.execute(" INSERT INTO libreria (codigo,nro_art,descripcion,marca,costo,precio,stk_disp,pnt_rep,aviso,sw) VALUES(?,?,?,?,?,?,?,?,?,?)",(codigo,nro_art,descripcion,marca,costo,precio,0,0,False,True ) )
			else:
				precio= round(costo*( 1+ganancia/100) )
				cursor.execute(" INSERT INTO "+rubro+" (codigo,nro_art,descripcion,marca,costo,precio,stk_disp,pnt_rep,aviso,sw) VALUES(?,?,?,?,?,?,?,?,?,?)",(codigo,nro_art,descripcion,marca,costo,precio,0,0,False,True ) )
			bbdd.commit()
			cursor.close()
			bbdd.close()
			self.liststore_elejido.append( [int(codigo),nro_art,descripcion,marca,costo,precio,0,0,False] )
			question(self,self_padre)
		else:
			nueva_marca(self,self_padre)

	def validar_codigo(self,widget):
		self.codigo_ok=False
		codigo=self.entry_codigo.get_text()
		if es_int(codigo):
			if not codigo_no_repetido(self.liststore_elejido,self.entry_codigo):
				self.entry_codigo.set_icon_from_stock(1,gtk.STOCK_APPLY)
				self.entry_codigo.set_property("secondary-icon-tooltip-text","")
				self.codigo_ok=True
			else:
				self.entry_codigo.set_property("secondary-icon-tooltip-text","Codigo Repetido")
				self.entry_codigo.set_icon_from_stock(1,gtk.STOCK_DIALOG_ERROR)
		else:
			self.entry_codigo.set_property("secondary-icon-tooltip-text","Incorrecto")
			self.entry_codigo.set_icon_from_stock(1,gtk.STOCK_DIALOG_ERROR)
		if codigo == "":
			self.entry_codigo.set_property("secondary-icon-stock",None)

	def validar_nro_art(self,widget):
		self.nro_art_ok=False
		nro_art=self.entry_nro_art.get_text()
		marca = self.entry_marca.get_text()
		rubro = self.combobox.get_active_text()
		if es_int(nro_art):
			if articulo_no_repetido(rubro,nro_art,marca):
				self.entry_nro_art.set_icon_from_stock(1,gtk.STOCK_APPLY)
				self.entry_nro_art.set_property("secondary-icon-tooltip-text","")
				self.nro_art_ok=True
			else:
				self.entry_nro_art.set_icon_from_stock(1,gtk.STOCK_DIALOG_ERROR)
				self.entry_nro_art.set_property("secondary-icon-tooltip-text","Articulo Repetido")
		else:
			self.entry_nro_art.set_icon_from_stock(1,gtk.STOCK_DIALOG_ERROR)
			self.entry_nro_art.set_property("secondary-icon-tooltip-text","Incorrecto")
		if nro_art =="":
			self.entry_nro_art.set_property("secondary-icon-stock",None)

	def validar_descripcion(self,widget):
		self.descripcion_ok=False
		descripcion=self.entry_descripcion.get_text()
		if caracteres_validos(descripcion) and descripcion != "":
			self.entry_descripcion.set_icon_from_stock(1,gtk.STOCK_APPLY)
			self.entry_descripcion.set_property("secondary-icon-tooltip-text","")
			self.descripcion_ok=True
		else:
			self.entry_descripcion.set_icon_from_stock(1,gtk.STOCK_DIALOG_ERROR)
			self.entry_descripcion.set_property("secondary-icon-tooltip-text","Incorrecto")

	def validar_marca(self,widget):
		self.marca_ok=False
		marca=self.entry_marca.get_text()
		if caracteres_validos(marca) and marca != "":
			self.entry_marca.set_icon_from_stock(1,gtk.STOCK_APPLY)
			self.entry_marca.set_property("secondary-icon-tooltip-text","")
			self.marca_ok=True
		else:
			self.entry_nro_art.set_property("secondary-icon-stock",None)
			self.entry_nro_art.set_text("")
			self.entry_marca.set_icon_from_stock(1,gtk.STOCK_DIALOG_ERROR)
			self.entry_marca.set_property("secondary-icon-tooltip-text","Incorrecto")

	def validar_costo(self,widget):
		self.costo_ok=False
		costo=self.entry_costo.get_text()
		if es_float(costo):
			self.entry_costo.set_icon_from_stock(1,gtk.STOCK_APPLY)
			self.entry_costo.set_property("secondary-icon-tooltip-text","")
			self.costo_ok=True
		else:
			self.entry_costo.set_icon_from_stock(1,gtk.STOCK_DIALOG_ERROR)
			self.entry_costo.set_property("secondary-icon-tooltip-text","Incorrecto")
		if costo == "":
		 self.entry_costo.set_property("secondary-icon-stock",None)

	def desbloquear_aceptar(self,widget):
		self.btn_ok.set_sensitive(False)
		if self.marca_ok and self.descripcion_ok and self.costo_ok:
			#1 bien y la otra vacia o las 2 bien
			if ( ( self.codigo_ok and self.entry_nro_art.get_text() == "" ) or ( self.entry_codigo.get_text() =="" and self.nro_art_ok ) ) or ( self.codigo_ok and self.nro_art_ok ):
				self.btn_ok.set_sensitive(True)

	def aceptar_with_enter(self,widget,event,self_padre):
		if event.keyval ==gtk.keysyms.Return:
			if self.marca_ok and self.descripcion_ok and self.costo_ok:
			#1 bien y la otra vacia o las 2 bien
				if ( ( self.codigo_ok and self.entry_nro_art.get_text() == "" ) or ( self.entry_codigo.get_text() =="" and self.nro_art_ok ) ) or ( self.codigo_ok and self.nro_art_ok ):
					self.aceptar(None,self_padre)

	def elejir_rubro(self,widget,self_padre):
		self.cargar_lista()
		self.habilitar_entrys()
		model = self.combobox.get_model()
		index = self.combobox.get_active()
		self.entry_codigo.set_text("")
		self.entry_nro_art.set_text("")
		self.entry_descripcion.set_text("")
		self.entry_marca.set_text("")
		self.entry_costo.set_text("")
		self.entry_codigo.set_property("secondary-icon-stock",None)
		self.entry_nro_art.set_property("secondary-icon-stock",None)
		self.entry_descripcion.set_property("secondary-icon-stock",None)
		self.entry_marca.set_property("secondary-icon-stock",None)
		self.entry_costo.set_property("secondary-icon-stock",None)
		if model[index][0] =="Bazar":
			self.liststore_elejido=self_padre.liststore_bazar
		if model[index][0] =="Jugueteria":
			self.liststore_elejido=self_padre.liststore_jugueteria
		if model[index][0] =="Libreria":
			self.liststore_elejido=self_padre.liststore_libreria
		self.entry_marca.set_property("is-focus",1)

	def habilitar_entrys(self):
		self.entry_codigo.set_sensitive(True)
		self.entry_nro_art.set_sensitive(True)
		self.entry_descripcion.set_sensitive(True)
		self.entry_marca.set_sensitive(True)
		self.entry_costo.set_sensitive(True)

	def primero_marca(self,widget,event):
		if not self.marca_ok:
			self.entry_nro_art.set_text("Ingrese Marca")
			self.entry_nro_art.set_property("editable",0)
			self.entry_nro_art.set_property("secondary-icon-stock",None)

	def salio_de_art(self,widget,event):
		if not self.marca_ok:
			self.entry_nro_art.set_text("")
			self.entry_nro_art.set_property("editable",1)

	def delete_event(self,widget,event,window):
		window.set_sensitive(True)
		self.window.destroy()

	def cerrar(self,widget,window):
		window.set_sensitive(True)
		self.window.destroy()

	def __init__(self,self_padre):
		self_padre.window.set_sensitive(False)
		self.archivo_glade = "./altas/ventana_altas.glade"
		self.glade = gtk.Builder()
		self.glade.add_from_file(self.archivo_glade)

		self.window = self.glade.get_object("window")
		self.entry_codigo = self.glade.get_object("entry_codigo")
		self.entry_nro_art = self.glade.get_object("entry_nro_art")
		self.entry_descripcion = self.glade.get_object("entry_descripcion")
		self.entry_marca = self.glade.get_object("entry_marca")
		self.entry_costo = self.glade.get_object("entry_costo")
		self.liststore_marca = self.glade.get_object("liststore_marca")
		self.table=self.glade.get_object("table1")

		self.completion = gtk.EntryCompletion()
		self.completion.set_model(self.liststore_marca)
		self.entry_marca.set_completion(self.completion)
		self.btn_ok = self.glade.get_object("button_ok")
		self.btn_no = self.glade.get_object("button_no")
		self.completion.set_text_column(0)

		self.combobox = gtk.combo_box_new_text()
		self.table.attach(self.combobox,1,2,0,1)
		self.combobox.append_text("Bazar")
		self.combobox.append_text("Jugueteria")
		self.combobox.append_text("Libreria")

		self.codigo_ok,self.nro_art_ok,self.marca_ok,self.descripcion_ok,self.costo_ok=False,False,False,False,False

		self.btn_ok.connect("clicked",self.aceptar,self_padre)
		self.window.connect("key-press-event",self.aceptar_with_enter,self_padre)
		self.btn_no.connect("clicked",self.cerrar,self_padre.window)
		self.window.connect("delete-event",self.delete_event,self_padre.window)

		self.entry_nro_art.connect("focus-in-event",self.primero_marca)
		self.entry_nro_art.connect("focus-out-event",self.salio_de_art)

		self.combobox.connect("changed",self.elejir_rubro,self_padre)
		self.entry_codigo.connect("changed",self.validar_codigo)
		self.entry_nro_art.connect("changed",self.validar_nro_art)
		self.entry_marca.connect("changed",self.validar_marca)
		self.entry_descripcion.connect("changed",self.validar_descripcion)
		self.entry_costo.connect("changed",self.validar_costo)

		self.entry_codigo.connect("changed",self.desbloquear_aceptar)
		self.entry_nro_art.connect("changed",self.desbloquear_aceptar)
		self.entry_marca.connect("changed",self.desbloquear_aceptar)
		self.entry_descripcion.connect("changed",self.desbloquear_aceptar)
		self.entry_costo.connect("changed",self.desbloquear_aceptar)

		self.combobox.show()
