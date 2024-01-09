# # shop_market
# My internet shop Django
# создаем приложения - python3 manage.py startapp products

# sudo apt install python3-venv
# python3 -m venv venv
# source venv/bin/activate
# pip install django
# pip install sorl-thumbnail
# pip install python-slugify
# pip install pillow
# python3 manage.py makemigrations
# python3 manage.py migrate
# http://127.0.0.1:8001/ -->

# усли работаем в винде то подключение Venv следующее
# 1. Запустить VS Code от имени администратора, перейти в каталог проекта в 
# PowerShell, выполнить код ниже, появится папка env, содержащая файлы виртуального окружения
# python -m venv env - windows; # python3 -m venv env/venv

# 2. Изменить политику, в PowerShell набрать
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# 3. Войти в папку окружения (env), выполнить команду
# env\Scripts\activate.ps1 - windows
# source venv/bin/activate - для Linux

# 4. Впереди в PowerShell появится маркер окружения (env), но VS Code может о нем все еще ничего не знать. 
# Нажать Ctrl+Shift + P, набрать Python: Select Interpreter
# Указать нужный путь к python.exe в папке окружения env, это отобразится внизу в панели состояния.
#  Профит! Теперь можно устанавливать модули только для конкретного проекта.

# 5. Если нужно будет выйти, то в PowerShell выполнить deactivate, в выборе интерпетатора вернуться на глобальный.


# server {
#   listen 80;
#   server_name karnel26.fvds.ru www.karnel26.fvds.ru 62.109.0.164;
# 
#    location = /favicon.ico { access_log off; log_not_found off; }
#    location /static/ {
#        root /var/www/html/e-shop;
#    }
# 
#    location /media/ {
#        root /var/www/html/e-shop;
#    }
# 
#    location / {
#        include proxy_params;
#        proxy_pass http://unix:/run/gunicorn.sock;
#    }
# } 