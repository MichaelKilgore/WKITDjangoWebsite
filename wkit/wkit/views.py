from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
import asyncio
import uuid
import datetime
from django.http import HttpResponse
from django.http import JsonResponse
import json
import jsonpickle

from wkit.var import cities, schools, assessments, school_districts
import wkit.tables as tables

login_url = '/account/login/'

@login_required(login_url = login_url)
def index(request):
  return render(request, 'wkit/index.html', {})

@login_required(login_url = login_url)
def createStudent(request):
  if request.user.is_authenticated:
    if request.method == 'POST':
      loop = asyncio.new_event_loop()
      asyncio.set_event_loop(loop)
      loop = asyncio.get_event_loop()
      x = uuid.uuid4().hex
      loop.run_until_complete(tables.insertStudent(request.POST, x))
      loop.close()

      z, z['student'] = {}, request.POST

      return redirect('/student/profile/'+x, newProfile=z)
    else:
      h, h['cities'], h['schools'], h['assessments'], h['interests'] = {}, cities, schools, assessments, tables.getInterests()
      return render(request, 'wkit/Students/createStudent.html', h)
  else:
    return HttpResponseRedirect('/')


def nextOrPrevPage(request, items_label, direction, pagname = "paginator"):
  paginator = jsonpickle.decode(request.session[pagname])
  model_current_page = int(request.POST['current_page']) - 1
  pageToGet = model_current_page + 1 if direction == 'forward' else model_current_page - 1
  if pageToGet < 0 or not paginator.existsPage(pageToGet):
    print(f"FAIL - no page {pageToGet} - why was button enabled?")
    return JsonResponse({})
  else:
    data = paginator.getPage(pageToGet, items_label)
    request.session[pagname] = jsonpickle.encode(paginator)
    return JsonResponse(data)

def doSimpleSearch(request, fetch_func, items_label, uri):
  print(f"request = {request}: request.POST={request.POST}")
  if request.method == 'GET':
    paginator = fetch_func('full_scan', None)
    data = paginator.getPage(0, items_label)
    request.session['paginator'] = jsonpickle.encode(paginator)
    return render(request, uri, data)
  else:
    if 'search_type' in request.POST:
      search_type = request.POST['search_type']
      paginator = fetch_func(search_type, request.POST['search_entry'])
      data = paginator.getPage(0, items_label)
      request.session['paginator'] = jsonpickle.encode(paginator)
      return render(request, uri, data)
    elif 'action' in request.POST and request.POST['action'] == 'next_page':
      return nextOrPrevPage(request, items_label, 'forward')

    elif 'action' in request.POST and request.POST['action'] == 'prev_page':
      return nextOrPrevPage(request, items_label, 'backward')
    elif 'delete' in request.POST:
      tables.deleteInterest(request.POST['interest'])
      paginator = fetch_func('full_scan', None)
      data = paginator.getPage(0, items_label)
      request.session['paginator'] = jsonpickle.encode(paginator)
      return render(request, uri, data)
    else:
      return JsonResponse({})

@login_required(login_url = login_url)
def searchStudent(request, key=None):
  return doSimpleSearch(request, tables.queryStudents, "students", 'wkit/Students/searchStudent.html')


@login_required(login_url = login_url)
def updateStudent(request):
  if request.method == 'POST':
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(tables.updateStudent(int(request.POST['studentID']), request.data))
    loop.close()

    return redirect('/student/profile/'+request.POST['studentID'])

