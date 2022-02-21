import boto3
from boto3.dynamodb.conditions import Key
import asyncio
from boto3.dynamodb.conditions import Attr
from datetime import date
from wkit.var import cities, schools, assessments, school_districts



class Paginator:
  def __init__(self, table_name, page_size, kwargs={}, pages={}):
    self.table_name = table_name
    self.page_size = page_size
    self.kwargs = kwargs
    if pages != {}:
      self.pages = pages
    else:
      self.pages = []

  def getPage(self, page_num):
    if page_num >= len(self.pages):
      self.advanceToPage(page_num)

    return self.pages[page_num]['Items'] if self.existsPage(page_num) else None

  def existsPage(self, page_num):
    self.advanceToPage(page_num)
    return len(self.pages) >= page_num

  def advanceToPage(self, page_num):
    while (page_num >= len(self.pages)):
      if len(self.pages) == 0:
        self.pages.append(self.nextPage(None))
      else:
        token = self.pages[-1]['LastEvaluatedKey']
        if not token:
          return
        self.pages.append(self.nextPage(token))

  def nextPage(self, token):
    print(f"loading page {len(self.pages)}: {token}")
    kwargs = self.kwargs.copy()
    kwargs['Limit'] = self.page_size
    if token:
      kwargs['ExclusiveStartKey'] = token
    #  rsp = self.table.scan(**kwargs)
    #    Limit=self.page_size,
    #    ExclusiveStartKey=token,
    #  )
    #else:
    #  rsp = self.table.scan(Limit=self.page_size)
    dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
    table = dynamodb.Table(self.table_name)

    rsp = table.scan(**kwargs)
    #rsp = self.aws_pag.paginate(
    #  TableName=self.table_name,
    #  PaginationConfig = {
    #    'MaxItems': self.page_size,
    #    'PageSize': self.page_size,
    #    # 'StartingToken': token,
    #  },
    #)
    return rsp


def getInterests():
  dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
  table = dynamodb.Table('wkit_interest_table')
  vals = table.scan()

  strings = vals['Items']
  return strings

async def insertStudent(student, id):
  dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
  table = dynamodb.Table('wkit_student_table')

  today = str(date.today())
  if student['grade'] == '12':
    x = today.split('-')
    x[0] = str(int(int(x[0]) - 1))
    today = ""
    for val in x:
      today = today + val + "-"
    today = today[:-1]

  interests = ""
  if len(student.getlist('interest')) == 1:
    interests = student['interest']
  else:
    for val in student.getlist('interest'):
      interests += val + ', '
    interests = interests[:-2]

  response = table.put_item(
    Item={
      'id': id,
      'email': student['email'],
      'phone_number': student['phone_number'],
      'last_name': student['last_name'],
      'first_name': student['first_name'],
      'address': student['address'],
      'apartment': student['apartment'],
      'city': student['city'],
      'zip': student['zip'],
      'school': student['school'],
      'district': school_districts[student['school']],
      'grade': today,
      'interest': interests,
      'assessment': student['assessment'],
      'preferred_method': student['preferred_method'],
      'gender': student['gender'],
      'ethnicity': student['ethnicity'],
      'notes': student['notes']
    }
  )
  return response

def deleteStudent(id):
  dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
  table = dynamodb.Table('wkit_student_table')

  response = table.delete_item(
    Key={
      'id': id
    }
  )

def getStudent(id):
  dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
  table = dynamodb.Table('wkit_student_table')
  
  response = table.query(
    KeyConditionExpression=Key('id').eq(id)
  )

  if len(response['Items']) == 1:
    return response['Items'][0] 
  else:
    return {}

