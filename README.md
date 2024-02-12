
<h2>Всем привет, это Андрей <img src="https://github.com/blackcater/blackcater/raw/main/images/Hi.gif" height="32"/></h2>
</h2> 

<h3>Вы находитесь на странице моего учебного проекта Яндекс Практикум</h3> 

Перед Вами сайт-социальная сеть, построенная на Django. Пользователи могут регистрироваться, размещать посты, оставлять комментарии. Так же предусмотрена система рейтинга у каждого поста (За идею спасибо Pikabu)

## Технологии:

<details><summary>Подробнее</summary>

**Языки программирования, библиотеки и модули:**

[![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11-blue?logo=python)](https://www.python.org/)

**Фреймворк, расширения и библиотеки:**

[![Django](https://img.shields.io/badge/Django-v2.2.16-blue?logo=Django)](https://www.djangoproject.com/)


**Базы данных и инструменты работы с БД:**

[![SQLite3](https://img.shields.io/badge/-SQLite3-464646?logo=SQLite)](https://www.sqlite.com/version3.html)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?logo=PostgreSQL)](https://www.postgresql.org/)

**Фронт:**

![Static Badge](https://img.shields.io/badge/Bootstrap-5.2.0-blue?logo=Bootstrap&logoColor=blue)
![Static Badge](https://img.shields.io/badge/Jquery-3.6.1-blue?logo=jquery&logoColor=blue)

</details>

## Запуск:

<details><summary>Подробнее</summary>


Для удобства запуска в репозиторий добавлены база данных и файлы статики. Базовые шаги:


1. Клонируйте репозиторий с GitHub:
```bash
git clone git@github.com:AFrantsevich/hw05_final.git
```

2. Создайте и активируйте виртуальное окружение:
   * Если у вас Linux/macOS
   ```bash
    python -m venv venv && source venv/bin/activate
   ```
   * Если у вас Windows
   ```bash
    python -m venv venv && source venv/Scripts/activate
   ```
   
3. Установите в виртуальное окружение все необходимые зависимости из файла **requirements.txt**:
```bash
python -m pip install --upgrade pip && pip install -r requirements.txt
```

4. Создайте файл env по образцу env_example в случае использования SQLite блок DB НЕ указывать.

5. При необходиомсти создайте суперюзера и запустите приложение:
```bash
python yatube/manage.py create_superuser && \
python yatube/manage.py runserver
```
Сервер запустится локально по адресу `http://127.0.0.1:8000/`

6. Остановить приложение можно комбинацией клавиш Ctl-C.
<h1></h1>

</details>
