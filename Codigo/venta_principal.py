#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3 as bdapi
import gtk

from actualizaciones.actualizar import actualizaciones
from altas.agregar import altas
from bajas.eliminar import bajas
from control.controlar import control
from modificaciones.modificar import modificaciones
from Backup.backup_BBDD import backup
from altas.agregar_marca_en_main import nueva_marca

class principal() :

	def abrir_recordatorios(self):
		archivo=open("recordatorios.txt","r")
		linea=archivo.read()
		self.textbuffer.set_text(str(linea))
		archivo.close()

	def guardar_recordatorios(self):
		archivo=open("recordatorios.txt","w")
		start,end=self.textbuffer.get_bounds()
		texto=self.textbuffer.get_text(start,end)
		archivo.write(texto)
		archivo.close()

	def conectar_bd(self):
		bbdd=bdapi.connect('./Base_Datos/stock_rosarino.db')
		cursor=bbdd.cursor()
		cursor.execute("SELECT * FROM bazar")
		self.liststore_bazar.clear()
		for tupla in cursor.fetchall():
			if tupla[10]:
				self.liststore_bazar.append([int(tupla[1]),tupla[2],tupla[3],tupla[4],tupla[5],tupla[6],tupla[7],tupla[8],tupla[9]])
			else:
				self.liststore_bazar.append([int(tupla[1]),tupla[2],tupla[3],tupla[4],tupla[5],tupla[6],tupla[7],tupla[8],False])
		cursor.execute("SELECT * FROM jugueteria")
		self.liststore_jugueteria.clear()
		for tupla in cursor.fetchall():
			if tupla[10]:
				self.liststore_jugueteria.append([int(tupla[1]),tupla[2],tupla[3],tupla[4],tupla[5],tupla[6],tupla[7],tupla[8],tupla[9]])
			else:
				self.liststore_jugueteria.append([int(tupla[1]),tupla[2],tupla[3],tupla[4],tupla[5],tupla[6],tupla[7],tupla[8],False])
		cursor.execute("SELECT * FROM libreria")
		self.liststore_libreria.clear()
		for tupla in cursor.fetchall():
			if tupla[10]:
				self.liststore_libreria.append([int(tupla[1]),tupla[2],tupla[3],tupla[4],tupla[5],tupla[6],tupla[7],tupla[8],True])
			else:
				self.liststore_libreria.append([int(tupla[1]),tupla[2],tupla[3],tupla[4],tupla[5],tupla[6],tupla[7],tupla[8],False])
		bbdd.commit()
		cursor.close()
		bbdd.close()

	def buscar_bazar(self,widget):
		busca=self.entry_buscar_bazar.get_text()
		filtrado_por= self.combo_buscar_bazar.get_active_text()
		filtrado_por = filtrado_por.replace(" ","_")
		self.liststore_bazar.clear()
		bbdd=bdapi.connect('./Base_Datos/stock_rosarino.db')
		cursor=bbdd.cursor()
		if busca != "":
			cursor.execute("SELECT * FROM bazar WHERE "+filtrado_por.lower()+" LIKE '%"+busca+"%'")
			for tupla in cursor.fetchall():
				self.liststore_bazar.append([int(tupla[1]),tupla[2],tupla[3],tupla[4],tupla[5],tupla[6],tupla[7],tupla[8],tupla[9]])
		else:
			cursor.execute(""" SELECT * FROM bazar """)
			for tupla in cursor.fetchall():
				self.liststore_bazar.append([int(tupla[1]),tupla[2],tupla[3],tupla[4],tupla[5],tupla[6],tupla[7],tupla[8],tupla[9]])
		bbdd.commit()
		cursor.close()
		bbdd.close()

	def buscar_jugueteria(self,widget):
		busca=self.entry_buscar_jugueteria.get_text()
		filtrado_por=self.combo_buscar_jugueteria.get_active_text()
		filtrado_por = filtrado_por.replace(" ","_")
		self.liststore_jugueteria.clear()
		bbdd=bdapi.connect('./Base_Datos/stock_rosarino.db')
		cursor=bbdd.cursor()
		if busca != "":
			cursor.execute("SELECT * FROM jugueteria WHERE "+filtrado_por.lower()+" LIKE '%"+busca+"%'")
			for tupla in cursor.fetchall():
				self.liststore_jugueteria.append([int(tupla[1]),tupla[2],tupla[3],tupla[4],tupla[5],tupla[6],tupla[7],tupla[8],tupla[9]])
		else:
			cursor.execute(""" SELECT * FROM jugueteria """)
			for tupla in cursor.fetchall():
				self.liststore_jugueteria.append([int(tupla[1]),tupla[2],tupla[3],tupla[4],tupla[5],tupla[6],tupla[7],tupla[8],tupla[9]])
		bbdd.commit()
		cursor.close()
		bbdd.close()

	def buscar_libreria(self,widget):
		busca=self.entry_buscar_libreria.get_text()
		filtrado_por=self.combo_buscar_libreria.get_active_text()
		filtrado_por = filtrado_por.replace(" ","_")
		self.liststore_libreria.clear()
		bbdd=bdapi.connect('./Base_Datos/stock_rosarino.db')
		cursor=bbdd.cursor()
		if busca != "":
			cursor.execute("SELECT * FROM libreria WHERE "+filtrado_por.lower()+" LIKE '%"+busca+"%'")
			for tupla in cursor.fetchall():
				self.liststore_libreria.append([int(tupla[1]),tupla[2],tupla[3],tupla[4],tupla[5],tupla[6],tupla[7],tupla[8],tupla[9]])
		else:
			cursor.execute(""" SELECT * FROM libreria """)
			for tupla in cursor.fetchall():
				self.liststore_libreria.append([int(tupla[1]),tupla[2],tupla[3],tupla[4],tupla[5],tupla[6],tupla[7],tupla[8],tupla[9]])
		bbdd.commit()
		cursor.close()
		bbdd.close()

	def bloquear_botones(self):
		self.btn_eliminar.set_sensitive(False)
		self.btn_modificar.set_sensitive(False)

	def need_backup(self,widget):
		backup(self)

	def call_class_actualizaciones(self,widget):
		actualizaciones(self)

	def call_class_altas(self,widget):
		altas(self)

	def call_class_bajas(self,widget):
		bajas(self)
		self.bloquear_botones()

	def call_class_control(self,widget):
		control(self)

	def call_class_modificaciones(self,widget):
		modificaciones(self)
		self.bloquear_botones()

	def new_marca(self,widget):
		nueva_marca(self)

	def desbloquear_botones(self):
		self.btn_modificar.set_sensitive(True)
		self.btn_eliminar.set_sensitive(True)

	def target_bazar(self,widget):
		(model, iter) = self.treeselection_bazar.get_selected()
		if self.datos_seleccionados != []:
			self.datos_seleccionados=[]
		try:
			for x in range(8):
				self.datos_seleccionados.append(self.liststore_bazar.get_value(iter,x))
			self.datos_seleccionados.append("bazar")
			self.datos_seleccionados.append(iter)
			self.desbloquear_botones()
		except:
			pass

	def target_jugueteria(self,widget):
		(model, iter) = self.treeselection_jugueteria.get_selected()
		if self.datos_seleccionados != []:
			self.datos_seleccionados=[]
		try:
			for x in range(8):
				self.datos_seleccionados.append(self.liststore_jugueteria.get_value(iter,x))
			self.datos_seleccionados.append("jugueteria")
			self.datos_seleccionados.append(iter)
			self.desbloquear_botones()
		except:
			pass

	def target_libreria(self,widget):
		(model, iter) = self.treeselection_libreria.get_selected()
		if self.datos_seleccionados != []:
			self.datos_seleccionados=[]
		try:
			for x in range(8):
				self.datos_seleccionados.append(self.liststore_libreria.get_value(iter,x))
			self.datos_seleccionados.append("libreria")
			self.datos_seleccionados.append(iter)
			self.desbloquear_botones()
		except:
			pass

	def teclas(self,widget,event):
		if event.keyval ==gtk.keysyms.F1:
			self.go_home(None)
		if event.keyval ==gtk.keysyms.F2:
			self.go_stock(None)

	def go_home(self,widget):
		self.notebook.set_current_page(0)
		self.window.set_title("Ventana Principal")

	def go_stock(self,widget):
		self.notebook.set_current_page(1)
		self.window.set_title("Gestion de Productos")

	def cerrar(self,widget):
		self.guardar_recordatorios()
		gtk.main_quit()

	def delete_event(self,widget,event):
		self.guardar_recordatorios()
		gtk.main_quit()

	def __init__(self):
		self.datos_seleccionados = []
		self.archivo_glade="./ventana_principal.glade"
		self.glade=gtk.Builder()
		self.glade.add_from_file(self.archivo_glade)
		self.window = self.glade.get_object("window_main")
		self.notebook = self.glade.get_object("notebook_principal")

		self.textview_recordatorio=self.glade.get_object("textview_recordatorios")
		self.textbuffer = self.textview_recordatorio.get_buffer()