async def updateStudent(id, student):
  dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
  table = dynamodb.Table('wkit_student_table')

  #is mentor removed
  if 'mentor_id' in student and student['delete_mentor'] != 'delete_mentor':
    pass
  else:
    student['mentor_id'] = ""


  #get array of scholarship ids to be deleted
  deleted_scholarships = []
  if 'deleted_scholarships' in student:
    if len(student.getlist('deleted_scholarships')) == 1:
      deleted_scholarships = [student['deleted_scholarships']]
    else:
      for val in student.getlist('deleted_scholarships'):
        deleted_scholarships.append(val)


  #final set of new scholarships
  h = {}
  for val in deleted_scholarships:
    h[val] = True

  new_scholarships = []
  for val in student.getlist('scholarships'):
    if val not in h: 
      new_scholarships.append(val)
  
  #setting new time.
  today = str(date.today())
  if student['grade'] == '12':
    x = today.split('-')
    x[0] = str(int(int(x[0]) - 1))
    today = ""
    for val in x:
      today = today + val + "-"
    today = today[:-1]
  elif student['grade'] == 'Graduated':
    x = today.split('-')
    x[0] = str(int(int(x[0]) - 5))
    today = ""
    for val in x:
      today = today + val + "-"
    today = today[:-1]


  #setting interests
  interests = ""
  if len(student.getlist('interest')) == 1:
    interests = student['interest']
  else:
    for val in student.getlist('interest'):
      interests += val + ', '
    interests = interests[:-2]


  #sending update response
  response = table.update_item(
    Key={
      'id': id
    },
    UpdateExpression="set email=:a, phone_number=:b, last_name=:c, first_name=:d, address=:e, apartment=:f, city=:g, zip=:h, school=:i, district=:j, grade=:k, interest=:l, assessment=:m, preferred_method=:n, gender=:o, ethnicity=:p, notes=:q, mentor_id=:r, scholarships=:s",
    ExpressionAttributeValues={
      ':a': student['email'],
      ':b': student['phone_number'],
      ':c': student['last_name'],
      ':d': student['first_name'],
      ':e': student['address'],
      ':f': student['apartment'],
      ':g': student['city'],
      ':h': student['zip'],
      ':i': student['school'],
      ':j': school_districts[student['school']],  
      ':k': today,
      ':l': interests,
      ':m': student['assessment'],
      ':n': student['preferred_method'],
      ':o': student['gender'],
      ':p': student['ethnicity'], 
      ':q': student['notes'],
      ':r': student['mentor_id'],
      ':s': new_scholarships
    },
    ReturnValues="UPDATED_NEW"
  )

  return response

def getAllStudents():
  dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
  table = dynamodb.Table('wkit_student_table')

  resp = table.scan()

  return resp['Items']

def queryStudents(search_type, search_entry):
  print(f"search on {search_entry}")

  if search_type == 0: #search by email
    return Paginator('wkit_student_table', 10, {
      'IndexName': 'email-index',
      'FilterExpression': Attr('email').contains(search_entry),
    })
  elif search_type == 1: #search by phone number
    return Paginator('wkit_student_table', 10, {
      'IndexName': 'phone_number-index',
      'FilterExpression': Attr('phone_number').contains(search_entry),
    })
  else: #full scan
    return Paginator('wkit_student_table', 10)

async def convertStudent(id):
  #get student info
  dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
  table = dynamodb.Table('wkit_student_table')
  mentor_table = dynamodb.Table('wkit_mentor_table')
  
  response = table.query(
    KeyConditionExpression=Key('id').eq(id)
  )

  mentor = {}
  if len(response['Items']) == 1:
    mentor = response['Items'][0]
  else:
    return

  #create mentor with student info
  
  response = mentor_table.put_item(
    Item={
      'id': id,
      'email': mentor['email'],
      'phone_number': mentor['phone_number'],
      'last_name': mentor['last_name'],
      'first_name': mentor['first_name'],
      'address': mentor['address'],
      'apartment': mentor['apartment'],
      'city': mentor['city'],
      'zip': mentor['zip'],
      'interest': mentor['interest'],
      'job_title': '',
      'is_volunteer': 'Yes',
      'preferred_method': mentor['preferred_method'],
      'gender': mentor['gender'],
      'ethnicity': mentor['ethnicity'],
      'background_check': 'Not Started',
      'notes': mentor['notes']
    }
  )

  #delete student info.
  response = table.delete_item(
    Key={
      'id': id
    }
  )


