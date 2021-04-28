FROM docker:stable
RUN apk add --update curl && rm -rf /var/cache/apk/*
RUN apk add python3-dev py-pip libffi-dev openssl-dev gcc libc-dev make bash
RUN pip install cryptography==3.3.2 docker-compose jinja2 ruamel.yaml