@login_required(login_url = login_url)
def studentProfile(request, id):
  if request.method == 'GET':
    h = {}
    h, h['cities'], h['schools'], h['assessments'], h['interests'] = {}, cities, schools, assessments, tables.getInterests()
    h['student'] = tables.getStudent(id)
    if 'mentor_id' in h['student']:
      if h['student']['mentor_id'] != "":
          x = tables.getMentor(h['student']['mentor_id'])
          h['student']['mentor_name'] = x['first_name'] + " " + x['last_name']
    if 'scholarships' in h['student']:
      if len(h['student']['scholarships']) != 0:
        h['student']['scholarships'] = tables.getScholarships(id)
    else:
      h['student']['scholarships'] = []

    #find next june 21st.
    today = datetime.date.today()
    comparison = ""
    x = str(today).split("-")
    if int(x[1]) <= 6:
      comparison = str(x[0] + '-' + '06' + '-' + '30')
    else:
      comparison = str(str(int(x[0]) + 1) + '-' + '06' + '-' + '30')

    """
    dt = datetime.datetime.strptime(h['student']['grade'], '%Y-%m-%d').date()

    comparison = datetime.datetime.strptime(comparison, '%Y-%m-%d').date()

    difference = comparison - dt

    days = int(difference.days)

    if days < 365:
      h['student']['grade'] = '11'
    elif days < 730:
      h['student']['grade'] = '12'
    else:
      h['student']['grade'] = 'Graduated'
    """

    h['student']['district'] = school_districts[h['student']['school']]

    return render(request, 'wkit/Students/studentProfile.html', h)
  else:
    print('recognized post: ', request.POST)
    if 'first_name' in request.POST: #edit mode
      loop = asyncio.new_event_loop()
      asyncio.set_event_loop(loop)
      loop = asyncio.get_event_loop()
      student_info = request.POST.copy()
      loop.run_until_complete(tables.updateStudent(request.POST['id'], student_info))

      loop.close()

      z, z['student'] = {}, request.POST

      return redirect('/student/profile/'+z['student']['id'], newProfile=z)
    elif 'convert_to_mentor' in request.POST: #convert to mentor
      loop = asyncio.new_event_loop()
      asyncio.set_event_loop(loop)
      loop = asyncio.get_event_loop()
      loop.run_until_complete(tables.convertStudent(request.POST['id']))
      loop.close()

      return HttpResponse(status=204)
    elif 'delete' in request.POST: #delete user
      loop = asyncio.new_event_loop()
      asyncio.set_event_loop(loop)
      loop = asyncio.get_event_loop()
      loop.run_until_complete(tables.deleteStudent(request.POST['id']))
      loop.close()

      return HttpResponse(status=204)
    elif 'get_mentors' in request.POST: #search for mentors
      label = "mentors"
      if request.POST['search_entry'] != "":
        search_type = request.POST['search_type']
        paginator = tables.queryMentors(search_type, request.POST['search_entry'], 10)
        data = paginator.getPage(0, label)
        request.session['mentor_paginator'] = jsonpickle.encode(paginator)
        return JsonResponse(data)
      else:
        paginator = tables.queryMentors('full_scan', request.POST['search_entry'], 10)
        data = paginator.getPage(0, label)
        request.session['mentor_paginator'] = jsonpickle.encode(paginator)
        return JsonResponse(data)
      request.session['mentor_paginator'] = paginator
    elif 'pair_mentor' in request.POST: #pair mentor to user
      loop = asyncio.new_event_loop()
      asyncio.set_event_loop(loop)
      loop = asyncio.get_event_loop()
      loop.run_until_complete(tables.pairMentor(request.POST['id'], request.POST['mentor_id']))
      loop.close()

      return HttpResponse(status=204)
    elif 'get_scholarships' in request.POST: #search for scholarships
      paginator = tables.queryScholarships(request.POST['id'], request.POST['name'], request.POST['min_amount'], request.POST['max_amount'], request.POST['type'])
      allScholarships, allScholarships['scholarships'] = {}, paginator.getPage(0)
      request.session['mentor_paginator'] = json.dumps(vars(paginator))
      return JsonResponse(allScholarships)
    elif 'pair_scholarship' in request.POST: #pair scholarship to user
      #query for old list of scholarships 
      user = tables.getStudent(request.POST['id'])
      #allScholarships = tables.getScholarships(request.POST('id'))           
  
      allScholarships = []
      checker = {}
      if 'scholarships' in user:  
        allScholarships = user['scholarships']

      for key in allScholarships:
        if request.POST['scholarship_id'] in checker:
          break
        checker[key] = True
      else:
        #add given scholarship to list of scholarships and update
        allScholarships.append(request.POST['scholarship_id']);
        tables.appendScholarship(request.POST['id'], allScholarships)

      return HttpResponse(status=204)
    elif 'action' in request.POST and request.POST['action'] == 'next_page':
      return nextOrPrevPage(request, "mentors", "forward", "mentor_paginator")

    elif 'action' in request.POST and request.POST['action'] == 'prev_page':
      return nextOrPrevPage(request, "mentors", "backward", "mentor_paginator")

    elif 'program' in request.POST and 'next_page' in request.POST:
      paginator_dict = json.loads(request.session['program_paginator'])
      paginator = tables.Paginator(**paginator_dict)
      allPrograms, allPrograms['programs'] = {}, paginator.getPage(int(request.POST['next_page'])+1)
      return JsonResponse(allPrograms)
    elif 'program' in request.POST and 'last_page' in request.POST:
      paginator_dict = json.loads(request.session['program_paginator'])
      paginator = tables.Paginator(**paginator_dict)
      if (int(request.POST['last_page'])-1 >= 0):
        allPrograms, allPrograms['programs'] = {}, paginator.getPage(int(request.POST['last_page'])-1)
        return JsonResponse(allPrograms)
      return JsonResponse({})
    elif 'scholarship' in request.POST and 'next_page' in request.POST:
      paginator_dict = json.loads(request.session['scholarship_paginator'])
      paginator = tables.Paginator(**paginator_dict)
      allScholarships, allScholarships['scholarships'] = {}, paginator.getPage(int(request.POST['next_page'])+1)
      return JsonResponse(allScholarships)
    elif 'scholarship' in request.POST and 'last_page' in request.POST:
      paginator_dict = json.loads(request.session['scholarship_paginator'])
      paginator = tables.Paginator(**paginator_dict)
      if (int(request.POST['last_page'])-1 >= 0):
        allScholarships, allScholarships['scholarships'] = {}, paginator.getPage(int(request.POST['last_page'])-1)
        return JsonResponse(allScholarships)
      return JsonResponse({})
    else:
      return JsonResponse({})