#pair mentor
async def pairMentor(id, mentor_id):
  dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
  table = dynamodb.Table('wkit_student_table')

  response = table.update_item(
    Key={
      'id': id
    },
    UpdateExpression="set mentor_id=:a",
    ExpressionAttributeValues={
      ':a': mentor_id,
    },
    ReturnValues="UPDATED_NEW"
  )

  return response

def appendScholarship(id, allScholarships):
  dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
  table = dynamodb.Table('wkit_student_table')
  
  response = table.update_item(
    Key={
      'id': id
    },
    UpdateExpression="set scholarships=:a",
    ExpressionAttributeValues={
      ':a': allScholarships,
    },
    ReturnValues="UPDATED_NEW"
  )
  
  return response



###############     MENTOR       ######################

async def insertMentor(mentor, id):
  dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
  table = dynamodb.Table('wkit_mentor_table')

  interests = ""
  if len(mentor.getlist('interest')) == 1:
    interests = mentor['interest']
  else:
    for val in mentor.getlist('interest'):
      interests += val + ', '
    interests = interests[:-2]

  response = table.put_item(
    Item={
      'id': id,
      'email': mentor['email'],
      'phone_number': mentor['phone_number'],
      'last_name': mentor['last_name'],
      'first_name': mentor['first_name'],
      'address': mentor['address'],
      'apartment': mentor['apartment'],
      'city': mentor['city'],
      'zip': mentor['zip'],
      'interest': interests,
      'job_title': mentor['job_title'],
      'is_volunteer': mentor['is_volunteer'],
      'preferred_method': mentor['preferred_method'],
      'gender': mentor['gender'],
      'ethnicity': mentor['ethnicity'],
      'background_check': mentor['background_check'],
      'notes': mentor['notes']
    }
  )
  return response

def getMentor(id):
  dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
  table = dynamodb.Table('wkit_mentor_table')
  
  response = table.query(
    KeyConditionExpression=Key('id').eq(id)
  )

  if len(response['Items']) == 1:
    return response['Items'][0] 
  else:
    return {}



def queryMentors(search_type, search_entry):
  dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
  table = dynamodb.Table('wkit_mentor_table')
  print(f"search mentors on {search_entry}")

  if search_type == 0: #search by email
    return Paginator('wkit_mentor_table', 10, {
      'IndexName': 'email-index',
      'FilterExpression': Attr('email').contains(search_entry),
    })
  elif search_type == 1: #search by phone number
    return Paginator('wkit_mentor_table', 10, {
      'IndexName': 'phone_number-index',
      'FilterExpression': Attr('phone_number').contains(search_entry),
    })
  else: #full scan
    return Paginator('wkit_mentor_table', 10)

def deleteMentor(id):
  dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
  table = dynamodb.Table('wkit_mentor_table')
  response = table.delete_item(
    Key={
      'id': id
    }
  )


