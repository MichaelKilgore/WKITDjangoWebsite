from django.test import TestCase
from http import HTTPStatus
from django.test.client import Client
from django.contrib.auth.models import User
import wkit.tables as tables

class CreateMentorTestCase(TestCase):
  def setUp(self):
    pass
		#self.client = Client()
		#self.user = User.objects.create_user('michael', 'michael.kilgore@gmail.com', 'kilgore')


