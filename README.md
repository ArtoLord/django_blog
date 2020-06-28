# Django blog

### Deploy
Чтобы запустить проект, нужно скопировать `blog/settings_local.py.example` в `blog/settings_local.py` и вставить туда логин и пароль от аккаунта google (я использую google smtp для отправки email), а так же добавить свой хост в `ALLOWED_HOSTS`, а так же изменить `HOSTNAME`, чтобы правильно отображались ссылки в email.
После этого можно запускать через docker:
```bash
$ docker-compose build
$ docker-compose up
```