async def updateMentor(id, mentor):
  dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
  table = dynamodb.Table('wkit_mentor_table')

  #get array of student ids to be deleted
  deleted_students = []
  if 'deleted_students' in mentor:
    if len(mentor.getlist('deleted_students')) == 1:
      deleted_students = [mentor['deleted_students']]
    else:
      for val in student.getlist('deleted_students'):
        deleted_students.append(val)

  print('the students are: ', deleted_students)

  #UNPAIR THE STUDENT FROM THIS MENTOR
  for student in deleted_students:
    await pairMentor(student, "")

  #setting interests
  interests = ""
  if len(mentor.getlist('interest')) == 1:
    interests = mentor['interest']
  else:
    counter = 0
    for val in mentor.getlist('interest'):
      counter += 1
      interests += val + ', '
      if counter == 5:
        break
    interests = interests[:-2]

  #sending update response
  response = table.update_item(
    Key={
      'id': id
    },
    UpdateExpression="set email=:a, phone_number=:b, last_name=:c, first_name=:d, address=:e, apartment=:f, city=:g, zip=:h, interest=:i, preferred_method=:j, gender=:k, ethnicity=:l, notes=:m",
    ExpressionAttributeValues={
      ':a': mentor['email'],
      ':b': mentor['phone_number'],
      ':c': mentor['last_name'],
      ':d': mentor['first_name'],
      ':e': mentor['address'],
      ':f': mentor['apartment'],
      ':g': mentor['city'],
      ':h': mentor['zip'],
      ':i': interests,
      ':j': mentor['preferred_method'],  
      ':k': mentor['gender'],
      ':l': mentor['ethnicity'],
      ':m': mentor['notes'],
    },
    ReturnValues="UPDATED_NEW"
  )

  return response

def appendStudent(id, allStudents):
  dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
  table = dynamodb.Table('wkit_mentor_table')
  
  response = table.update_item(
    Key={
      'id': id
    },
    UpdateExpression="set students=:a",
    ExpressionAttributeValues={
      ':a': allStudents,
    },
    ReturnValues="UPDATED_NEW"
  )
  
  return response

#TODO: DEFINATELY NEED AN INDEX ON MENTOR_ID
def getStudents(id):
  dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
  table = dynamodb.Table('wkit_student_table')
  
  response = table.scan()
 
  ans = []

  for user in response['Items']:
    if 'mentor_id' in user:
      if user['mentor_id'] == id:
        ans.append(user)

  print('the students are: ', ans)

  return ans

######################## PROGRAM ########################

def getOrganizations():
  dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
  table = dynamodb.Table('wkit_organization_table')

  resp = table.scan()
  return resp['Items']

async def insertProgram(program, id):
  dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
  table = dynamodb.Table('wkit_program_table')

  response = table.put_item(
    Item={
      'id': id,
      'program_name': program['program_name'],
      'organizationID': program['organizationID'],
      'phone_number': program['phone_number'],
      'email': program['email'],
      'interest': program['interest'],
      'time_commitment': program['time_commitment'],
      'program_duration': program['program_duration'],
      'application_deadlines': program['application_deadlines'],
      'start_dates': program['start_dates'],
      'notes': program['notes'],
    }
  )
  return response

def getProgram(id):
  dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
  table = dynamodb.Table('wkit_program_table')
  
  response = table.query(
    KeyConditionExpression=Key('id').eq(id)
  )


  if len(response['Items']) == 1:
    return response['Items'][0] 
  else:
    return {}

def scanPrograms():
  dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
  table = dynamodb.Table('wkit_program_table')

  resp = table.scan()

  return resp['Items']

# time commitments are stored in dynamodb as strings that are either:
#   greater than 40 hrs/week
#   ~40 hrs/week 
#   ~20 hrs/week
#   ~30 hrs/week
#   ~10 hrs/week
#   ~5 hrs/week
#   less than 5 hrs/week

#   this needs to search based off of the inputs given in queryPrograms
def queryPrograms(search_name: str, city: [str], interest: [str], time_commitment: int):
  """if search_type == 0: #search by email
    return Paginator('wkit_student_table', 10, {
      'IndexName': 'email-index',
      'FilterExpression': Attr('email').contains(search_entry),
    })
  elif search_type == 1: #search by phone number
    return Paginator('wkit_student_table', 10, {
      'IndexName': 'phone_number-index',
      'FilterExpression': Attr('phone_number').contains(search_entry),
    })
  else: #full scan
    return Paginator('wkit_student_table', 10)"""

  pass




#################### ORGANIZATION ###################

