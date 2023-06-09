### Данный проект нацелен на создание сайта, позволяющего искать различные произведения искусства с использованием сторонних API (на момент написания этого текста - V&A API, IIIF API). В нем присутствует функционал как поисковой системы (обычный текстовый запрос, текстовый запрос с параметрами), так и относительно примитивной социальной сети (пользовательские аккаунты, подписки на другие аккаунты, посты (публичные и приватные), закладки, подсчет взаимодействий с произведениями искусства)
1. Использованные модули и API
* api:
  * V&A Collections API
  * IIIF Image API
* модули:
  * Flask (2.2.3) - фреймворк, на котором строится данное веб-приложение
  * Jinja2 (3.1.2) - шаблонизатор для питона, позволяет работать с html шаблонами, использовать в них переменные, условия и циклы
  * SQLAlchemy (2.0.8) - модуль для работы с базой данных через ORM
  * Flask-Login (0.6.2) - дополнение для Flask, позволяющее добавить систему создания и логина в аккаунты, чьи данные хранятся в базе данных
  * Werkzeug (2.2.3) - модуль для защиты и хэширования паролей
  * WTForms (3.0.1) - библиотека для подтверждения и рендера форм в HTML
  * Flask-WTF (1.1.1) - модуль для интеграции WTForms с Flask
  * requests (2.28.2) - модуль для обращения к API и работы с полученными от API ответами
  * Pillow (9.5.0) - библиотека, используемая в данном проекте для того, чтобы хранить все пользовательские фото в одном размере
2. Структура проекта

##### В корневой директории лежат шесть файлов и пять поддиректорий.
##### Файлы:
* .gitignore - указывает Git, какие файлы необходимо игнорировать
* requirements.txt - файл со всеми сторонними модулями (с указанием конкретных версий), используемыми приложением
* start.sh - BASH-скрипт, позволяющий Glitch запустить данное приложение
* server.py - основной файл приложения, содержащий обработку ошибок, регистрации/входа в аккаунт, а также обработку всех страниц и действий, совершающихся в приложении. Код разделен (комментариями) на отделы, которые дают понимание того, за что отвечает тот или иной отдел.
* agents.py - содержит функции-агенты, которыми пользуются несколько разных страниц
* api_request.py - вспомогательный файл с функциями, используемыми для осуществления различных типов запросов к API  V&A:
#### Директории:
* forms - папка с тремя файлами с классами форм, использующихся в приложении. Классы разбиты на файлы по их назначению: в search_forms.py все, касающиеся поиска; в user_forms все, что взаимодействуют с данными о пользователях; в post_forms все, что связаны с созданием постов
* db - директория с базой данных приложения
* data - директория с файлами для организации ORM-модели и работы с базой данных таким образом (__all_models.py & db_session.py помогают иниализации БД, users.py, subscriptions.py, content.py, bookmarks.py & posts.py отвечают за соответствующие им таблицы в БД)

* templates

Содержит html-шаблоны для страниц. Названия шаблонам даны с учетом выполняемой ими функции; некоторые шаблоны могут использоваться для нескольких разных страниц одновременно.
Есть основной шаблон base.html, содержащий все, что есть на каждой странице сайта; base_with_profile_opt.html, содержащий кнопки, которые не должны отображаться на части страниц (наследуется от base.html); base_profile_pagination, добавляющий кнопки для перехода между страницами там, где есть такая необходимость (например, список постов) ((наследуется от base_with_profile_opt.html));
Остальные шаблоны наследуется от одного из этих трех.
* static

Содержит папки со статичными данными, а именно:
  * * css
custom.css - файл для дополнительной стилизации через css
  * * js
js_masonry_fix.js - попытка исправить баг с имплементацией masonry в Bootstrap 5.x.x
  * * img
Внутри папки img находится логотип сервиса в формате .svg, изображения для кнопок действий, а также еще две директории:
  * * * avatar пользовательские фото
  * * * error_images - изображения для отображения  с различными кодами ошибок
