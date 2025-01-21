# Proyecto de procesos
Es un proyecto basado en Django y Mysql

 Versiones:
 - python version: 3.10
 - Django version: 4.2
 - mysql version: 8.0

# Instalando el proyecto

## levantar el Docker con las variables ".env" personalizadas:
  `docker compose --env-file app/.env up --build`
    - **Nota**: El archivo *.env* debe estar a la misma altura de *manage.py*, hacer una copia: *.env_sample*

## Cargar la preData:
   `docker exec -ti django-web python3 manage.py loaddata apps/common/fixtures/001_user_base.json`
   `docker exec -ti django-web python3 manage.py loaddata apps/common/fixtures/002_servicios.json`

## Visit webSite: 
  `http://localhost:8001` or `http://localhost:8001/admin`

## Usuarios default:
  | Rol           | Usuario     | pass     |
  |---------------|-------------|----------|
  | Administrador | admin       | admin    |
  | Cliente       | cliente     | admin    |
 

## inspeccionar los logs (django-web):
  `docker logs -f django-web`

## Create superuser : 
  `docker exec -it django-web python manage.py createsuperuser`

# ---------------

# Notas adicionales

## Instalar enviroment local en caso necesitar
- Verificar la zona horaria con "America/lima"
- Instalar pip `sudo apt-get install python-pip`
- Instalar enviroment `sudo apt-get install python3.8-venv`
- Crear un entorno virtual: `python3 -m venv venv_accidentes`
- activar entorno `source venv_accidentes\bin\active`


  ### Descargar el git y el enviroment (.env)
  - Instalar el conector MariadB:
  `sudo apt-get install python3-dev default-libmysqlclient-dev build-essential`
  - Luego instalar los requerimientos con el entorno activado :
  `(venv_accidentes)$ pip install --upgrade -r requirements.txt`

  - Correr en la consola usando:
  `(venv_accidentes)$ python manage.py runserver --settings=core.settings`

  - Correr las migraciones:
    `python manage.py migrate --settings=core.settings`

## Para crear una nueva app
 - Se tiene que crear con el comando:
   `python manage.py startapp name_my_app`
 - Luego moverla a la carpeta **apps**, en donde se encuentra todas las apps creadas previamente.
    renombrar la variable **name**:  `name = 'apps.base'`

## Sobre uso de constantes en el proyecto
 - El manejo de todas las constantes esta en el archivo **constants** para todo el proyecto, la ubicacion esta en la carpeta "common" dentro de apps

# --------------- 
# Fuentes:
   * (https://github.com/harveydf/tutoriales-django-environments)
   * https://www.youtube.com/watch?v=_DJahG4FiOE
   * https://adminlte.io/themes/v3/index.html
   * https://github.com/ColorlibHQ/AdminLTE
   * Font Awesome Free 5.15.4 by @fontawesome - https://fontawesome.com
   
---
- Se reviso la libreria `django-crum` en https://pythonhosted.org/django-crum
- Como BD use el por defecto sqlite3, asi el administrador de BD = DBeaver

# ---------------
# Adicionales

 - Ubicarnos dentro de la carpeta **base**
 - Otros:
    ```sh
    $ docker exec -ti django-web python3 manage.py shell
    $ docker exec -ti django-web python3 manage.py createsuperuser
    $ docker exec -ti django-web python3 manage.py startapp remittance
    $ docker exec -ti django-web python3 manage.py makemigrations
    $ docker exec -ti django-web python3 manage.py migrate
    $ docker exec -ti django-web python3 manage.py makemigrations myapp --empty
    $ docker exec -ti django-web python3 manage.py showmigrations
    $ docker exec -ti django-web python3 manage.py loaddata apps/common/fixtures/001_user_base.json
    ```
 - Para iniciar el docker en local luego de haber creado las images y instancias:
   ```sh
    $ docker start django-web 
    $ docker start mysql-container
   ```
      
 - Para destruir el docker en local:
   ```sh
    $ docker stop django-web mysql-container
    $ docker rm -v django-web mysql-container
    $ sudo rm -R data
    $ docker image rm proy_accidentes_web
   ```
   
 - limpiar archivos .pyc
   ```sh
    # clear cache python
    find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf
   
---
# Screenshots

- Dashboard
 <img alt="Screenshot" height="200" src="docs/img/example_dashboard.png" title="Dashboard_template" width="400"/>
 
 - Login
 <img alt="Screenshot" height="200" src="docs/img/example_login.png" title="Dashboard_template" width="400"/>

Jaime 