async def insertOrganization(organization, id):
  dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
  table = dynamodb.Table('wkit_organization_table')

  response = table.put_item(
    Item={
      'id': id,
      'name': organization['name'],
      'type': organization['type'],
      'address': organization['address'],
      'city': organization['city'],
      'zip': organization['zip'],
      'notes': organization['notes']
    }
  )
  return response

def getOrganization(id):
  dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
  table = dynamodb.Table('wkit_organization_table')
  
  response = table.query(
    KeyConditionExpression=Key('id').eq(id)
  )

  if len(response['Items']) == 1:
    return response['Items'][0] 
  else:
    return {}

def queryOrganizations(search_type, search_entry):
  dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
  table = dynamodb.Table('wkit_organization_table')

  if search_type == 0: #search by name
    resp = table.query(
      IndexName='name-index',
      KeyConditionExpression=Key('name').eq(search_entry)
    )
    return resp['Items']
  elif search_type == 1: #search by city
    resp = table.query(
      IndexName='city-index',
      KeyConditionExpression=Key('city').eq(search_entry)
    )
    return resp['Items']
  else: #full scan
    resp = table.scan()
    return resp['Items']

def updateOrganization(id, organization):
  dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
  table = dynamodb.Table('wkit_organization_table')

  response = table.update_item(
    Key={
      'id': id
    },
    UpdateExpression="set organization_name=:a, organization_type=:b, address=:c, city=:d, zip=:e, notes=:f",
    ExpressionAttributeValues={
      ':a': organization['organization_name'],
      ':b': organization['organization_type'],
      ':c': organization['address'],
      ':d': organization['city'],
      ':e': organization['zip'],
      ':f': organization['notes']
    },
    ReturnValues="UPDATED_NEW"
  )

  return response


def deleteOrganization(id):
  dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
  table = dynamodb.Table('wkit_organization_table')
  response = table.delete_item(
    Key={
      'id': id
    }
  )



###################### INTERESTS #############

async def insertInterest(interest):
  dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
  table = dynamodb.Table('wkit_interest_table')

  response = table.put_item(
    Item={
      'interest': interest
    }
  )
  return response


def queryInterests(interest):
  """dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
  table = dynamodb.Table('wkit_interest_table')"""
  
  if (interest != ""):
    """response = table.query(
      KeyConditionExpression=Key('interest').eq(interest)
    )
    
    return response['Items']"""

    return Paginator('wkit_interest_table', 10, {
      'FilterExpression': Attr('interest').contains(interest),
    })
  else:
    return Paginator('wkit_interest_table', 10)

def deleteInterest(interest):
  dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
  table = dynamodb.Table('wkit_interest_table')
  response = table.delete_item(
    Key={
      'interest': interest
    }
  )

#################################### SCHOLARSHIP ###################
async def insertScholarship(scholarship, id):
  dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
  table = dynamodb.Table('wkit_scholarship_table')

  response = table.put_item(
    Item={
      'id': id,
      'scholarship_name': scholarship['scholarship_name'],
      'amount': int(scholarship['amount']),
      'type': scholarship['type'],
      'notes': scholarship['notes']
    }
  )
  return response

def queryScholarships(id, name, min_amount, max_amount, scholarship_type):
  dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
  table = dynamodb.Table('wkit_scholarship_table')


  # get off limit keys  
  off_limits = {}
  if id != 'foo':
    student = getStudent(id)
    if 'scholarships' in student: 
      for key in student['scholarships']:
        off_limits[key] = True

  if name == "" and min_amount == "" and max_amount == "" and scholarship_type=='no_preference':
    response = table.scan()

    ans = response['Items']
    return_ans = []

    for item in ans:
      if item['id'] not in off_limits:
        return_ans.append(item)
    
    return return_ans
  else:
    if min_amount == "":
      min_amount = "0"
    if max_amount == "":
      max_amount = "999999999999999999"

    ans = {}
    if scholarship_type=='no_preference': #just by name
      resp = table.scan()
  
      for val in resp['Items']:
        if val['amount'] <= int(max_amount) and val['amount'] >= int(min_amount):
          if val['name'] == name:
            ans.append(val)

      return_ans = []

      for item in ans:
        if item['id'] not in off_limits:
          return_ans.append(item)
      
      return return_ans
    elif name=="": #just by type
      resp = table.scan()

      if val['amount'] <= int(max_amount) and val['amount'] >= int(min_amount):
        if val['type'] == scholarship_type:
          ans.append(val)

      return_ans = []

      for item in ans:
        if item['id'] not in off_limits:
          return_ans.append(item)
      
      return return_ans
    else: #both
      if val['amount'] <= int(max_amount) and val['amount'] >= int(min_amount):
        if val['type'] == scholarship_type and val['name'] == name:
          ans.append(val)

      return_ans = []

      for item in ans:
        if item['id'] not in off_limits:
          return_ans.append(item)
  
      return return_ans
  