@login_required(login_url = login_url)
def createMentor(request):
  if request.user.is_authenticated:
    if request.method == 'POST':
      loop = asyncio.new_event_loop()
      asyncio.set_event_loop(loop)
      loop = asyncio.get_event_loop()
      x = uuid.uuid4().hex
      loop.run_until_complete(tables.insertMentor(request.POST, x))
      loop.close()

      z, z['mentor'] = {}, request.POST

      return redirect('/mentor/profile/'+x, newProfile=z)
    else:
      h, h['cities'], h['schools'], h['assessments'], h['interests'] = {}, cities, schools, assessments, tables.getInterests()
      return render(request, 'wkit/Mentors/createMentor.html', h)
  else:
    return HttpResponseRedirect('/')



@login_required(login_url = login_url)
def searchMentor(request, key=None):
  return doSimpleSearch(request, tables.queryMentors, "mentors", 'wkit/Mentors/searchMentor.html')


@login_required(login_url = login_url)
def mentorProfile(request, id):
  if request.method == 'GET':
    h = {}
    h, h['cities'], h['schools'], h['assessments'], h['interests'] = {}, cities, schools, assessments, tables.getInterests()
    h['mentor'] = tables.getMentor(id)
    h['mentor']['students'] = tables.getStudents(id) 

    return render(request, 'wkit/Mentors/mentorProfile.html', h)
  else:
    if 'first_name' in request.POST: #edit mode
      loop = asyncio.new_event_loop()
      asyncio.set_event_loop(loop)
      loop = asyncio.get_event_loop()
      loop.run_until_complete(tables.updateMentor(request.POST['id'], request.POST))

      loop.close()

      z, z['mentor'] = {}, request.POST

      return redirect('/mentor/profile/'+z['mentor']['id'], newProfile=z)
    elif 'delete' in request.POST: #delete user
      loop = asyncio.new_event_loop()
      asyncio.set_event_loop(loop)
      loop = asyncio.get_event_loop()
      loop.run_until_complete(tables.deleteMentor(request.POST['id']))
      loop.close()
    elif 'get_students' in request.POST: #search students
      if request.POST['search_entry'] != "":
        if request.POST['search_type'] == 'email':
          paginator = tables.queryStudents(0, request.POST['search_entry'])
          allStudents, allStudents['students'] = {}, paginator.getPage(0)
          request.session['paginator'] = json.dumps(vars(paginator))
          return JsonResponse(allStudents)
        elif request.POST['search_type'] == 'phone_number':
          paginator = tables.queryStudents(1, request.POST['search_entry'])
          allStudents, allStudents['students'] = {}, paginator.getPage(0)
          request.session['paginator'] = json.dumps(vars(paginator))
          return JsonResponse(allStudents)
        else:
          paginator = tables.queryStudents(2, request.POST['search_entry'])
          allStudents, allStudents['students'] = {}, paginator.getPage(0)
          request.session['paginator'] = json.dumps(vars(paginator))
          return JsonResponse(allStudents)
      else:
        if request.POST['search_type'] != 'full_scan':
          return JsonResponse({})
        else:
          paginator = tables.queryStudents(2, request.POST['search_entry'])
          allStudents, allStudents['students'] = {}, paginator.getPage(0)
          request.session['paginator'] = json.dumps(vars(paginator))
          return JsonResponse(allStudents)
      request.session['paginator'] = paginator
    elif 'pair_student' in request.POST: #pair student to user
      user = tables.getMentor(request.POST['id'])

      allStudents = []
      checker = {}

      if 'students' in user:  
        allStudents = user['students']

      for key in allStudents:
        if request.POST['student_id'] in checker:
          break
        checker[key] = True
      else:
        allStudents.append(request.POST['student_id']);
        tables.appendStudent(request.POST['id'], allStudents)

      return HttpResponse(status=204)
    elif 'next_page' in request.POST:
      paginator_dict = json.loads(request.session['paginator'])
      paginator = tables.Paginator(**paginator_dict)
      allStudents, allStudents['students'] = {}, paginator.getPage(int(request.POST['next_page'])+1)
      return JsonResponse(allStudents)
    elif 'last_page' in request.POST:
      paginator_dict = json.loads(request.session['paginator'])
      paginator = tables.Paginator(**paginator_dict)
      if (int(request.POST['last_page'])-1 >= 0):
        allStudents, allStudents['students'] = {}, paginator.getPage(int(request.POST['last_page'])-1)
        return JsonResponse(allStudents)
      return JsonResponse({})
    else:
      return JsonResponse({})