####################################BOTONES################################
		self.btn_actualizar = self.glade.get_object("actualizar_producto")
		self.btn_agregar = self.glade.get_object("agregar_producto")
		self.btn_eliminar = self.glade.get_object("eliminar_producto")
		self.btn_controlar = self.glade.get_object("controlar_producto")
		self.btn_modificar = self.glade.get_object("modificar_producto")
		self.button_home = self.glade.get_object("button_home")
		self.button_stock = self.glade.get_object("button_stock")
		self.button_backup = self.glade.get_object("button_backup")
		self.button_agregar_marca = self.glade.get_object("agregar_marca")
		self.button_salir = self.glade.get_object("button_salir")
#################################ENTRYS Y COMBO Bself.guardar_recordatorios()OX DE BUSQUEDA####################################
		self.entry_buscar_bazar = self.glade.get_object("entry_buscar_bazar")
		self.entry_buscar_jugueteria = self.glade.get_object("entry_buscar_jugueteria")
		self.entry_buscar_libreria = self.glade.get_object("entry_buscar_libreria")
		self.hbox_buscar_bazar = self.glade.get_object("hbox3")
		self.hbox_buscar_jugueteria = self.glade.get_object("hbox6")
		self.hbox_buscar_libreria = self.glade.get_object("hbox7")
		filtrado=("Codigo","Nro Art","Descripcion","Marca")
		self.combo_buscar_bazar = gtk.combo_box_new_text()
		self.combo_buscar_jugueteria = gtk.combo_box_new_text()
		self.combo_buscar_libreria = gtk.combo_box_new_text()
		for fil in filtrado:
			self.combo_buscar_bazar.append_text(fil)
			self.combo_buscar_jugueteria.append_text(fil)
			self.combo_buscar_libreria.append_text(fil)
		self.hbox_buscar_bazar.pack_start(self.combo_buscar_bazar,False,True,0)
		self.hbox_buscar_jugueteria.pack_start(self.combo_buscar_jugueteria,False,True,0)
		self.hbox_buscar_libreria.pack_start(self.combo_buscar_libreria,False,True,0)
