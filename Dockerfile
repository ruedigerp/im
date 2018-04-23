FROM alpine:latest
MAINTAINER Ruediger Kuepper <ruediger@kuepper.nrw>
RUN apk add --no-cache python3 && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools && \
    rm -r /root/.cache
COPY ./web_app/requirements.txt /tmp/requirements.txt
RUN pip3 install -qr /tmp/requirements.txt
RUN mkdir -p /opt/webapp
COPY ./web_app /opt/webapp/
# VOLUME ./static /opt/webapp/static
WORKDIR /opt/webapp
EXPOSE 5000
CMD ["python3", "app.py" ]
