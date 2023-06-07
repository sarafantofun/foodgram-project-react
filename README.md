# Проект **Foodgram - "Продуктовый помощник"**
![example workflow](https://github.com/sarafantofun/foodgram-project-react/actions/workflows/main.yml/badge.svg)


### **URL проекта**
http://158.160.11.128/admin <br>

### **Документация доступна по адресу**
http://158.160.11.128/api/docs/redoc.html <br>

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
```

---

### **шаблон наполнения env-файла**

```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
SECRET_KEY='django-insecure-tqp3-u*dgy)#sovf%4+ny(d7w-z#hj=$5*rh*zev@_3z6sn+1m'

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
SSH_KEY

```

---

---

Данный проект , является дипломной работой начинающего программиста Сарафановой Татьяны <br>
https://github.com/sarafantofun <br>
Он сделан в рамках обучения на курсе Python-разработчик Яндекс-Практикума <br>
Backend разработкой, настройкой сервера , докера и тп <br>
