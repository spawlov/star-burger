# Сайт доставки еды Star Burger

Это сайт сети ресторанов Star Burger. Здесь можно заказать превосходные бургеры с доставкой на дом.

##### Демоверсия сайта доступна по этой ссылке: [https://star-burger.s-pavlov.site/](https://star-burger.s-pavlov.site/)

![скриншот сайта](https://dvmn.org/filer/canonical/1594651635/686/)


Сеть Star Burger объединяет несколько ресторанов, действующих под единой франшизой. У всех ресторанов одинаковое меню и одинаковые цены. Просто выберите блюдо из меню на сайте и укажите место доставки. Мы сами найдём ближайший к вам ресторан, всё приготовим и привезём.

На сайте есть три независимых интерфейса. Первый — это публичная часть, где можно выбрать блюда из меню, и быстро оформить заказ без регистрации и SMS.

Второй интерфейс предназначен для менеджера. Здесь происходит обработка заказов. Менеджер видит поступившие новые заказы и первым делом созванивается с клиентом, чтобы подтвердить заказ. После оператор выбирает ближайший ресторан и передаёт туда заказ на исполнение. Там всё приготовят и сами доставят еду клиенту.

Третий интерфейс — это админка. Преимущественно им пользуются программисты при разработке сайта. Также сюда заходит менеджер, чтобы обновить меню ресторанов Star Burger.

## Как запустить dev-версию сайта

Для запуска сайта нужно запустить **одновременно** бэкенд и фронтенд, в двух терминалах.

### Как собрать бэкенд

Скачайте код:
```sh
git clone https://github.com/devmanorg/star-burger.git
```

Перейдите в каталог проекта:
```sh
cd star-burger
```

[Установите Python](https://www.python.org/), если этого ещё не сделали.

Проверьте, что `python` установлен и корректно настроен. Запустите его в командной строке:
```sh
python --version
```
**Важно!** Версия Python должна быть не ниже 3.6.

Возможно, вместо команды `python` здесь и в остальных инструкциях этого README придётся использовать `python3`. Зависит это от операционной системы и от того, установлен ли у вас Python старой второй версии.

В каталоге проекта создайте виртуальное окружение:
```sh
python -m venv venv
```
Активируйте его. На разных операционных системах это делается разными командами:

- Windows: `.\venv\Scripts\activate`
- MacOS/Linux: `source venv/bin/activate`


Установите зависимости в виртуальное окружение:
```sh
pip install -r requirements.txt
```

Определите переменную окружения `SECRET_KEY`. Создать файл `.env` в каталоге `star_burger/` и положите туда такой код:
```sh
DEBUG=True
SECRET_KEY=django-insecure-0if40nf4nf93n4
```

Создайте файл базы данных SQLite и отмигрируйте её следующей командой:

```sh
python manage.py migrate
```

Запустите сервер:

```sh
python manage.py runserver
```

Откройте сайт в браузере по адресу [http://127.0.0.1:8000/](http://127.0.0.1:8000/). Если вы увидели пустую белую страницу, то не пугайтесь, выдохните. Просто фронтенд пока ещё не собран. Переходите к следующему разделу README.

### Собрать фронтенд

**Откройте новый терминал**. Для работы сайта в dev-режиме необходима одновременная работа сразу двух программ `runserver` и `parcel`. Каждая требует себе отдельного терминала. Чтобы не выключать `runserver` откройте для фронтенда новый терминал и все нижеследующие инструкции выполняйте там.

[Установите Node.js](https://nodejs.org/en/), если у вас его ещё нет.

Проверьте, что Node.js и его пакетный менеджер корректно установлены. Если всё исправно, то терминал выведет их версии:

```sh
nodejs --version
# v12.18.2
# Если ошибка, попробуйте node:
node --version
# v12.18.2

npm --version
# 6.14.5
```

Версия `nodejs` должна быть не младше 10.0. Версия `npm` не важна. Как обновить Node.js читайте в статье: [How to Update Node.js](https://phoenixnap.com/kb/update-node-js-version).

Перейдите в каталог проекта и установите пакеты Node.js:

```sh
cd star-burger
npm ci --dev
```

Команда `npm ci` создаст каталог `node_modules` и установит туда пакеты Node.js. Получится аналог виртуального окружения как для Python, но для Node.js.

Помимо прочего будет установлен [Parcel](https://parceljs.org/) — это упаковщик веб-приложений, похожий на [Webpack](https://webpack.js.org/). В отличии от Webpack он прост в использовании и совсем не требует настроек.

Теперь запустите сборку фронтенда и не выключайте. Parcel будет работать в фоне и следить за изменениями в JS-коде:

```sh
./node_modules/.bin/parcel watch bundles-src/index.js --dist-dir bundles --public-url="./"
```

Если вы на Windows, то вам нужна та же команда, только с другими слешами в путях:

```sh
.\node_modules\.bin\parcel watch bundles-src/index.js --dist-dir bundles --public-url="./"
```

Дождитесь завершения первичной сборки. Это вполне может занять 10 и более секунд. О готовности вы узнаете по сообщению в консоли:

```
✨  Built in 10.89s
```

Parcel будет следить за файлами в каталоге `bundles-src`. Сначала он прочитает содержимое `index.js` и узнает какие другие файлы он импортирует. Затем Parcel перейдёт в каждый из этих подключенных файлов и узнает что импортируют они. И так далее, пока не закончатся файлы. В итоге Parcel получит полный список зависимостей. Дальше он соберёт все эти сотни мелких файлов в большие бандлы `bundles/index.js` и `bundles/index.css`. Они полностью самодостаточно и потому пригодны для запуска в браузере. Именно эти бандлы сервер отправит клиенту.

Теперь если зайти на страницу  [http://127.0.0.1:8000/](http://127.0.0.1:8000/), то вместо пустой страницы вы увидите:

![](https://dvmn.org/filer/canonical/1594651900/687/)

Каталог `bundles` в репозитории особенный — туда Parcel складывает результаты своей работы. Эта директория предназначена исключительно для результатов сборки фронтенда и потому исключёна из репозитория с помощью `.gitignore`.

**Сбросьте кэш браузера <kbd>Ctrl-F5</kbd>.** Браузер при любой возможности старается кэшировать файлы статики: CSS, картинки и js-код. Порой это приводит к странному поведению сайта, когда код уже давно изменился, но браузер этого не замечает и продолжает использовать старую закэшированную версию. В норме Parcel решает эту проблему самостоятельно. Он следит за пересборкой фронтенда и предупреждает JS-код в браузере о необходимости подтянуть свежий код. Но если вдруг что-то у вас идёт не так, то начните ремонт со сброса браузерного кэша, жмите <kbd>Ctrl-F5</kbd>.


## Как запустить prod-версию сайта

Собрать фронтенд:

```sh
./node_modules/.bin/parcel build bundles-src/index.js --dist-dir bundles --public-url="./"
```

Настроить бэкенд: создать файл `.env` в каталоге `star_burger/` со следующими настройками:

- `DEBUG` — дебаг-режим. Поставьте `False`.
- `SECRET_KEY` — секретный ключ проекта. Он отвечает за шифрование на сайте. Например, им зашифрованы все пароли на вашем сайте.
- `ALLOWED_HOSTS` — [см. документацию Django](https://docs.djangoproject.com/en/3.1/ref/settings/#allowed-hosts)

<hr>

##### Переход на `postgresql`:

Создать базу данных, создать пользователя с паролем и дать ему все привилегии для новой базы данных [Туториал по postgresql](https://www.digitalocean.com/community/tutorials/how-to-use-postgresql-with-your-django-application-on-ubuntu-14-04).

В файле `.env` в каталоге `star_burger/` определить переменную `DB_URL`:

- `DB_URL` — `postgres://user:password@host:port/db_name`.

В файле `star_burger/settings.py`, блоке подключение к `sqlite3` измените значение `default` на любое другое (например `notused`), а в блоке `postgresql` - измените значение `second` на `default`:
```python
DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:////{0}'.format(os.path.join(BASE_DIR, 'db.sqlite3'))
    ),
    'second': dj_database_url.config(
        default=env('DB_URL'),
        conn_max_age=600,
        conn_health_checks=True,
    )
}
```
Если вы более не планируете использовать `sqlite3` - блок подклюдчения к этой БД можно удалить.
<hr>

##### Добавление сервиса `Rollbar` (опционально):

Зарегистрируйтесь на сайте [http://rollbar.com](http://rollbar.com) получите токен.
Определите переменную окружения `ROLLBAR_TOKEN`. В файл `.env` добавить код:

- `ROLLBAR_TOKEN` — Ваш токен в Rollbar
- `ROLLBAR_ENV` = установить в `production` (если это Prod весия, иначе можно не устаналивать)

<hr>

##### Автоматический деплой:

Автоматический деплой производится запуском скрипта `deploy.sh` из корня проекта:
```sh
./deploy.sh
```

Если вы используете `Rollbar` - отредактируйте скрипт, а именно присвойте переменной значение своего токена иначе скрипт не будет сообщать о новом деплое в `Rollbar`:

- ROLLBAR_ACCESS_TOKEN = Ваш токен `post_server_item`

Скрипт осуществляет следующие действия:

- Выполняет команду `git pull`
- Активирует виртуальное окружение (если имя вашего виртуального окружения отличается от `venv` - отредактируйте `source venv/bin/activate`)
- Обновляет зависимости - `pip install -r requirements.txt`
- Обновляет библиотеки JS - `npm update`
- Пересобирает фронтенд - `./node_modules/.bin/parcel build bundles-src/index.js --dist-dir bundles --public-url="./"`
- Обновляет статику - `python manage.py collectstatic --noinput`
- Применяет миграции - `python manage.py migrate`
- Перзапускает `Gunicorn` и перезагружает `Nginx`
- Если указан токен - отправит сообщение в `Rollbar`

Скрипт завершает свою работу, если не возникло ошибок, сообщением `Deploy completed.`

<hr>

## Как запустить проект в docker

### dev - версия на локальном компьютере

Проверьте, что у вас установлен `docker` и `docker-compose`:

```sh
docker --version
docker-compose --version
```
Если нет, установите его - подробно, как скачать и установить `docker` на любую систему, смотрите на официальном сайте: [https://www.docker.com/](https://www.docker.com/)

Создайте файл `.env` содержащий:

```shell-session
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1
SECRET_KEY=<Secret KEY fo Django>
GEO_API_KEY=<GEO API KEY from Yandex>
ROLLBAR_TOKEN=<Rollbar Token - post_server_item>

POSTGRES_DB=<django_db>
POSTGRES_USER=<django_user>
POSTGRES_PASSWORD=<django_password>
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

Запустите сборку образов проекта командой:

```sh
docker-compose -f docker-compose.yml -d --build
```

Затем сделайте миграции:

```sh
docker-compose -f docker-compose.yml exec web python manage.py migrate --noinput
```

После окончания сборки проекта, сайт будет доступен по адресу `http://localhoct`

### prod - версия на сервере

Создайте образ Node.Js + Django и загрузите его на Docker Hub

```shell
docker build -t <Login for Docker Hub>/<Name your repo> .
docker login
docker push <Login for Docker Hub>/<Name your repo>
```

На сервере создайте файл `.env` с указанным выше содержимым (измените только значение `ALLOWED_HOSTS` в соответствии с IP-адресом вашего сервера) и скопируйте файл `nginx.conf`,

Создайте файл `docker-compose.yml`:

```shell-session
version: '3.8'

services:
  web:
    image: <Login for Docker Hub>/<Name your repo>
    command: gunicorn star_burger.wsgi:application --bind 0.0.0.0:8000
    volumes:
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    env_file:
      - ./.env
    expose:
      - 8000
    depends_on:
      db:
        condition: service_healthy
    healthcheck:
      test: [ "CMD", "curl", "-f", "http://localhost:8000/" ]
      interval: 30s
      timeout: 10s
      retries: 3
    restart: always

  db:
    image: postgres:14.2
    volumes:
      - ./db/star-burger/data:/var/lib/postgresql/data
    env_file:
      - ./.env
    healthcheck:
      test: [ "CMD-SHELL", "pg_isready -U ${POSTGRES_USER} -d ${POSTGRES_DB}" ]
      interval: 30s
      timeout: 10s
      retries: 3
    restart: unless-stopped

  nginx:
    image: nginx:latest
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    ports:
      - "80:80"
    depends_on:
      web:
        condition: service_healthy

volumes:
  static_volume:
  media_volume:

```

Запустите сборку проекта

```sh
docker-compose -f docker-compose.yml -d --build
```

Затем сделайте миграции:

```sh
docker-compose -f docker-compose.yml exec web python manage.py migrate --noinput
```

После окончания сборки проекта, сайт будет доступен по адресу `http://<IP-фдрес вашего сервера>`

<hr>

## Цели проекта

Код написан в учебных целях — это урок в курсе по Python и веб-разработке на сайте [Devman](https://dvmn.org). За основу был взят код проекта [FoodCart](https://github.com/Saibharath79/FoodCart).

Где используется репозиторий:

- Второй и третий урок [учебного курса Django](https://dvmn.org/modules/django/)