@login_required(login_url = login_url)
def createProgram(request):
  if request.user.is_authenticated:
    if request.method == 'POST':
      loop = asyncio.new_event_loop()
      asyncio.set_event_loop(loop)
      loop = asyncio.get_event_loop()
      x = uuid.uuid4().hex
      loop.run_until_complete(tables.insertProgram(request.POST, x))
      loop.close()

      z, z['program'] = {}, request.POST

      return redirect('/program/profile/'+x, newProfile=z)
    else:
      h, h['organizations'], h['interests'] = {}, tables.getOrganizations(), tables.getInterests()
      return render(request, 'wkit/Programs/createProgram.html', h)
  else:
    return HttpResponseRedirect('/')



@login_required(login_url = login_url)
def searchProgram(request):
  label = 'programs'
  if request.method == 'GET':
    h, h['cities'], h['interests'] = {}, cities, tables.getInterests()
    paginator = tables.scanPrograms()
    h['programs'] = paginator.getPage(0, label)['programs']

    allOrganizations = tables.getOrganizations()
    orgHash = {}

    for org in allOrganizations:
      orgHash[org['id']] = org['city']

    for program in h['programs']:
      if (orgHash[program['organizationID']]):
        program['city'] = orgHash[program['organizationID']]

    print('programs: ', h['programs'])
    request.session['paginator'] = json.dumps(vars(paginator))
    return render(request, 'wkit/Programs/searchProgram.html', h)
  else:
    if 'next_page' in request.POST:
      paginator_dict = json.loads(request.session['paginator'])
      paginator = tables.Paginator(**paginator_dict)
      allPrograms, allPrograms['programs'] = {}, paginator.getPage(int(request.POST['next_page'])+1, label)['programs']

      allOrganizations = tables.getOrganizations()
      orgHash = {}

      for org in allOrganizations:
        orgHash[org['id']] = org['city']

      for program in allPrograms['programs']:
        if (orgHash[program['organizationID']]):
          program['city'] = orgHash[program['organizationID']]

      return JsonResponse(allPrograms)
    elif 'last_page' in request.POST:
      paginator_dict = json.loads(request.session['paginator'])
      paginator = tables.Paginator(**paginator_dict)
      if (int(request.POST['last_page'])-1 >= 0):
        allPrograms, allPrograms['programs'] = {}, paginator.getPage(int(request.POST['last_page'])-1, label)['programs']

        allOrganizations = tables.getOrganizations()
        orgHash = {}

        for org in allOrganizations:
          orgHash[org['id']] = org['city']

        for program in allPrograms['programs']:
          if (orgHash[program['organizationID']]):
            program['city'] = orgHash[program['organizationID']]

        return JsonResponse(allPrograms)

      return JsonResponse({})
    elif request.POST['program_name'] == "" and request.POST['search_duration'] == 'Any' and 'city' not in request.POST and 'interest' not in request.POST:
        allPrograms, allPrograms['programs'] = {}, tables.scanPrograms()
        allPrograms['cities'], allPrograms['interests'] = cities, tables.getInterests()

        allOrganizations = tables.getOrganizations()
        orgHash = {}
  
        for org in allOrganizations:
          orgHash[org['id']] = org['city']

        for program in allPrograms['programs']:
          if (orgHash[program['organizationID']]):
            program['city'] = orgHash[program['organizationID']]
        

        return render(request, 'wkit/Programs/searchProgram.html', allPrograms)
    else:
        allPrograms, allPrograms['programs'] = {}, tables.queryPrograms()
        return render(request, 'wkit/Programs/searchProgram.html', allPrograms)


