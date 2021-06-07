FROM tensorflow/tensorflow:1.14.0-py3

# Se instalan los paquetes necesarios
RUN apt-get update && apt-get install -y \
	libsm6 libxext6 libxrender-dev nginx supervisor curl libcurl4-openssl-dev libssl-dev

RUN pip install uWSGI==2.0.18 \
 && pip install folium \
 && pip install pandas \
 && pip install Flask \
 && pip install seaborn \
 && pip install SQLAlchemy \
 && pip install tensorflow==2.5.0

RUN useradd --no-create-home nginx

RUN apt-get update && apt-get install -y dos2unix

COPY start.sh /home/start.sh
RUN chmod 0777 /home/start.sh

COPY conf/nginx.conf /etc/nginx/
RUN dos2unix /etc/nginx/nginx.conf

COPY conf/flask-site-nginx.conf /etc/nginx/conf.d/
RUN dos2unix /etc/nginx/conf.d/flask-site-nginx.conf

COPY conf/uwsgi.ini /etc/uwsgi/
RUN dos2unix /etc/uwsgi/uwsgi.ini

COPY conf/supervisord.conf /etc/
RUN dos2unix /etc/supervisord.conf

RUN apt-get --purge remove -y dos2unix && rm -rf /var/lib/apt/lists/*

RUN mkdir /home/modelos \
&& mkdir /home/templates \
&& mkdir /home/static \
&& mkdir /home/log

COPY app_seguridad.py /home/app_seguridad.py
COPY mapea_delitos.py /home/mapea_delitos.py
COPY modelos/ /home/modelos/
COPY templates/ /home/templates/
COPY static/ /home/static/

CMD ["/home/start.sh"]