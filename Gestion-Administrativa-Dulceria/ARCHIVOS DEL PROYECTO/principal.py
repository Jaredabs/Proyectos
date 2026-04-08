# -*- coding: utf-8 -*-
"""
Created on Mon Nov  6 08:44:17 2023

@author: Absja
"""
import sys
import sqlite3
import pandas as pd
from proyecto import Ui_MainWindow


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication,QMessageBox#es para hacerle como el jopane de java
conexion= sqlite3.connect('Proyecto.db')
c= conexion.cursor()#seleccionar cada elemento de la base
global id
#or ord(i)>=48 and ord(i)<=57 or ord(i)==35 or ord(i)==44   , y #
class applicacionWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ventana = Ui_MainWindow()
        self.ventana.setupUi(self)
        self.ventana.mnuAMenu.triggered.connect(lambda: self.ventana.stackedWidget.setCurrentWidget(self.ventana.pageMenu))
        self.ventana.mnuAUsuarios.triggered.connect(lambda: self.ventana.stackedWidget.setCurrentWidget(self.ventana.pageUsuarios))	
        self.ventana.mnuAProveedores.triggered.connect(lambda: self.ventana.stackedWidget.setCurrentWidget(self.ventana.pageProveedores))	
        self.ventana.mnuAClientes.triggered.connect(lambda: self.ventana.stackedWidget.setCurrentWidget(self.ventana.pageClientes))	
        self.ventana.mnuAProductos.triggered.connect(lambda: self.ventana.stackedWidget.setCurrentWidget(self.ventana.pageProductos))	
        self.bd()
        self.cargarDatos()
        self.ventana.btnGuardar.clicked.connect(self.guardar)
        self.ventana.btnEliminar.clicked.connect(self.eliminar)
        self.ventana.btnSeleccionar.clicked.connect(self.seleccion)
        self.ventana.btnModificar.clicked.connect(self.modificar)
        
        self.ventana.btnEliminarclientes.clicked.connect(self.eliminarCliente)
        self.ventana.btnGuardarclientes.clicked.connect(self.guardarCliente)
        self.ventana.btnModificarclientes.clicked.connect(self.modificarCliente)
        self.ventana.btnSeleccionarclientes.clicked.connect(self.seleccionCliente)
        self.bdCliente()
        self.cargarDatosCliente()
        
        self.ventana.btnEliminarproveedor.clicked.connect(self.eliminarProveedor)
        self.ventana.btnGuardarproveedor.clicked.connect(self.guardarProveedor)
        self.ventana.btnModificarproveedor.clicked.connect(self.modificarProveedor)
        self.ventana.btnSeleccionarproveedor.clicked.connect(self.seleccionProveedor)
        self.bdProveedor()
        self.cargarDatosProveedor()
        
        self.ventana.btnEliminarproducto.clicked.connect(self.eliminarProducto)
        self.ventana.btnGuardarproducto.clicked.connect(self.guardarProducto)
        self.ventana.btnModificarproducto.clicked.connect(self.modificarProducto)
        self.ventana.btnSeleccionarproducto.clicked.connect(self.seleccionProducto)
        self.bdProducto()
        self.cargarDatosProducto()
        
        
        
        
        self.ventana.stackedWidget.setCurrentWidget(self.ventana.page)
        self.ventana.menubar.hide()
        self.ventana.btnIngresar.clicked.connect(self.validarLogin)
        self.ventana.btnPdfcliente.clicked.connect(self.clientesPdf)
        self.ventana.btnPdfusuario.clicked.connect(self.usuariosPdf)
        self.ventana.btnPdfproveedor.clicked.connect(self.proveedoresPdf)
    
    def clientesPdf(self):
        df = pd.read_sql_query("SELECT * FROM clientes", conexion)
        df.to_excel("Reporte_Clientes.xlsx", index=False)
       
            
    def usuariosPdf(self):
        pdf = pd.read_sql_query("SELECT * FROM usuario", conexion)
        pdf.to_excel("Reporte_Usuarios.xlsx", index=False)
        
    def proveedoresPdf(self):
        pdf = pd.read_sql_query("SELECT * FROM proveedores", conexion)
        pdf.to_excel("Reporte_Proveedores.xlsx", index=False)
        
            
    def validarLogin(self):
        u = self.ventana.txtU.text()
        p = self.ventana.txtC.text()

        c.execute("SELECT usuario, password FROM user;")
        conexion.commit()#cerrar o close 
        d=c.fetchall()#elige todos los elmentos de select y los manda a d
        usuario_enc = False  

        for usuario, password in d:
            print(usuario)
            if u==usuario and p==password:
                usuario_enc=True
                self.ventana.menubar.show()
                self.ventana.stackedWidget.setCurrentWidget(self.ventana.pageMenu)
                mensaje = QMessageBox()
                mensaje.setWindowTitle('Mensaje')
                mensaje.setIcon(QMessageBox.Information)
                mensaje.setText('Bienvenido')
                mensaje.setStandardButtons(QMessageBox.Ok)
                mensaje.exec_()
                break

        if usuario_enc==False:
            mensaje = QMessageBox()
            mensaje.setWindowTitle('Mensaje')
            mensaje.setIcon(QMessageBox.Information)
            mensaje.setText('Usuario erroneo')
            mensaje.setStandardButtons(QMessageBox.Ok)
            mensaje.exec_()
            self.ventana.menubar.hide(False)

        if u == 'admin':
            self.ventana.menubar.show()
        elif u == 'supervisor':
            self.ventana.mnuAUsuarios.setEnabled(False)
            self.ventana.btnPdfproducto.setEnabled(False)
            
        elif u=='trabajador':
            
            self.ventana.mnuAUsuarios.setEnabled(False)
            self.ventana.btnPdfcliente.setEnabled(False)
            self.ventana.btnPdfproveedor.setEnabled(False)
            self.ventana.btnPdfproducto.setEnabled(False)
            self.ventana.btnGuardarproducto.setEnabled(False)
            self.ventana.btnEliminarproducto.setEnabled(False)
            
    #PRODUCTOS   
    def seleccionProducto(self):
        global id
        fila= self.ventana.tableProductos.currentRow()#sellecionar fila que le di click
        id= self.ventana.tableProductos.item(fila,0).text()#id
        p= self.ventana.tableProductos.item(fila,1).text()#producto
        s= self.ventana.tableProductos.item(fila,2).text()#stock
        m= self.ventana.tableProductos.item(fila,3).text()#marca
        self.ventana.txtProducto.setText(p)
        self.ventana.btnStock.setText(s)
        self.ventana.txtMarca.setText(m)
      
    def modificarProducto(self):
        global id
        x=0
        b=0
        s=0
        p= self.ventana.txtProducto.text()
        st= self.ventana.btnStock.text()
        m= self.ventana.txtMarca.text()
       
        
        for i in p:
            if (ord(i)>=97 and ord(i)<=122) or (ord(i)>=65 and ord(i)<=90) or ord(i)==32:#mayus,mini y espacio
                   x+=1
        for i in st:
            if ord(i)>=48 and ord(i)<=57:#0-9
                b+=1
        for i in m:
            if (ord(i)>=97 and ord(i)<=122) or (ord(i)>=65 and ord(i)<=90) or ord(i)==32 :#mayus,mini y espacio 
                s+=1
        if len(p)==0 and len(st)==0 and len(m)==0:
            mensaje=QMessageBox()
            mensaje.setWindowTitle('Mensaje')
            mensaje.setIcon(QMessageBox.Information)
            mensaje.setText('ERROR: ingresa texto')
            mensaje.setStandardButtons(QMessageBox.Ok)
            mensaje.exec_()
        if x==len(p) and b==len(st) and s==len(m) and len(st)<4 and len(m)<31 and len(p)<30 and len(m)>4 and len(st)>0 and len(p)>4 and p[0]!=' ' and m[0]!=' ' :
            
            c.execute("UPDATE productos SET producto='"+p+"', stock='"+st+"', marca='"+m+"' WHERE id='" +str(id)+"'")
            conexion.commit()
            mensaje=QMessageBox()
            mensaje.setWindowTitle('Mensaje')
            mensaje.setIcon(QMessageBox.Information)
            mensaje.setText('Datos actualizados')
            mensaje.setStandardButtons(QMessageBox.Ok)
            estado=mensaje.exec_()
            if estado==QMessageBox.Ok:
                self.actualizarProducto()
            p= self.ventana.txtProducto.setText('')
            st= self.ventana.btnStock.setText('')
            m= self.ventana.txtMarca.setText('')
        else:
            mensaje=QMessageBox()
            mensaje.setWindowTitle('Mensaje')
            mensaje.setIcon(QMessageBox.Information)
            mensaje.setText('datos erroneos')
            mensaje.setStandardButtons(QMessageBox.Ok)
            mensaje.exec_()
            
        
        
    def eliminarProducto(self):
        global id
        fila= self.ventana.tableProductos.currentRow()#sellecionar fila que le di click
        id= self.ventana.tableProductos.item(fila,0).text()#id
        c.execute("DELETE FROM productos WHERE id='"+id+"'")
        conexion.commit()
        mensaje=QMessageBox()
        mensaje.setWindowTitle('Mensaje')
        mensaje.setIcon(QMessageBox.Information)
        mensaje.setText('Datos eliminados')
        mensaje.setStandardButtons(QMessageBox.Ok)
        estado=mensaje.exec_()
        if estado==QMessageBox.Ok:
            self.actualizarProducto()
        
        
    def actualizarProducto(self):#tabla
        fila=0
        c.execute("SELECT * FROM productos;")
        d= c.fetchall()#elige todos los elmentos de select y los manda a d
        self.ventana.tableProductos.setRowCount(len(d))
        for i in d:
            print(i)
            self.ventana.tableProductos.setItem(fila,0,QtWidgets.QTableWidgetItem(str(i[0])))
            self.ventana.tableProductos.setItem(fila,1,QtWidgets.QTableWidgetItem(i[1]))
            self.ventana.tableProductos.setItem(fila,2,QtWidgets.QTableWidgetItem(i[2]))
            self.ventana.tableProductos.setItem(fila,3,QtWidgets.QTableWidgetItem(i[3]))
            
            fila =fila+1
        
     
    def cargarDatosProducto(self):
        
        datos=[{"ID":"1","Producto:":"doritos","Stock":"12","Marca":"Sabritas"},{"ID":"1","Producto:":"chetos","Stock":"12","Marca":"Sabritas"}]
        fila=0
        
        c.execute("SELECT * FROM productos;")
        d= c.fetchall()#elige todos los elmentos de select y los manda a d
        self.ventana.tableProductos.setRowCount(len(d))
        for i in d:
            print(i)
            self.ventana.tableProductos.setItem(fila,0,QtWidgets.QTableWidgetItem(str(i[0])))
            self.ventana.tableProductos.setItem(fila,1,QtWidgets.QTableWidgetItem(i[1]))
            self.ventana.tableProductos.setItem(fila,2,QtWidgets.QTableWidgetItem(i[2]))
            self.ventana.tableProductos.setItem(fila,3,QtWidgets.QTableWidgetItem(i[3]))
            
            fila =fila+1
      
    
    def guardarProducto(self):
        x=0
        b=0
        s=0
        p= self.ventana.txtProducto.text()
        st= self.ventana.btnStock.text()
        m= self.ventana.txtMarca.text()
        for i in p:
            if (ord(i)>=97 and ord(i)<=122) or (ord(i)>=65 and ord(i)<=90) or ord(i)==32:#mayus,mini y espacio
                x+=1
        for i in st:
            if ord(i)>=48 and ord(i)<=57:#0-9
                b+=1
        for i in m:
            if (ord(i)>=97 and ord(i)<=122) or (ord(i)>=65 and ord(i)<=90) or ord(i)==32:#mayus,mini y espacio 
                s+=1
        if len(p)==0 and len(st)==0 and len(m)==0:
            mensaje=QMessageBox()
            mensaje.setWindowTitle('Mensaje')
            mensaje.setIcon(QMessageBox.Information)
            mensaje.setText('ERROR: ingresa texto')
            mensaje.setStandardButtons(QMessageBox.Ok)
            mensaje.exec_()
        if x==len(p) and b==len(st) and s==len(m) and len(st)<4 and len(m)<31 and len(p)<30 and len(m)>4 and len(st)>0 and len(p)>4 and p[0]!=' ' and m[0]!=' ' :
        #cuenta letra por letra el contador,  si sale un numero no lo cuenta y se va al else
         
           c.execute("INSERT INTO productos VALUES(null,?,?,?)",(p,st,m))#?=ubicar donde meteremos los datos nombre y telefono
           conexion.commit()#cerrar o close  
           mensaje=QMessageBox()
           mensaje.setWindowTitle('Mensaje')
           mensaje.setIcon(QMessageBox.Information)
           mensaje.setText('datos guardados')
           mensaje.setStandardButtons(QMessageBox.Ok)
           estado=mensaje.exec_()
           if estado==QMessageBox.Ok:
               self.actualizarProducto()
        
           p= self.ventana.txtProducto.setText('')
           st= self.ventana.btnStock.setText('')
           m= self.ventana.txtMarca.setText('')
        else:
            mensaje=QMessageBox()
            mensaje.setWindowTitle('Mensaje')
            mensaje.setIcon(QMessageBox.Information)
            mensaje.setText('datos erroneos')
            mensaje.setStandardButtons(QMessageBox.Ok)
            mensaje.exec_()
          

    def bdProducto(self):
    
    
        c.execute("""
                  CREATE TABLE IF NOT EXISTS productos(
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      producto VARCHAR(20),
                      stock VARCHAR(10),
                      marca VARCHAR(30)
                      );          
                  """)    
            
    #PROVEEDORES
    def seleccionProveedor(self):
        global id
        fila= self.ventana.tableProveedor.currentRow()#sellecionar fila que le di click
        id= self.ventana.tableProveedor.item(fila,0).text()#id
        n= self.ventana.tableProveedor.item(fila,1).text()#nombre
        t= self.ventana.tableProveedor.item(fila,2).text()#telefono
        e= self.ventana.tableProveedor.item(fila,3).text()#direccion
        self.ventana.txtNombreproveedor.setText(n)
        self.ventana.txtTelefonoproveedor.setText(t)
        self.ventana.txtEmpresa.setText(e)
      
    def modificarProveedor(self):
        global id
        x=0
        b=0
        s=0
        n= self.ventana.txtNombreproveedor.text()
        t= self.ventana.txtTelefonoproveedor.text()
        e= self.ventana.txtEmpresa.text()
       
        
        for i in n:
            if (ord(i)>=97 and ord(i)<=122) or (ord(i)>=65 and ord(i)<=90) or ord(i)==32:#mayus,mini y espacio
                   x+=1
        for i in t:
            if ord(i)>=48 and ord(i)<=57:#0-9
                b+=1
        for i in e:
            if (ord(i)>=97 and ord(i)<=122) or (ord(i)>=65 and ord(i)<=90) or ord(i)==32 :#mayus,mini y espacio 
                s+=1
        if len(n)==0 and len(e)==0 :
            mensaje=QMessageBox()
            mensaje.setWindowTitle('Mensaje')
            mensaje.setIcon(QMessageBox.Information)
            mensaje.setText('ERROR: ingresa texto')
            mensaje.setStandardButtons(QMessageBox.Ok)
            mensaje.exec_()
        if x==len(n) and b==len(t) and len(t)==10 and s==len(e) and len(e)<51 and len(n)<21 and len(n)>4 and len(e)>4 and e[0]!=' ' and t[0]=='3' and t[1]=='3':
            
            c.execute("UPDATE proveedores SET nombre='"+n+"', telefono='"+t+"', empresa='"+e+"' WHERE id='" +str(id)+"'")
            conexion.commit()
            mensaje=QMessageBox()
            mensaje.setWindowTitle('Mensaje')
            mensaje.setIcon(QMessageBox.Information)
            mensaje.setText('Datos actualizados')
            mensaje.setStandardButtons(QMessageBox.Ok)
            estado=mensaje.exec_()
            if estado==QMessageBox.Ok:
                self.actualizarProveedor()
            n= self.ventana.txtNombreproveedor.setText('')
            t= self.ventana.txtTelefonoproveedor.setText('')
            e= self.ventana.txtEmpresa.setText('')
        else:
            mensaje=QMessageBox()
            mensaje.setWindowTitle('Mensaje')
            mensaje.setIcon(QMessageBox.Information)
            mensaje.setText('datos erroneos')
            mensaje.setStandardButtons(QMessageBox.Ok)
            mensaje.exec_()
            
        
        
    def eliminarProveedor(self):
        global id
        fila= self.ventana.tableProveedor.currentRow()#sellecionar fila que le di click
        id= self.ventana.tableProveedor.item(fila,0).text()#id
        c.execute("DELETE FROM proveedores WHERE id='"+id+"'")
        conexion.commit()
        mensaje=QMessageBox()
        mensaje.setWindowTitle('Mensaje')
        mensaje.setIcon(QMessageBox.Information)
        mensaje.setText('Datos eliminados')
        mensaje.setStandardButtons(QMessageBox.Ok)
        estado=mensaje.exec_()
        if estado==QMessageBox.Ok:
            self.actualizarProveedor()
        
        
    def actualizarProveedor(self):#tabla
        fila=0
        c.execute("SELECT * FROM proveedores;")
        d= c.fetchall()#elige todos los elmentos de select y los manda a d
        self.ventana.tableProveedor.setRowCount(len(d))
        for i in d:
            print(i)
            self.ventana.tableProveedor.setItem(fila,0,QtWidgets.QTableWidgetItem(str(i[0])))
            self.ventana.tableProveedor.setItem(fila,1,QtWidgets.QTableWidgetItem(i[1]))
            self.ventana.tableProveedor.setItem(fila,2,QtWidgets.QTableWidgetItem(i[2]))
            self.ventana.tableProveedor.setItem(fila,3,QtWidgets.QTableWidgetItem(i[3]))
            
            fila =fila+1
        
    def cargarDatosProveedor(self):
        
        datos=[{"ID":"1","Nombre:":"fernando","Telefono":"33223623","Empresa":"Sabritas"},{"ID":"2","Nombre:":"edgar","Telefono":"332233","Empresa":"Barcel"}]
        fila=0
        
        c.execute("SELECT * FROM proveedores;")
        d= c.fetchall()#elige todos los elmentos de select y los manda a d
        self.ventana.tableProveedor.setRowCount(len(d))
        for i in d:
            print(i)
            self.ventana.tableProveedor.setItem(fila,0,QtWidgets.QTableWidgetItem(str(i[0])))
            self.ventana.tableProveedor.setItem(fila,1,QtWidgets.QTableWidgetItem(i[1]))
            self.ventana.tableProveedor.setItem(fila,2,QtWidgets.QTableWidgetItem(i[2]))
            self.ventana.tableProveedor.setItem(fila,3,QtWidgets.QTableWidgetItem(i[3]))
            
            fila =fila+1
      
    def guardarProveedor(self):
        x=0
        b=0
        s=0
        n= self.ventana.txtNombreproveedor.text()
        t= self.ventana.txtTelefonoproveedor.text()
        e= self.ventana.txtEmpresa.text()
        for i in n:
            if (ord(i)>=97 and ord(i)<=122) or (ord(i)>=65 and ord(i)<=90) or ord(i)==32:#mayus,mini y espacio
                x+=1
        for i in t:
            if ord(i)>=48 and ord(i)<=57:#0-9
                b+=1
        for i in e:
            if (ord(i)>=97 and ord(i)<=122) or (ord(i)>=65 and ord(i)<=90) or ord(i)==32:#mayus,mini y espacio 
                s+=1
        if len(n)==0 and len(e)==0:
            mensaje=QMessageBox()
            mensaje.setWindowTitle('Mensaje')
            mensaje.setIcon(QMessageBox.Information)
            mensaje.setText('ERROR: ingresa texto')
            mensaje.setStandardButtons(QMessageBox.Ok)
            mensaje.exec_()
        if  t[0]=='3' and t[1]=='3' and x==len(n) and b==len(t) and len(t)==10 and s==len(e) and len(e)<51 and len(n)<21 and len(n)>3 and len(e)>3 and e[0]!=' ' :
        #cuenta letra por letra el contador,  si sale un numero no lo cuenta y se va al else
         
           c.execute("INSERT INTO proveedores VALUES(null,?,?,?)",(n,t,e))#?=ubicar donde meteremos los datos nombre y telefono
           conexion.commit()#cerrar o close  
           mensaje=QMessageBox()
           mensaje.setWindowTitle('Mensaje')
           mensaje.setIcon(QMessageBox.Information)
           mensaje.setText('datos guardados')
           mensaje.setStandardButtons(QMessageBox.Ok)
           estado=mensaje.exec_()
           if estado==QMessageBox.Ok:
               self.actualizarProveedor()
        
           n= self.ventana.txtNombreproveedor.setText('')
           t= self.ventana.txtTelefonoproveedor.setText('')
           e= self.ventana.txtEmpresa.setText('')
        else:
            mensaje=QMessageBox()
            mensaje.setWindowTitle('Mensaje')
            mensaje.setIcon(QMessageBox.Information)
            mensaje.setText('datos erroneos')
            mensaje.setStandardButtons(QMessageBox.Ok)
            mensaje.exec_()
      
    def bdProveedor(self):
    
    
        c.execute("""
                  CREATE TABLE IF NOT EXISTS proveedores(
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      nombre VARCHAR(20),
                      telefono VARCHAR(10),
                      empresa VARCHAR(50)
                      );          
                  """)
        
    #CLIENTES
    def seleccionCliente(self):
        global id
        fila= self.ventana.tableClientes.currentRow()#sellecionar fila que le di click
        id= self.ventana.tableClientes.item(fila,0).text()#id
        n= self.ventana.tableClientes.item(fila,1).text()#nombre
        t= self.ventana.tableClientes.item(fila,2).text()#telefono
        d= self.ventana.tableClientes.item(fila,3).text()#direccion
        self.ventana.txtNombre.setText(n)
        self.ventana.txtTelefono.setText(t)
        self.ventana.txtDireccion.setText(d)
        
     
    def modificarCliente(self):
        x=0
        b=0
        s=0
        global id
        n= self.ventana.txtNombre.text()
        t= self.ventana.txtTelefono.text()
        d= self.ventana.txtDireccion.text()
        gato=d.count('#')
        for i in n:
            if (ord(i)>=97 and ord(i)<=122) or (ord(i)>=65 and ord(i)<=90) or ord(i)==32:#mayus,mini y espacio
                x+=1
        for i in t:
            if ord(i)>=48 and ord(i)<=57:#0-9
                b+=1
        for i in d:
            if (ord(i)>=97 and ord(i)<=122) or (ord(i)>=65 and ord(i)<=90) or ord(i)==32 or (ord(i)>=48 and ord(i)<=57) or ord(i)==35 or ord(i)==44:#mayus,mini y espacio 
                s+=1
        if len(n)==0 and len(d)==0:
            mensaje=QMessageBox()
            mensaje.setWindowTitle('Mensaje')
            mensaje.setIcon(QMessageBox.Information)
            mensaje.setText('ERROR: ingresa texto')
            mensaje.setStandardButtons(QMessageBox.Ok)
            mensaje.exec_()
        if x==len(n) and b==len(t) and len(t)==10 and s==len(d) and len(d)<51 and len(n)<21 and len(n)>3 and len(d)>5 and d[0]!=',' and d[0]!=' ' and  d[0]!='#' and d[-1]!=',' and d[-1]!=' ' and  d[-1]!='#' and gato<2 and t[0]=='3' and t[1]=='3':
            c.execute("UPDATE clientes SET nombre='"+n+"', telefono='"+t+"', direccion='"+d+"' WHERE id='" +str(id)+"'")
            conexion.commit()
            mensaje=QMessageBox()
            mensaje.setWindowTitle('Mensaje')
            mensaje.setIcon(QMessageBox.Information)
            mensaje.setText('Datos actualizados')
            mensaje.setStandardButtons(QMessageBox.Ok)
            estado=mensaje.exec_()
            if estado==QMessageBox.Ok:
                self.actualizarCliente()
            n= self.ventana.txtNombre.setText('')
            t= self.ventana.txtTelefono.setText('')
            d= self.ventana.txtDireccion.setText('')
        else:
            mensaje=QMessageBox()
            mensaje.setWindowTitle('Mensaje')
            mensaje.setIcon(QMessageBox.Information)
            mensaje.setText('datos erroneos')
            mensaje.setStandardButtons(QMessageBox.Ok)
            mensaje.exec_()
            
        
    def eliminarCliente(self):
        global id
        fila= self.ventana.tableClientes.currentRow()#sellecionar fila que le di click
        id= self.ventana.tableClientes.item(fila,0).text()#id
        c.execute("DELETE FROM clientes WHERE id='"+id+"'")
        conexion.commit()
        mensaje=QMessageBox()
        mensaje.setWindowTitle('Mensaje')
        mensaje.setIcon(QMessageBox.Information)
        mensaje.setText('Datos eliminados')
        mensaje.setStandardButtons(QMessageBox.Ok)
        estado=mensaje.exec_()
        if estado==QMessageBox.Ok:
            self.actualizarCliente()
        
        
    def actualizarCliente(self):#tabla
        fila=0
        c.execute("SELECT * FROM clientes;")
        d= c.fetchall()#elige todos los elmentos de select y los manda a d
        self.ventana.tableClientes.setRowCount(len(d))
        for i in d:
            print(i)
            self.ventana.tableClientes.setItem(fila,0,QtWidgets.QTableWidgetItem(str(i[0])))
            self.ventana.tableClientes.setItem(fila,1,QtWidgets.QTableWidgetItem(i[1]))
            self.ventana.tableClientes.setItem(fila,2,QtWidgets.QTableWidgetItem(i[2]))
            self.ventana.tableClientes.setItem(fila,3,QtWidgets.QTableWidgetItem(i[3]))
            
            fila =fila+1
       
    def cargarDatosCliente(self):
        
        datos=[{"ID":"1","Nombre:":"Admin","Telefono":"332236","Direccion":"mexico"},{"ID":"2","Nombre:":"edgar","Telefono":"332233","Direccion":"usa"}]
        fila=0
        
        c.execute("SELECT * FROM clientes;")
        d= c.fetchall()#elige todos los elmentos de select y los manda a d
        self.ventana.tableClientes.setRowCount(len(d))
        for i in d:
            print(i)
            self.ventana.tableClientes.setItem(fila,0,QtWidgets.QTableWidgetItem(str(i[0])))
            self.ventana.tableClientes.setItem(fila,1,QtWidgets.QTableWidgetItem(i[1]))
            self.ventana.tableClientes.setItem(fila,2,QtWidgets.QTableWidgetItem(i[2]))
            self.ventana.tableClientes.setItem(fila,3,QtWidgets.QTableWidgetItem(i[3]))
            
            fila =fila+1
    
    def guardarCliente(self):
        x=0
        b=0
        s=0
        n= self.ventana.txtNombre.text()
        t= self.ventana.txtTelefono.text()
        d= self.ventana.txtDireccion.text()
        gato=d.count('#')
        for i in n:
            if (ord(i)>=97 and ord(i)<=122) or (ord(i)>=65 and ord(i)<=90) or ord(i)==32:#mayus,mini y espacio
                x+=1
        for i in t:
            if ord(i)>=48 and ord(i)<=57:#0-9
                b+=1
        for i in d:
            if (ord(i)>=97 and ord(i)<=122) or (ord(i)>=65 and ord(i)<=90) or ord(i)==32 or (ord(i)>=48 and ord(i)<=57) or ord(i)==35 or ord(i)==44:#mayus,mini y espacio 
                s+=1
        
        if len(n)==0 and len(d)==0:
            mensaje=QMessageBox()
            mensaje.setWindowTitle('Mensaje')
            mensaje.setIcon(QMessageBox.Information)
            mensaje.setText('ERROR: ingresa texto')
            mensaje.setStandardButtons(QMessageBox.Ok)
            mensaje.exec_()
        if x==len(n) and b==len(t) and s==len(d) and len(t)==10 and len(n)<21 and len(d)<51 and len(n)>3 and len(d)>5 and d[0]!=',' and d[0]!=' ' and  d[0]!='#' and d[-1]!=',' and d[-1]!=' ' and  d[-1]!='#' and gato<2 and t[0]=='3' and t[1]=='3':#cuenta letra por letra el contador,  si sale un numero no lo cuenta y se va al else
         
           c.execute("INSERT INTO clientes VALUES(null,?,?,?)",(n,t,d))#?=ubicar donde meteremos los datos nombre y telefono
           conexion.commit()#cerrar o close  
           mensaje=QMessageBox()
           mensaje.setWindowTitle('Mensaje')
           mensaje.setIcon(QMessageBox.Information)
           mensaje.setText('datos guardados')
           mensaje.setStandardButtons(QMessageBox.Ok)
           estado=mensaje.exec_()
           if estado==QMessageBox.Ok:
               self.actualizarCliente()
           n= self.ventana.txtNombre.setText('')
           t= self.ventana.txtTelefono.setText('')
           d= self.ventana.txtDireccion.setText('')    
            
        else:
            mensaje=QMessageBox()
            mensaje.setWindowTitle('Mensaje')
            mensaje.setIcon(QMessageBox.Information)
            mensaje.setText('datos erroneos')
            mensaje.setStandardButtons(QMessageBox.Ok)
            mensaje.exec_()
           
          
    def bdCliente(self):
    
    
        c.execute("""
                  CREATE TABLE IF NOT EXISTS clientes(
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      nombre VARCHAR(20),
                      telefono VARCHAR(10),
                      direccion VARCHAR(50)
                      );          
                  """)
        
    #USUARIOS
    def seleccion(self):
        global id
        fila= self.ventana.tableWidget.currentRow()#sellecionar fila que le di click
        id= self.ventana.tableWidget.item(fila,0).text()#id
        u= self.ventana.tableWidget.item(fila,1).text()#user
        p= self.ventana.tableWidget.item(fila,2).text()#password
        self.ventana.txtUsuario.setText(u)
        self.ventana.txtPassword.setText(p)
        
        
        
    def modificar(self):
        global id
        x=0
        b=0
        u= self.ventana.txtUsuario.text()
        p= self.ventana.txtPassword.text()
        for i in u:
            if (ord(i)>=97 and ord(i)<=122) or (ord(i)>=65 and ord(i)<=90) or ord(i)==32:#mayus,mini y espacio
                x+=1
        for i in p:
            if ord(i)>=48 and ord(i)<=57:#0-9
                b+=1
        if len(u)<3 and len (p)<3:
            mensaje=QMessageBox()
            mensaje.setWindowTitle('Mensaje')
            mensaje.setIcon(QMessageBox.Information)
            mensaje.setText('ERROR: ingresa datos')
            mensaje.setStandardButtons(QMessageBox.Ok)
            mensaje.exec_()
        if x==len(u) and b==len(p) and  len(p)<11 and u=='admin' or u=='supervisor' or u=='trabajador':
            c.execute("UPDATE user SET usuario='"+u+"', password='"+p+"' WHERE id='"+str(id)+"'")
            conexion.commit()
            mensaje=QMessageBox()
            mensaje.setWindowTitle('Mensaje')
            mensaje.setIcon(QMessageBox.Information)
            mensaje.setText('Datos actualizados')
            mensaje.setStandardButtons(QMessageBox.Ok)
            estado=mensaje.exec_()
            if estado==QMessageBox.Ok:
                self.actualizar()
            u= self.ventana.txtUsuario.setText('')
            p= self.ventana.txtPassword.setText('')
            
        else:
            mensaje=QMessageBox()
            mensaje.setWindowTitle('Mensaje')
            mensaje.setIcon(QMessageBox.Information)
            mensaje.setText('datos erroneos')
            mensaje.setStandardButtons(QMessageBox.Ok)
            mensaje.exec_()
           
    def eliminar(self):
        global id
        
        fila= self.ventana.tableWidget.currentRow()#sellecionar fila que le di click
        id= self.ventana.tableWidget.item(fila,0).text()#id
        c.execute("DELETE FROM user WHERE id='"+id+"'")
        conexion.commit()
        mensaje=QMessageBox()
        mensaje.setWindowTitle('Mensaje')
        mensaje.setIcon(QMessageBox.Information)
        mensaje.setText('Datos eliminados')
        mensaje.setStandardButtons(QMessageBox.Ok)
        estado=mensaje.exec_()
        if estado==QMessageBox.Ok:
            self.actualizar()
        
        
    def actualizar(self):#tabla
        fila=0
        c.execute("SELECT * FROM user;")
        d= c.fetchall()#elige todos los elmentos de select y los manda a d
        self.ventana.tableWidget.setRowCount(len(d))
        for i in d:
            print(i)
            self.ventana.tableWidget.setItem(fila,0,QtWidgets.QTableWidgetItem(str(i[0])))
            self.ventana.tableWidget.setItem(fila,1,QtWidgets.QTableWidgetItem(i[1]))
            self.ventana.tableWidget.setItem(fila,2,QtWidgets.QTableWidgetItem(i[2]))
            fila =fila+1
        
    def cargarDatos(self):
        
        datos=[{"ID":"1","Usuario":"Admin","Password":"12345"},{"ID":"2","Usuario":"Invitado","Password":"12345"}]
        fila=0
        
        c.execute("SELECT * FROM user;")
        d= c.fetchall()#elige todos los elmentos de select y los manda a d
        self.ventana.tableWidget.setRowCount(len(d))
        for i in d:
            print(i)
            self.ventana.tableWidget.setItem(fila,0,QtWidgets.QTableWidgetItem(str(i[0])))
            self.ventana.tableWidget.setItem(fila,1,QtWidgets.QTableWidgetItem(i[1]))
            self.ventana.tableWidget.setItem(fila,2,QtWidgets.QTableWidgetItem(i[2]))
            fila =fila+1
      
    def guardar(self):
        x=0
        b=0
        u= self.ventana.txtUsuario.text()
        p= self.ventana.txtPassword.text()
        for i in u:
            if (ord(i)>=97 and ord(i)<=122) or (ord(i)>=65 and ord(i)<=90) or ord(i)==32:#mayus,mini y espacio
                x+=1
        for i in p:
            if ord(i)>=48 and ord(i)<=57:#0-9
                b+=1
        if len(u)<3 and len (p)<3:
            mensaje=QMessageBox()
            mensaje.setWindowTitle('Mensaje')
            mensaje.setIcon(QMessageBox.Information)
            mensaje.setText('ERROR: ingresa datos')
            mensaje.setStandardButtons(QMessageBox.Ok)
            mensaje.exec_()
            
            
        if x==len(u) and b==len(p) and  len(p)<11  and u=='admin' or u=='supervisor' or u=='trabajador':#cuenta letra por letra el contador,  si sale un numero no lo cuenta y se va al else
         
           c.execute("INSERT INTO user VALUES(null,?,?)",(u,p))#?=ubicar donde meteremos los datos nombre y telefono
           conexion.commit()#cerrar o close  
           mensaje=QMessageBox()
           mensaje.setWindowTitle('Mensaje')
           mensaje.setIcon(QMessageBox.Information)
           mensaje.setText('datos guardados')
           mensaje.setStandardButtons(QMessageBox.Ok)
           estado=mensaje.exec_()
           if estado==QMessageBox.Ok:
               self.actualizar()
           u= self.ventana.txtUsuario.setText('')
           p= self.ventana.txtPassword.setText('')
         
        else:
            mensaje=QMessageBox()
            mensaje.setWindowTitle('Mensaje')
            mensaje.setIcon(QMessageBox.Information)
            mensaje.setText('datos erroneos')
            mensaje.setStandardButtons(QMessageBox.Ok)
            mensaje.exec_()
           
    def bd(self):
        
        
        c.execute("""
        CREATE TABLE IF NOT EXISTS user(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario VARCHAR(20),
            password VARCHAR(10)
        );          
        """)
    
if __name__=='__main__':
    app= QApplication(sys.argv)
    v= applicacionWindow()
    v.show()
    sys.exit(app.exec_())