###########################LISTSTORES-TREEVIEW#############################
		self.treeview_bazar = self.glade.get_object("treeview_bazar")
		self.treeview_jugueteria = self.glade.get_object("treeview_jugueteria")
		self.treeview_libreria = self.glade.get_object("treeview_libreria")
		self.liststore_bazar = self.glade.get_object("liststore_bazar")
		self.liststore_jugueteria = self.glade.get_object("liststore_jugueteria")
		self.liststore_libreria = self.glade.get_object("liststore_libreria")
		self.conectar_bd()
		self.abrir_recordatorios()
############################CONECTANDO SEÑALES#############################
		self.window.connect("key-press-event",self.teclas)
		self.window.connect("delete_event",self.delete_event)
		self.btn_actualizar.connect("clicked",self.call_class_actualizaciones)
		self.btn_agregar.connect("clicked",self.call_class_altas)
		self.btn_eliminar.connect("clicked",self.call_class_bajas)
		self.btn_controlar.connect("clicked",self.call_class_control)
		self.btn_modificar.connect("clicked",self.call_class_modificaciones)
		self.button_agregar_marca.connect("clicked",self.new_marca)
		self.treeview_bazar.connect("cursor-changed",self.target_bazar)
		self.treeview_jugueteria.connect("cursor-changed",self.target_jugueteria)
		self.treeview_libreria.connect("cursor-changed",self.target_libreria)
		self.entry_buscar_bazar.connect("changed",self.buscar_bazar)
		self.entry_buscar_jugueteria.connect("changed",self.buscar_jugueteria)
		self.entry_buscar_libreria.connect("changed",self.buscar_libreria)
		self.button_home.connect("clicked",self.go_home)
		self.button_stock.connect("clicked",self.go_stock)
		self.button_backup.connect("clicked",self.need_backup)
		self.button_salir.connect("clicked",self.cerrar)
############################TREESELECTIOS##################################
		self.treeselection_bazar = self.treeview_bazar.get_selection()
		self.treeselection_jugueteria = self.treeview_jugueteria.get_selection()
		self.treeselection_libreria = self.treeview_libreria.get_selection()
###########################################################################
		self.combo_buscar_bazar.set_active(0)
		self.combo_buscar_bazar.show()
		self.combo_buscar_jugueteria.set_active(0)
		self.combo_buscar_jugueteria.show()
		self.combo_buscar_libreria.set_active(0)
		self.combo_buscar_libreria.show()

	def main(self):
		gtk.main()


if __name__=="__main__":
	program=principal()
	program.main()
