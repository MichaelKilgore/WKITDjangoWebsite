from django.test import TestCase
from http import HTTPStatus
from django.test.client import Client
from django.contrib.auth.models import User
import wkit.tables as tables

class CreateStudentTestCase(TestCase):
  def setUp(self):
    self.client = Client()
    self.user = User.objects.create_user('michael', 'michael.kilgore@gmail.com', 'kilgore')
    self.temp_id = ""

  def test_create_student_multi_interests(self):
    self.client.login(username='michael', password='kilgore')
    response = self.client.post("/student/create/", data={
      'first_name': 'michael',
      'last_name': 'kilgore',
      'email': 'happy.guy@gmail.com',
      'phone_number': '555-555-5555',
      'address': '99th St SW',
      'apartment': '16B',
      'city': 'Lynnwood',
      'zip': '99009',
      'school': 'Lynnwood High School',
      'grade': '11',
      'interest': ['Computer Science', 'Mechanic', 'Fishing'],
      'assessment': 'blacksmith',
      'preferred_method': 'Email',
      'gender': 'Cisgender Male',
      'ethnicity': 'asian',
      'notes': 'gotta blast'
    }, follow=True)
    self.assertEqual(response.status_code, HTTPStatus.OK)
    self.assertContains(response, 'michael', status_code=200)
    self.assertContains(response, 'kilgore', status_code=200)
    self.assertContains(response, 'happy.guy@gmail.com', status_code=200)
    self.assertContains(response, '555-555-5555', status_code=200)
    self.assertContains(response, '99th St SW', status_code=200)
    self.assertContains(response, '16B', status_code=200)
    self.assertContains(response, 'Lynnwood', status_code=200)
    self.assertContains(response, '99009', status_code=200)
    self.assertContains(response, 'Lynnwood High School', status_code=200)
    self.assertContains(response, 'Edmonds School District', status_code=200)
    self.assertContains(response, 'Computer Science', status_code=200)
    self.assertContains(response, 'blacksmith', status_code=200)
    self.assertContains(response, 'Email', status_code=200)
    self.assertContains(response, 'Cisgender Male', status_code=200)
    self.assertContains(response, 'asian', status_code=200)
    self.assertContains(response, 'gotta blast', status_code=200)

    #test throwing get request at students profile now that is created.
    response = self.client.get("/student/profile/"+response.context['student']['id'], follow=True)  
    self.assertEqual(response.status_code, HTTPStatus.OK)
    self.assertContains(response, 'michael', status_code=200)
    self.assertContains(response, 'kilgore', status_code=200)
    self.assertContains(response, 'happy.guy@gmail.com', status_code=200)
    self.assertContains(response, '555-555-5555', status_code=200)
    self.assertContains(response, '99th St SW', status_code=200)
    self.assertContains(response, '16B', status_code=200)
    self.assertContains(response, 'Lynnwood', status_code=200)
    self.assertContains(response, '99009', status_code=200)
    self.assertContains(response, 'Lynnwood High School', status_code=200)
    self.assertContains(response, 'Edmonds School District', status_code=200)
    self.assertContains(response, 'Computer Science', status_code=200)
    self.assertContains(response, 'blacksmith', status_code=200)
    self.assertContains(response, 'Email', status_code=200)
    self.assertContains(response, 'Cisgender Male', status_code=200)
    self.assertContains(response, 'asian', status_code=200)
    self.assertContains(response, 'gotta blast', status_code=200)

    #test pulling data directly from the table.
    info = tables.getStudent(response.context['student']['id'])
    self.assertEqual(info['first_name'], 'michael')
    self.assertEqual(info['last_name'], 'kilgore')
    self.assertEqual(info['email'], 'happy.guy@gmail.com')
    self.assertEqual(info['phone_number'], '555-555-5555')
    self.assertEqual(info['address'], '99th St SW')
    self.assertEqual(info['apartment'], '16B')
    self.assertEqual(info['city'], 'Lynnwood')
    self.assertEqual(info['zip'], '99009')
    self.assertEqual(info['school'], 'Lynnwood High School')
    self.assertEqual(info['district'], 'Edmonds School District')
    self.assertEqual(info['interest'], 'Computer Science, Mechanic, Fishing')
    self.assertEqual(info['assessment'], 'blacksmith')
    self.assertEqual(info['preferred_method'], 'Email')
    self.assertEqual(info['gender'], 'Cisgender Male')
    self.assertEqual(info['ethnicity'], 'asian')
    self.assertEqual(info['notes'], 'gotta blast')
  
    self.temp_id = info['id']

  def test_create_student_multi_interests_delete(self):
    #delete person that was added.
    tables.deleteStudent(self.temp_id)

    



  def test2(self):
    pass

  """
  def test_create_valid_student(self):
    #test creating student.
    self.client.login(username='michael', password='kilgore')
    response = self.client.post("/student/create/", data={
      'first_name': 'michael',
      'last_name': 'kilgore',
      'email': 'happy.guy@gmail.com',
      'phone_number': '555-555-5555',
      'address': '99th St SW',
      'apartment': '16B',
      'city': 'Lynnwood',
      'zip': '99009',
      'school': 'Lynnwood High School',
      'grade': '11',
      'interest': 'Computer Science',
      'assessment': 'blacksmith',
      'preferred_method': 'Email',
      'gender': 'Cisgender Male',
      'sexual_orientation': 'Asexual',
      'ethnicity': 'Asian',
      'notes': 'gotta blast'
    }, follow=True)
    self.assertEqual(response.status_code, HTTPStatus.OK)
    self.assertContains(response, 'michael', status_code=200)
    self.assertContains(response, 'kilgore', status_code=200)
    self.assertContains(response, 'happy.guy@gmail.com', status_code=200)
    self.assertContains(response, '555-555-5555', status_code=200)
    self.assertContains(response, '99th St SW', status_code=200)
    self.assertContains(response, '16B', status_code=200)
    self.assertContains(response, 'Lynnwood', status_code=200)
    self.assertContains(response, '99009', status_code=200)
    self.assertContains(response, 'Lynnwood High School', status_code=200)
    self.assertContains(response, 'Edmonds School District', status_code=200)
    self.assertContains(response, 'Computer Science', status_code=200)
    self.assertContains(response, 'blacksmith', status_code=200)
    self.assertContains(response, 'Email', status_code=200)
    self.assertContains(response, 'Cisgender Male', status_code=200)
    self.assertContains(response, 'Asexual', status_code=200)
    self.assertContains(response, 'Asian', status_code=200)
    self.assertContains(response, 'gotta blast', status_code=200)
    
    #test throwing get request at students profile now that is created.
    response = self.client.get("/student/profile/"+response.context['student']['id'], follow=True)  
    self.assertEqual(response.status_code, HTTPStatus.OK)
    self.assertContains(response, 'michael', status_code=200)
    self.assertContains(response, 'kilgore', status_code=200)
    self.assertContains(response, 'happy.guy@gmail.com', status_code=200)
    self.assertContains(response, '555-555-5555', status_code=200)
    self.assertContains(response, '99th St SW', status_code=200)
    self.assertContains(response, '16B', status_code=200)
    self.assertContains(response, 'Lynnwood', status_code=200)
    self.assertContains(response, '99009', status_code=200)
    self.assertContains(response, 'Lynnwood High School', status_code=200)
    self.assertContains(response, 'Edmonds School District', status_code=200)
    self.assertContains(response, 'Computer Science', status_code=200)
    self.assertContains(response, 'blacksmith', status_code=200)
    self.assertContains(response, 'Email', status_code=200)
    self.assertContains(response, 'Cisgender Male', status_code=200)
    self.assertContains(response, 'Asexual', status_code=200)
    self.assertContains(response, 'Asian', status_code=200)
    self.assertContains(response, 'gotta blast', status_code=200)

    #test pulling data directly from the table.
    info = tables.getStudent(response.context['student']['id'])
    self.assertEqual(info['first_name'], 'michael')
    self.assertEqual(info['last_name'], 'kilgore')
    self.assertEqual(info['email'], 'happy.guy@gmail.com')
    self.assertEqual(info['phone_number'], '555-555-5555')
    self.assertEqual(info['address'], '99th St SW')
    self.assertEqual(info['apartment'], '16B')
    self.assertEqual(info['city'], 'Lynnwood')
    self.assertEqual(info['zip'], '99009')
    self.assertEqual(info['school'], 'Lynnwood High School')
    self.assertEqual(info['district'], 'Edmonds School District')
    self.assertEqual(info['interest'], 'Computer Science')
    self.assertEqual(info['assessment'], 'blacksmith')
    self.assertEqual(info['preferred_method'], 'Email')
    self.assertEqual(info['gender'], 'Cisgender Male')
    self.assertEqual(info['sexual_orientation'], 'Asexual')
    self.assertEqual(info['ethnicity'], 'Asian')
    self.assertEqual(info['notes'], 'gotta blast')

    #delete person that was added.
    tables.deleteStudent(info['id'])
    """

  
  def test_create_clones(self):
    i=0
    self.client.login(username='michael', password='kilgore')
    while i != 50:
      last_name = 'trooper '+str(i)
      response = self.client.post("/student/create/", data={
          'first_name': 'clone',
          'last_name': last_name,
          'email': 'clone.trooper@gmail.com',
          'phone_number': '555-555-5555',
          'address': '99th St SW',
          'apartment': '16B',
          'city': 'Lynnwood',
          'zip': '99009',
          'school': 'Lynnwood High School',
          'grade': '11',
          'interest': 'Computer Science',
          'assessment': 'blacksmith',
          'preferred_method': 'Email',
          'gender': 'Cisgender Male',
          'sexual_orientation': 'Asexual',
          'ethnicity': 'Asian',
          'notes': 'gotta blast'
        }, follow=True)
      i += 1

  



  
  
