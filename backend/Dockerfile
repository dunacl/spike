FROM python:3.8.0-slim

# Timezone
ENV TZ=America/Santiago
# Expongo el puerto 
EXPOSE 3001

ADD requirements.txt /app/
WORKDIR /app 
RUN pip install -r requirements.txt

# Comando para ejecutar el archivo
COPY app.py /app

# Run
CMD ["gunicorn",  "-w 8", "-t 3600", "-b", "0.0.0.0:3001", "app:app"]
