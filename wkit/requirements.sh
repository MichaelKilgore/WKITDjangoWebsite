python3 -m venv env
source env/bin/activate
pip3 install django django-otp qrcode
pip3 install phonenumbers django-two-factor-auth twilio
./manage.py migrate
