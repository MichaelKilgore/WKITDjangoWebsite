python3 -m venv env
source env/bin/activate
pip3 install django django-otp qrcode
./manage.py migrate