def deleteScholarship(id):
  dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
  response = table.delete_item(
    Key={
      'id': id
    }
  )

def getScholarships(id):
  dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
  table = dynamodb.Table('wkit_student_table')
  
  response = table.query(
    KeyConditionExpression=Key('id').eq(id)
  )

  user = {}
  if len(response['Items']) == 1:
    user = response['Items'][0] 
  else:
    user = {}

  if 'scholarships' in user:
    #dynamodb = boto3.resource('dynamodb')
    dynamodb = boto3.resource("dynamodb", region_name='us-west-2')

    list_of_keys = []
    for key in user['scholarships']:
      list_of_keys.append({'id': key})  

    batch_keys = {
      'wkit_scholarship_table': {
        'Keys': list_of_keys
      }
    }

    response = dynamodb.batch_get_item(RequestItems=batch_keys)

    return response['Responses']['wkit_scholarship_table']
  else:
    return []
    
def updateScholarships(id, scholarships):
  dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
  table = dynamodb.Table('wkit_student_table')
  
  response = table.update_item(
    Key={
      'id': id
    },
    UpdateExpression="set scholarships=:a",
    ExpressionAttributeValues={
      ':a': scholarships,
    },
    ReturnValues="UPDATED_NEW"
  )

  return response

def getScholarship(id):
  dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
  table = dynamodb.Table('wkit_scholarship_table')
  
  response = table.query(
    KeyConditionExpression=Key('id').eq(id)
  )

  if len(response['Items']) == 1:
    return response['Items'][0] 
  else:
    return {}

def updateScholarship(id, scholarship):
  dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
  table = dynamodb.Table('wkit_scholarship_table')

  response = table.update_item(
    Key={
      'id': id
    },
    UpdateExpression="set scholarship_name=:a, amount=:b, scholarship_type=:c, notes=:d",
    ExpressionAttributeValues={
      ':a': scholarship['scholarship_name'],
      ':b': int(scholarship['amount']),
      ':c': scholarship['scholarship_type'],
      ':d': scholarship['notes']
    },
    ReturnValues="UPDATED_NEW"
  )

  return response

def updateCSV():
  import csv

  with open('file.csv', 'w', encoding='UTF8') as f:
    writer = csv.writer(f)

    writer.writerow(['id','first name', 'last name', 'email', 'phone number', 'address', 'apartment', 'city', 'zip', 'school', 'district', 'grade', 'field(s) of interest', 'assessment result', 'preferred method of contact', 'gender', 'ethnicity', 'notes', 'money given', 'money won', 'number of scholarships'])

    dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
    table = dynamodb.Table('wkit_student_table')

    students = table.scan()['Items']

    #for student in students:
      #writer.writerow(0)


 
    dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
    table = dynamodb.Table('wkit_mentor_table')
 
    dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
    table = dynamodb.Table('wkit_program_table')

    dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
    table = dynamodb.Table('wkit_organization_table')

    dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
    table = dynamodb.Table('wkit_interest_table')

    dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
    table = dynamodb.Table('wkit_scholarship_table')

    writer.writerow(row)
  










