# Проект **Foodgram - "Продуктовый помощник"**
ИЗМЕНИТЬ НА НОВЫЙ ![example workflow](https://github.com/sarafantofun/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)

### **Адрес проекта**
ДОБАВИТЬ

### **Описание проекта:**
сайт **Foodgram** - «Продуктовый помощник» <br>
На этом сервисе пользователи смогут <br> 
- публиковать рецепты <br>
- подписываться на публикации других пользователей <br>
- добавлять понравившиеся рецепты в список «Избранное» <br>
- скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

---

### **Технологии:**
Python 3.7 <br>
Django 3.2 <br>
DRF 3.12.4 <br>
Docker Hub <br>
Github Actions <br>
djoser==2.1.0 <br>
PostgreSQL <br>
nginx <br>
gunicorn <br>
Yandex cloud 

---

### **Разработчик:**
- Сарафанова Татьяна <br>
- GitHub: https://github.com/sarafantofun <br>

---

### **Запуск проекта:**
```
git clone git@github.com:sarafantofun/foodgram-project-react.git # клонируем проект
python -m venv venv # Создаем виртуальное окружение
. venv/Scripts/activate # Активируем виртуальное окружение
python -m pip install --upgrade pip
pip install -r requirements.txt
cd infra/ # Переходим в папку infra/
docker-compose up # Запуск docker-compose (Документация доступна по адресу http://localhost/api/docs/)

python manage.py importdata #заполняем базу ингредиентами
# Надо дописать!

```

---

### **шаблон наполнения env-файла**

ПОТОМ НАПИСАТЬ!
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=
DB_HOST=db
DB_PORT=5432
SECRET_KEY=''

```
---
### **Actions secrets**

```
DB_ENGINE
DB_HOST
DB_NAME
DB_PORT
DOCKER_PASSWORD
DOCKER_USERNAME
HOST
POSTGRES_PASSWORD
POSTGRES_USER
SECRET_KEY
SSH_KEY
TELEGRAM_TO
TELEGRAM_TOKEN
USER

```

---

### **Спецификация API Foodgram**
Документация: http://localhost/api/docs/

---

Данный проект , является дипломной работой начинающего программиста Сарафановой Татьяны <br>
https://github.com/sarafantofun <br>
Он сделан в рамках обучения на курсе Python-разработчик Яндекс-Практикума <br>
Backend разработкой, настройкой сервера , докера и тп <br>
