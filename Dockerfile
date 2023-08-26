FROM node:12.18.2 AS node
WORKDIR /app
COPY package.json package-lock.json /app/
RUN npm ci --dev

FROM python:3.9 as python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY requirements.txt /app/
RUN apt update && apt install -y python3-pip                                  \
    && pip3 install -r requirements.txt                                       \
    && apt remove -y python3-pip                                              \
    && apt autoremove --purge -y                                              \
    && rm -rf /var/lib/apt/lists/* /etc/apt/sources.list.d/*.list

FROM python
WORKDIR /app
COPY --from=node /app/node_modules /app/node_modules
COPY --from=node /usr/local/bin/node /usr/local/bin/node
COPY --from=python /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY . .
RUN ./node_modules/.bin/parcel build bundles-src/index.js --dist-dir bundles --public-url="./"
RUN SECRET_KEY=empty python ./manage.py collectstatic --noinput
EXPOSE 8000