@login_required(login_url = login_url)
def programProfile(request, id):
  if request.method == 'GET':
    h = {}
    h, h['cities'], h['interests'] = {}, cities, tables.getInterests()
    h['organizations'] = tables.getOrganizations()
    h['program'] = tables.getProgram(id)
    h['organization'] = tables.getOrganization(h['program']['organizationID'])

    return render(request, 'wkit/Programs/programProfile.html', h)
  else:
    if 'first_name' in request.POST: #edit mode
      loop = asyncio.new_event_loop()
      asyncio.set_event_loop(loop)
      loop = asyncio.get_event_loop()
      program_info = request.POST.copy()
      loop.run_until_complete(tables.updateProgram(request.POST['id'], program_info))

      loop.close()

      return redirect('/student/profile/'+z['student']['id'], newProfile={})
    else: #delete
      loop = asyncio.new_event_loop()
      asyncio.set_event_loop(loop)
      loop = asyncio.get_event_loop()
      loop.run_until_complete(tables.deleteMentor(request.POST['id']))
      loop.close()

      return HttpResponse(status=204)


@login_required(login_url = login_url)
def createOrganization(request):
  if request.user.is_authenticated:
    if request.method == 'POST':
      loop = asyncio.new_event_loop()
      asyncio.set_event_loop(loop)
      loop = asyncio.get_event_loop()
      x = uuid.uuid4().hex
      loop.run_until_complete(tables.insertOrganization(request.POST, x))
      loop.close()

      z, z['organization'] = {}, request.POST

      return redirect('/organization/profile/'+x, newProfile=z)
    else:
      h, h['cities'] = {}, cities
      return render(request, 'wkit/Organizations/createOrganization.html', h)
  else:
    return HttpResponseRedirect('/')


@login_required(login_url = login_url)
def searchOrganization(request):
  return doSimpleSearch(request, tables.queryOrganizations, "organizations", 'wkit/Organizations/searchOrganization.html')


@login_required(login_url = login_url)
def organizationProfile(request, id):
  if request.method == 'GET':
    h = {}
    h, h['cities'] = {}, cities
    h['organization'] = tables.getOrganization(id)

    return render(request, 'wkit/Organizations/organizationProfile.html', h)
  else:
    if 'organization_name' in request.POST:
      tables.updateOrganization(request.POST['id'], request.POST)
      z, z['organization'] = {}, request.POST
      return redirect('/organization/profile/'+z['organization']['id'], newProfile=z)
    else: #delete
      tables.deleteOrganization(request.POST['id'])

      return HttpResponse(status=204)


