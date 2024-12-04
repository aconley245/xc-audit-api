FROM unit:1.33.0-python3.11

COPY requirements.txt /config/requirements.txt
RUN mkdir /var/www/
RUN mkdir /var/www/app/
COPY *.py /war/www/app/
RUN chown -R unit:unit /var/www/
RUN pip install -r /config/requirements.txt
COPY ./config/*.json /docker-entrypoint.d/

EXPOSE 8000