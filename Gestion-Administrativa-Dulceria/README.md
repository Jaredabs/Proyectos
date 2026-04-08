# 📊 Sistema de Gestión Administrativa Comercio (Clientes, Productos, Proveedores & Productos)

**Desarrollado con Python, PyQt5 y SQLite**

Desarrolle una aplicación de escritorio orientada a la digitalización y gestión administrativa de un comercio. Este sistema inicia con un login con usuario y contraseña. El sistema implementa un ciclo completo de operaciones CRUD (altas, bajas, cambios y consultas) para el control de inventarios, proveedores y clientes, hay diferentes rangos de usuarios en el cual permite diferentes acciones sobre el sistema dependiendo la jerarquia, integrando una interfaz gráfica intuitiva con persistencia de datos en SQLite.

---

## 🚀Vista Previa
![Pantalla Login](https://github.com/Jaredabs/Proyectos/blob/main/Gestion-Administrativa-Dulceria/img/Login.png)

_Interfaz gráfica diseñada en Qt Designer Login_

![Pantalla Principal de la Aplicación](https://github.com/Jaredabs/Proyectos/blob/main/Gestion-Administrativa-Dulceria/img/Menu%20Principal.png)

_Interfaz Menu Principal_

![Pantalla Clientes](https://github.com/Jaredabs/Proyectos/blob/main/Gestion-Administrativa-Dulceria/img/InterfazClientes.png)

_Interfaz Clientes_

![Pantalla Productos](https://github.com/Jaredabs/Proyectos/blob/main/Gestion-Administrativa-Dulceria/img/InterfazProductos.png)

_Interfaz Productos_

![Pantalla Proveedores](https://github.com/Jaredabs/Proyectos/blob/main/Gestion-Administrativa-Dulceria/img/InterfazProveedores.png)

_Interfaz Proveedores_

![Pantalla Usuarios](https://github.com/Jaredabs/Proyectos/blob/main/Gestion-Administrativa-Dulceria/img/InterfazUsuarios.png)

_Interfaz Usuarios_

---

## 🛠️ Stack Tecnológico

- **Lenguaje:** Python
- **Interfaz Gráfica:** PyQt5 / Qt Designer (`principal.ui`)
- **Base de Datos:** SQLite (`Proyecto.db`)
- **Manipulación de Datos:** Pandas (Procesamiento de reportes CSV)

---

## ✨ Características Principales

- **Gestión Integral (CRUD):** Registro, consulta, edición y eliminación de Clientes, Productos, Usuarios y Proveedores.
- **Integración de Reportes:** Creacion de reportes de los datos guardados en la base de datos.
- **Persistencia SQL:** Almacenamiento seguro de datos, garantizando que la información se mantenga tras cerrar la app.
- **Arquitectura Limpia:** Separación de la lógica de negocio (`principal.py`) y el diseño visual (`principal.ui`).

---

## 📂 Estructura del Proyecto

- `principal.py`: Lógica principal, conexión a base de datos y control de eventos.
- `principal.ui`: Interfaz visual XML generada en Qt Designer.
- `Proyecto.db`: Base de datos SQLite que contiene las tablas de registros.