@login_required(login_url = login_url)
def createInterest(request):
  if request.user.is_authenticated:
    if request.method == 'POST':
      loop = asyncio.new_event_loop()
      asyncio.set_event_loop(loop)
      loop = asyncio.get_event_loop()
      print('interest is: ', request.POST['interest'])
      loop.run_until_complete(tables.insertInterest(str(request.POST['interest'])))
      loop.close()

      return redirect('/interest/search/')
    else:
      h= {}
      return render(request, 'wkit/Interests/createInterest.html', h)
  else:
    return HttpResponseRedirect('/')


  return render(request, 'wkit/Interests/createInterest.html', {})



@login_required(login_url = login_url)
def searchInterest(request):
  return doSimpleSearch(request, tables.queryInterests, "interests", 'wkit/Interests/searchInterest.html')


@login_required(login_url = login_url)
def deleteInterest(request):
  print('delete called');
  return redirect('/interest/search/')



@login_required(login_url = login_url)
def createScholarship(request):
  if request.user.is_authenticated:
    if request.method == 'POST':
      loop = asyncio.new_event_loop()
      asyncio.set_event_loop(loop)
      loop = asyncio.get_event_loop()
      x = uuid.uuid4().hex
      loop.run_until_complete(tables.insertScholarship(request.POST, x))
      loop.close()

      return redirect('/scholarship/search/')
    else:
      return render(request, 'wkit/Scholarships/createScholarship.html', {})
  else:
    return HttpResponseRedirect('/')

@login_required(login_url = login_url)
def searchScholarship(request):
  items_label = "scholarships"
  if request.method == 'GET':
    paginator = tables.queryScholarships('foo', None, None, None, None)
    data = paginator.getPage(0, items_label)
    request.session['paginator'] = jsonpickle.encode(paginator)
    return render(request, 'wkit/Scholarships/searchScholarship.html', data)
  elif 'search_type' in request.POST:
      print(f"searching for name={request.POST['name']}")
      paginator = tables.queryScholarships(
        'foo', request.POST['name'], request.POST['min_amount'], request.POST['max_amount'], request.POST['type']
      )
      data = paginator.getPage(0, items_label)
      request.session['paginator'] = jsonpickle.encode(paginator)
      return render(request, 'wkit/Scholarships/searchScholarship.html', data)
  elif 'action' in request.POST and request.POST['action'] == 'next_page':
    return nextOrPrevPage(request, items_label, 'forward')

  elif 'action' in request.POST and request.POST['action'] == 'prev_page':
    return nextOrPrevPage(request, items_label, 'backward')
  else:
    return JsonResponse({})



def scholarshipProfile(request, id):
  if request.method == 'GET':
    h, h['scholarship'] = {}, tables.getScholarship(id)
    return render(request, 'wkit/Scholarships/scholarshipProfile.html', h)
  else:
    if 'amount' in request.POST: #edit
      tables.updateScholarship(request.POST['id'], request.POST)

      z, z['scholarship'] = {}, request.POST

      return redirect('/scholarship/profile/'+z['scholarship']['id'], newProfile=z)
    else: #delete
      tables.deleteScholarship(request.POST['id'])

      return HttpResponse(status=204)


@login_required(login_url = login_url)
def viewGraph(request):
  if request.user.is_authenticated:
    if request.method == 'POST':
      loop = asyncio.new_event_loop()
      asyncio.set_event_loop(loop)
      loop = asyncio.get_event_loop()
      print('interest is: ', request.POST['interest'])
      loop.run_until_complete(tables.insertInterest(str(request.POST['interest'])))
      loop.close()

      return redirect('/interest/search/')
    else:
      return render(request, 'wkit/Graphs/viewGraph.html', {})
  else:
    return HttpResponseRedirect('/')


@login_required(login_url = login_url)
def downloadGraph(request):
  import mimetypes
  import os
  from django.http.response import HttpResponse

  tables.updateCSV()
  
  BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
  filename = "file.csv"
  filepath = BASE_DIR + '/' + filename
  path = open(filepath, 'r')
  mime_type, _ = mimetypes.guess_type(filepath)
  response = HttpResponse(path, content_type=mime_type)
  response['Content-Disposition'] = "attachment; filename=%s" % filename
  return response
  #return render(request, 'wkit/Graphs/downloadGraph.html', {})

def logout(request):
  return redirect('/admin/logout/')



@login_required(login_url = login_url)
def index(request):
  return render(request, 'wkit/index.html', {})



