Todolist

Веб планировщик задач, в котором вы можете формулировать цели, отслеживать их достижение.

Требования и установка

Для успешной работы проекта вам потребуется:

``OS: Windows/Linux``

``Python >= 3.10``

В проекте используются следующие основные библиотеки:

``Django 4.1.3``

Полный список зависимостей представлен в файле ``requirements.txt``

Клонируйте репозиторий:

``git clone https://github.com/KateNova/lesson33.git``


После клонирования репозитория выполните следующий команды:

``cd lesson33``

``python3 -m venv venv``

``source venv/bin/activate``

``pip install -r requirements.txt``

``cd todolist``

Для работы проекта необходим файл .env

Cоздайте файл командой ``touch .env``

Заполните созданный файл в соответствии с именами переменных в файле ``.env.example``

``python manage.py migrate``

``python manage.py runserver``

``python manage.py createsuperuser``

После создания администратора вам будет доступна админ-панель по адресу /admin/