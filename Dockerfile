FROM ubuntu:18.04
ENV PATH="/root/miniconda3/bin:${PATH}"
ARG PATH="/root/miniconda3/bin:${PATH}"

RUN apt-get update \
 && apt-get install -y wget \
 && rm -rf /var/lib/apt/lists/*

RUN wget \
    https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh \
    && mkdir /root/.conda \
    && bash Miniconda3-latest-Linux-x86_64.sh -b \
    && rm -f Miniconda3-latest-Linux-x86_64.sh 

RUN conda --version

RUN conda create -n seguridad_cdmx python=3.6.9

RUN conda init bash \
 && . ~/.bashrc

RUN . activate seguridad_cdmx \
 && apt-get update \
 && conda install -c conda-forge folium -y \
 && pip install pandas \
 && pip install Flask \
 && pip install seaborn \
 && pip install SQLAlchemy


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

CMD ["/home/start.sh"]