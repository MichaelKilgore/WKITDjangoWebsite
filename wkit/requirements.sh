python3 -m venv env
source env/bin/activate
pip3 install django django-otp qrcode django-crispy-forms
pip3 install boto3 phonenumbers django-two-factor-auth twilio
pip3 install jsonpickle
./manage.py migrate
