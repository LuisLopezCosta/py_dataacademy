## Creando tu entorno virtual

### Si tienes problemas para descargar librerías con `pip` sigue los siguientes pasos:
1. Ingresa a Ejecutar (`Windows + R`), escribe `%APPDATA%` y dale aceptar.
2.  Ubica e ingresa a la carpeta llamada `pip`, en caso no exista debemos crearla
3. Ubica e ingresa al archivo `pip.ini`
4. Ingresemos la siguiente porción de código

```ini title="pip.ini"
[global]
trusted-host = pypi.python.org
               pypi.org
               files.pythonhosted.org
```

### Instalar la librería virtualenv en el global
```
pip install virtualenv
```

### Generando un entorno virtual llamado `venv`
*Recuerda que debes ubicarte en la ruta de tu proyecto antes de ejecutar el siguiente comando*
```
virtualenv venv
```

<br>

## Instala las librerías necesarias para el proyecto

### Activa tu entorno virtual
Manera manual (Windows)
```
venv/Scripts/activate
```

Manera manual (Linux)
```
source venv/Scripts/activate
```

### Instala las librerías necesarias
```
pip install -r requirements.txt
```