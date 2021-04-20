# Spike

### Introducción

Para el proyecto decidí utilizar Angular 10 en conjunto con Python+Flask en backend.
Para la base de datos use un simple SQLite, ya que algo más complejo iba a consumir
más horas, situación que terminó ocurriendo de todas formas y no quiero gastar más
horas de las solicitadas en las bases del desafío.

Lo funcional hasta el momento es el backend completo, acepta las siguientes rutas:

### Rutas
- /ping  (GET) Simplemente para saber si el backend esta operativo o no
- /calculate-distance (POST) Proceso principal que procesa las direcciones y calcula la distancia, ademas de ingresar
el registro a base de datos
- /records (GET) Ruta para acceder a los registros almacenados en la base de datos

En el diseño del microservicio se generaron los archivos Dockerfile y adicionalmente una utilidad que uso
para facilitar el despliegue logal mediante el archivo script Makefile.
También se agregó un componente de HTTP Basic Auth, para que los métodos importantes no sean consumidos por terceros,
asimismo las protecciones CORS.


### Pendientes
- Agregar el servicio en el proyecto Angular para consumir el microservicio Python+Flask
- Conectar el formulario al servicio
- Generar toda la interfaz de registro de consultas previas
- Darle un diseño aceptable
- Validar los inputs en todos lados
- Revisión profunda en ciberseguridad

### RUN
Para levantar el servicio del backend:
- pip install -r requirements.txt
- python app.py
o también
- make DST=prod
- make run_prod

Para levantar el sitio web aun falta escribir el dockerfile o script yaml de docker compose.
De todas formas eso es lo de menos, ya que esa integración es sencilla comparada con los temas aun 
pendientes en desarrollo.  Una vez finalizado eso, para el despliegue en cualquier plataforma mediante un pipeline no tomaría más
de una hora escribir el setup que corresponda.


### Palabras finales
Me divertí mucho en este desafío ya que hace muchos años no trabajaba con temas relacionados a GIS, así que muchas
gracias por la oportunidad de pasarla bien un rato.

##### Post data
Me pase 30 minutos escribiendo documentación