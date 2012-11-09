#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sqlite3 as bdapi
import gtk ,os
from validaciones.validacion import es_int

class actualizaciones():
	
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

	def desbloquear_entrys(self):
		if self.entry_marcas.get_text() != "":
			self.entry_aumento_marca.set_property("is focus",1)
			
	def desbloquear_botones(self,widget):
		if not False in self.pagina1 and not False in self.pagina2:
			self.btn_aceptar.set_sensitive(True)
		
	def focusear_completation(self,widget):
		self.cargar_lista()
		self.entry_marcas.set_sensitive(True)
		self.entry_marcas.set_property("is focus",1)
		
	def limpiar(self):
		pagina_activa = self.notebook.get_current_page()
		if pagina_activa == 1:
			self.entry_codigo.set_text("")
			self.entry_aumento.set_text("")
			self.entry_cantidad.set_text("0")
			self.entry_pnt_rep.set_text("0")
			self.pagina2 = [True,True]
		else:
			self.entry_ganancia.set_text("")
			self.entry_aumento_marca.set_text("")
			self.pagina1 = [True,True]
		self.btn_aceptar.set_sensitive(False)
	
	def cambiar_pagina(self,widget,boton):
		if boton == "marca":
			self.entry_codigo.set_text("")
			self.entry_aumento.set_text("")
			self.entry_cantidad.set_text("0")
			self.entry_pnt_rep.set_text("0")
			self.checkbutton_reponer.set_sensitive(False)
			self.btn_aceptar.set_sensitive(False)
			self.checkbutton_reponer.set_sensitive(False)
			self.entry_aumento_marca.set_icon_from_stock(1,None)
			self.entry_ganancia.set_icon_from_stock(1,None)
			self.entry_marcas.set_icon_from_stock(1,None)
			self.notebook.set_current_page(0)
		else:
			self.entry_ganancia.set_text("")
			self.entry_aumento_marca.set_text("")
			self.btn_aceptar.set_sensitive(False)
			self.entry_codigo.set_icon_from_stock(1,None)
			self.entry_aumento.set_icon_from_stock(1,None)
			self.notebook.set_current_page(1)
		
	def validar_entero(self,widget,event,entry):
		
		if entry == "aumento marca":
			texto = self.entry_aumento_marca.get_text()
			texto2 = self.entry_ganancia.get_text()
			if es_int(texto):
				self.entry_aumento_marca.set_icon_from_stock(1,gtk.STOCK_APPLY)
				self.entry_aumento_marca.set_property("secondary-icon-tooltip-text",None)
				self.pagina1[0] = True
				if not False in self.pagina1 and (texto2 != "" or texto != ""):
					self.btn_aceptar.set_sensitive(True)
				else:
					self.btn_aceptar.set_sensitive(False)
			elif texto == "":
				if not False in self.pagina1 and (texto2 != "" or texto != ""): 
					self.btn_aceptar.set_sensitive(True)
				else:
					self.btn_aceptar.set_sensitive(False)
			else:
				self.entry_aumento_marca.set_icon_from_stock(1,gtk.STOCK_DIALOG_ERROR)
				self.entry_aumento_marca.set_property("secondary-icon-tooltip-text","Solo numeros enteros.")
				self.pagina1[0] = False
				self.btn_aceptar.set_sensitive(False)
		elif entry == "aumento":
			texto = self.entry_aumento.get_text()
			if es_int(texto) or texto == "":
				self.entry_aumento.set_icon_from_stock(1,gtk.STOCK_APPLY)
				self.entry_aumento.set_property("secondary-icon-tooltip-text",None)
				self.pagina2[0] = True
				if not False in self.pagina2:
					self.btn_aceptar.set_sensitive(True)
			else:
				self.entry_aumento.set_icon_from_stock(1,gtk.STOCK_DIALOG_ERROR)
				self.entry_aumento.set_property("secondary-icon-tooltip-text","Solo numeros enteros.")
				self.pagina2[0] = False
				self.btn_aceptar.set_sensitive(False)
		else:
			texto = self.entry_ganancia.get_text()
			if es_int(texto):
				self.entry_ganancia.set_icon_from_stock(1,gtk.STOCK_APPLY)
				self.entry_ganancia.set_property("secondary-icon-tooltip-text",None)
				self.pagina1[1] = True
				texto2 = self.entry_ganancia.get_text()
				if not False in self.pagina1 and (texto2 != "" or texto != ""):
					self.btn_aceptar.set_sensitive(True)
				else:
					self.btn_aceptar.set_sensitive(False)
			elif texto == "":
				if not False in self.pagina1 and (texto2 != "" or texto != ""): 
					self.btn_aceptar.set_sensitive(True)
				else:
					self.btn_aceptar.set_sensitive(False)
			else:
				self.entry_ganancia.set_icon_from_stock(1,gtk.STOCK_DIALOG_ERROR)
				self.entry_ganancia.set_property("secondary-icon-tooltip-text","Solo numeros enteros.")
				self.pagina1[1] = False
				self.btn_aceptar.set_sensitive(False)
				
	def verificar_marca(self,widget,event = None):
		marca = self.entry_marcas.get_text()
		model = self.combobox.get_model()
		index = self.combobox.get_active()
		rubro=model[index][0]
		ruta = os.getcwd()
		bbdd=bdapi.connect(ruta+'/Base_Datos/marcas_rosarinas.db')
		cursor=bbdd.cursor()
		cursor.execute("SELECT * FROM marca WHERE nombre =?",(marca,))
		tupla = cursor.fetchone()
		if tupla != None:
			if tupla[1] == marca and tupla[3] == rubro.lower():
				self.entry_marcas.set_icon_from_stock(1,gtk.STOCK_APPLY)
				self.entry_marcas.set_property("secondary-icon-tooltip-text",None)
				self.notebook.set_sensitive(True)
				self.desbloquear_entrys()
		else:
			self.entry_marcas.set_icon_from_stock(1,gtk.STOCK_DIALOG_ERROR)
			self.entry_marcas.set_property("secondary-icon-tooltip-text","Marca Inexistente")
			self.notebook.set_sensitive(False)
			self.limpiar()
		cursor.close()
		bbdd.close()
		
	def validar_codigo(self,widget,event = None):
		ruta = os.getcwd()
		codigo = self.entry_codigo.get_text()
		rubro = self.combobox.get_active_text()
		marca = self.entry_marcas.get_text()
		filtro = self.combobox_producto.get_active_text()
		filtro = filtro.replace(" ","_")
		bbdd=bdapi.connect(ruta+'/Base_Datos/stock_rosarino.db')
		cursor=bbdd.cursor()
		cursor.execute("SELECT * FROM "+rubro+" WHERE "+filtro+"=? AND marca=?",(codigo,marca))
		self.tupla = cursor.fetchall()
		if self.tupla != []:
			cursor.close()
			bbdd.close()
			self.entry_aumento.set_sensitive(True)
			self.entry_cantidad.set_sensitive(True)
			self.entry_pnt_rep.set_sensitive(True)
			self.checkbutton_reponer.set_sensitive(True)
			self.entry_codigo.set_icon_from_stock(1,gtk.STOCK_APPLY)
			self.entry_codigo.set_property("secondary-icon-tooltip-text","")
			if self.tupla[0][10]:
				self.checkbutton_reponer.set_active(1)
			else:
				self.checkbutton_reponer.set_active(0)
			self.tupla.append(rubro)
			self.entry_aumento.set_property("is-focus",1)
			self.pagina2[1] = True
			return self.tupla
		else:
			cursor.close()
			bbdd.close()
			self.entry_codigo.set_property("secondary-icon-tooltip-text","Codigo Inexistente")
			self.entry_codigo.set_icon_from_stock(1,gtk.STOCK_DIALOG_ERROR)
			self.pagina2[1] = False
			self.btn_aceptar.set_sensitive(False)
			return None
	
	def recargar_listas(self,self_padre,rubro,cursor):
		if rubro == "bazar":
			cursor.execute("SELECT * FROM bazar")
			self_padre.liststore_bazar.clear()
			for tupla in cursor.fetchall():
				self_padre.liststore_bazar.append([int(tupla[1]),tupla[2],tupla[3],tupla[4],tupla[5],tupla[6],tupla[7],tupla[8],tupla[9]])
		elif rubro == "jugueteria":
			cursor.execute("SELECT * FROM jugueteria")
			self_padre.liststore_jugueteria.clear()
			for tupla in cursor.fetchall():
				self_padre.liststore_jugueteria.append([int(tupla[1]),tupla[2],tupla[3],tupla[4],tupla[5],tupla[6],tupla[7],tupla[8],tupla[9]])
		else:
			cursor.execute("SELECT * FROM libreria")
			self_padre.liststore_libreria.clear()
			for tupla in cursor.fetchall():
				self_padre.liststore_libreria.append([int(tupla[1]),tupla[2],tupla[3],tupla[4],tupla[5],tupla[6],tupla[7],tupla[8],tupla[9]])
		
	def cambios_marca(self,self_padre):
		ruta = os.getcwd()
		self.values = []
		rubro = [self.combobox.get_active_text().lower()]
		self.values.append(self.entry_aumento_marca.get_text())
		self.values.append(self.entry_ganancia.get_text())
		self.values.append(self.entry_marcas.get_text())
		if self.values[0] == "" and self.values[1] != "":
			bbdd=bdapi.connect(ruta+'/Base_Datos/marcas_rosarinas.db')
			cursor=bbdd.cursor()
			cursor.execute("UPDATE marca SET coeficiente =? WHERE nombre =?",(self.values[1],self.values[2]))
			bbdd.commit()
			bbdd=bdapi.connect(ruta+'/Base_Datos/stock_rosarino.db')
			cursor=bbdd.cursor()
			cursor.execute("SELECT costo,codigo,nro_art FROM "+rubro[0]+" WHERE marca = ?",[self.values[2]])
			for tupla in cursor.fetchall():
				print tupla
				precio = tupla[0]*(1+float(self.values[1])/100)
				if precio <= 20:
					precio = round(precio,1)
					if tupla[1] == "0":
						cursor.execute("UPDATE "+rubro[0]+" SET precio =? WHERE nro_art =?",(precio,tupla[2]))
					else:
						cursor.execute("UPDATE "+rubro[0]+" SET precio =? WHERE codigo =?",(precio,tupla[1]))
				else:
					precio = round(precio)
					if tupla[1] == "0":
						cursor.execute("UPDATE "+rubro[0]+" SET precio =? WHERE nro_art =?",(precio,tupla[2]))
					else:
						cursor.execute("UPDATE "+rubro[0]+" SET precio =? WHERE codigo =?",(precio,tupla[1]))
			bbdd.commit()
			self.recargar_listas(self_padre,rubro[0],cursor)
		elif self.values[0] != "" and self.values[1] == "" :
			ruta = os.getcwd()
			bbdd=bdapi.connect(ruta+'/Base_Datos/marcas_rosarinas.db')
			cursor=bbdd.cursor()
			cursor.execute("SELECT coeficiente FROM marca WHERE nombre =?",(self.values[2],))
			ganancia = cursor.fetchone()
			cursor.close()
			bbdd.close()
			bbdd=bdapi.connect(ruta+'/Base_Datos/stock_rosarino.db')
			cursor=bbdd.cursor()
			cursor.execute("SELECT costo,codigo FROM "+rubro[0]+" WHERE marca = ?",(self.values[2],))
			if rubro[0] == "libreria":
				for tupla in cursor.fetchall():
					costo = round(tupla[0]*(1+float(self.values[0])/100),1)
					precio = round(costo*(1+ganancia[0]/100),1)
					cursor.execute("UPDATE "+rubro[0]+" SET costo =?, precio =? WHERE codigo =?",(costo,precio,tupla[1]))
			else:
				for tupla in cursor.fetchall():
					costo = round(tupla[0]*(1+float(self.values[0])/100))
					precio = round(costo*(1+ganancia[0]/100))
					cursor.execute("UPDATE "+rubro[0]+" SET costo =?, precio =? WHERE codigo =?",(costo,precio,tupla[1]))
			bbdd.commit()
			self.recargar_listas(self_padre,rubro[0],cursor)
		else:
			bbdd=bdapi.connect(ruta+'/Base_Datos/marcas_rosarinas.db')
			cursor=bbdd.cursor()
			cursor.execute("UPDATE marca SET coeficiente =? WHERE nombre =?",(self.values[1],self.values[2]))
			bbdd.commit()
			cursor.close()
			bbdd.close()
			bbdd=bdapi.connect(ruta+'/Base_Datos/stock_rosarino.db')
			cursor=bbdd.cursor()
			cursor.execute("SELECT costo,codigo FROM "+rubro[0]+" WHERE marca = ?",[self.values[2]])
			if rubro[0] == "libreria":
				for tupla in cursor.fetchall():
					costo = round(tupla[0]*(1+float(self.values[0])/100),1)
					precio = round(costo*(1+float(self.values[1])/100),1)
					cursor.execute("UPDATE "+rubro[0]+" SET costo =?, precio =? WHERE codigo =?",(costo,precio,tupla[1]))
			else:
				for tupla in cursor.fetchall():
					costo = round(tupla[0]*(1+float(self.values[0])/100))
					precio = round(costo*(1+float(self.values[1])/100))
					cursor.execute("UPDATE "+rubro[0]+" SET costo =?, precio =? WHERE codigo =?",(costo,precio,tupla[1]))
			bbdd.commit()
			self.recargar_listas(self_padre,rubro[0],cursor)
		cursor.close()
		bbdd.close()
		
	def cambios_productos(self,self_padre):
		codigo = self.entry_codigo.get_text()
		aumento = self.entry_aumento.get_text()
		cantidad_entrante= self.entry_cantidad.get_text()
		pnt_rep = int(self.entry_pnt_rep.get_text())
		reponer = self.checkbutton_reponer.get_active()
		filtro = self.combobox_producto.get_active_text().lower()
		filtro = filtro.replace(" ","_")
		codigo = self.entry_codigo.get_text()#se llama codigo, pero tmb puede ir el nro art
		marca = self.entry_marcas.get_text()
		ruta = os.getcwd()
		rubro = self.tupla[1]
		self.tupla = self.tupla[0]
		if aumento != "":
			bbdd=bdapi.connect(ruta+'/Base_Datos/marcas_rosarinas.db')
			cursor=bbdd.cursor()
			cursor.execute("SELECT coeficiente FROM marca WHERE nombre =?",[self.tupla[4]])
			ganancia = cursor.fetchone()
			cursor.close()
			bbdd.close()
			bbdd=bdapi.connect(ruta+'/Base_Datos/stock_rosarino.db')
			cursor=bbdd.cursor()
			if rubro == "libreria":
				costo = round(self.tupla[5]*(1+float(aumento)/100),1)
				precio = round(costo*(1+ganancia[0]/100),1)
			else:
				costo = round(self.tupla[5]*(1+float(aumento)/100))
				precio = round(costo*(1+ganancia[0]/100))
			cursor.execute("UPDATE "+rubro+" SET costo =? , precio =?, sw =? WHERE "+filtro+" =? and marca =?",(costo,precio,reponer,codigo,marca))
			bbdd.commit()
			cursor.close()
			bbdd.close()
		if cantidad_entrante != "0":
			cantidad_total = int(cantidad_entrante)+self.tupla[7]
			bbdd=bdapi.connect(ruta+'/Base_Datos/stock_rosarino.db')
			cursor=bbdd.cursor()
			if cantidad_total < self.tupla[8] and reponer:
				cursor.execute("UPDATE "+rubro+" SET stk_disp =?, aviso =?, sw =? WHERE "+filtro+" =? AND marca =?",(cantidad_total,True,reponer,codigo,marca))
			else:
				cursor.execute("UPDATE "+rubro+" SET stk_disp =?, aviso =?, sw =? WHERE "+filtro+" =? AND marca =?",(cantidad_total,False,reponer,codigo,marca))
			bbdd.commit()
			cursor.close()
			bbdd.close()
		if pnt_rep != "0":
			bbdd=bdapi.connect(ruta+'/Base_Datos/stock_rosarino.db')
			cursor=bbdd.cursor()
			if self.tupla[7] < pnt_rep and reponer:
				cursor.execute("UPDATE "+rubro+" SET pnt_rep =?, aviso =?, sw =? WHERE "+filtro+" =? AND marca =?",(pnt_rep,True,reponer,codigo,marca))
			else:
				cursor.execute("UPDATE "+rubro+" SET pnt_rep =?, aviso =?, sw =? WHERE "+filtro+" =? AND marca =?",(pnt_rep,False,reponer,codigo,marca))
			bbdd.commit()
			cursor.close()
			bbdd.close()
		self.limpiar()
		self_padre.conectar_bd()
		
	def aceptar(self,widget,self_padre,event = None):
		pagina_activa = self.notebook.get_current_page()
		if pagina_activa == 0:
			self.cambios_marca(self_padre)
			self_padre.window.set_sensitive(True)
			self.window.destroy()
		else:
			self.cambios_productos(self_padre)
			self.entry_codigo.set_property("secondary-icon-stock",None)
			self.entry_aumento.set_property("secondary-icon-stock",None)
				
			
		
	def cancelar(self,widget,window):
		window.set_sensitive(True)
		self.window.destroy()
		
	def delete_event(self,widget,event,window):
		window.set_sensitive(True)
		self.window.destroy()
		

	def __init__(self,self_padre):
		self.tupla = []
		self.pagina1 = [True,True]
		self.pagina2 = [True,True]
		self.archivo_glade="./actualizaciones/ventana_actualizaciones.glade"
		self.glade=gtk.Builder()
		self.glade.add_from_file(self.archivo_glade)
		self_padre.window.set_sensitive(False)
		self.window = self.glade.get_object("window_actualizaciones")
		self.table = self.glade.get_object("table1")
		self.hbox = self.glade.get_object("hbox1")
		self.notebook = self.glade.get_object("notebook1")
		self.liststore_marca = self.glade.get_object("liststore_marca")
		self.label = self.glade.get_object("label10")
		self.entry_marcas = self.glade.get_object("entry_marca")
		self.entry_ganancia = self.glade.get_object("entry_ganancia")
		self.entry_aumento_marca = self.glade.get_object("entry_aumento_marca")
		self.entry_codigo = self.glade.get_object("entry_codigo")
		self.entry_aumento = self.glade.get_object("entry_aumento")
		self.entry_cantidad = self.glade.get_object("entry_cantidad")
		self.entry_pnt_rep = self.glade.get_object("entry_pnt_rep")
		self.entry_codigo.set_property("secondary-icon-stock",None)
		self.entry_aumento.set_property("secondary-icon-stock",None)
		self.entry_marcas.set_property("secondary-icon-stock",None)
		self.entry_aumento_marca.set_property("secondary-icon-stock",None)
		self.entry_cantidad.set_property("secondary-icon-stock",None)
		self.entry_ganancia.set_property("secondary-icon-stock",None)
		self.checkbutton_reponer = self.glade.get_object("checkbutton_reponer")
		self.btn_aceptar = self.glade.get_object("button_aceptar")
		self.btn_cancelar = self.glade.get_object("button_cancelar")
		self.btn_pag_marca = self.glade.get_object("button_act_marca")
		self.btn_pag_producto = self.glade.get_object("button_act_producto")
		self.combobox = gtk.combo_box_new_text()
		self.combobox.append_text("Bazar")
		self.combobox.append_text("Libreria")
		self.combobox.append_text("Jugueteria")
		self.combobox_producto = gtk.combo_box_new_text()
		self.combobox_producto.append_text("Codigo")
		self.combobox_producto.append_text("Nro Art")
		self.completion = gtk.EntryCompletion()
		self.completion.set_model(self.liststore_marca)
		self.entry_marcas.set_completion(self.completion)
		self.completion.set_text_column(0)
		self.table.attach(self.combobox,1,2,0,1)
		self.hbox.pack_start(self.combobox_producto,True,True)
		self.combobox.connect("changed",self.focusear_completation)
		self.entry_marcas.connect("activate",self.verificar_marca)
		self.entry_codigo.connect("activate",self.validar_codigo)
		self.entry_codigo.connect("focus-out-event",self.validar_codigo)
		self.entry_aumento.connect("focus-out-event",self.validar_entero,"aumento")
		self.entry_aumento.connect("activate",self.validar_entero,None,"aumento")
		self.entry_ganancia.connect("focus-out-event",self.validar_entero,"ganancia")
		self.entry_ganancia.connect("activate",self.validar_entero,None,"ganancia")
		self.entry_aumento_marca.connect("activate",self.validar_entero,None,"aumento marca")
		self.entry_aumento_marca.connect("focus-out-event",self.validar_entero,"aumento marca")
		self.entry_pnt_rep.connect("activate",self.desbloquear_botones)
		self.entry_cantidad.connect("activate",self.desbloquear_botones)
		self.entry_marcas.connect("focus-out-event",self.verificar_marca)
		self.btn_pag_producto.connect("clicked",self.cambiar_pagina,"producto")
		self.btn_pag_marca.connect("clicked",self.cambiar_pagina,"marca")
		self.btn_aceptar.connect("clicked",self.aceptar,self_padre)
		self.checkbutton_reponer.connect("clicked",self.desbloquear_botones)
		self.btn_cancelar.connect("clicked",self.cancelar,self_padre.window)
		self.window.connect("delete-event",self.delete_event,self_padre.window)
		self.label.set_sensitive(True)
		self.notebook.set_sensitive(False)
		self.combobox.show()
		self.combobox_producto.show()
