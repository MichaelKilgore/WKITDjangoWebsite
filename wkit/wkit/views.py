from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
import asyncio
import uuid
import datetime
from django.http import HttpResponse
from django.http import JsonResponse

from wkit.var import cities, schools, assessments, school_districts
import wkit.tables as tables

@login_required(login_url = '/admin/')
def index(request):
	return render(request, 'wkit/index.html', {})

@login_required(login_url = '/admin/')
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

@login_required(login_url = '/admin/')
def searchStudent(request, key=None):
	if request.method == 'GET':
		#allStudents, allStudents['students'] = {}, tables.getAllStudents()
		return render(request, 'wkit/Students/searchStudent.html', {})
	else:
		if request.POST['search_entry'] != "":
			if request.POST['search_type'] == 'email':
				allStudents, allStudents['students'] = {}, tables.queryStudents(0, request.POST['search_entry'])
				return render(request, 'wkit/Students/searchStudent.html', allStudents)
			elif request.POST['search_type'] == 'phone_number':
				allStudents, allStudents['students'] = {}, tables.queryStudents(1, request.POST['search_entry'])
				return render(request, 'wkit/Students/searchStudent.html', allStudents)
			else:
				allStudents, allStudents['students'] = {}, tables.queryStudents(2, request.POST['search_entry'])
				return render(request, 'wkit/Students/searchStudent.html', allStudents)
		else:
			if request.POST['search_type'] != 'full_scan':
				return render(request, 'wkit/Students/searchStudent.html', {})
			else:
				allStudents, allStudents['students'] = {}, tables.queryStudents(2, request.POST['search_entry'])
				return render(request, 'wkit/Students/searchStudent.html', allStudents)


@login_required(login_url = '/admin/')
def updateStudent(request):
	if request.method == 'POST':
		
		loop = asyncio.new_event_loop()
		asyncio.set_event_loop(loop)
		loop = asyncio.get_event_loop()
		loop.run_until_complete(tables.updateStudent(int(request.POST['studentID']), request.data))
		loop.close()

		return redirect('/student/profile/'+request.POST['studentID'])

@login_required(login_url = '/admin/')
def studentProfile(request, id):
	if request.method == 'GET':
		h = {}
		h, h['cities'], h['schools'], h['assessments'], h['interests'] = {}, cities, schools, assessments, tables.getInterests()
		h['student'] = tables.getStudent(id)
		if h['student']['mentor_id'] != "":
			x = tables.getMentor(h['student']['mentor_id'])
			h['student']['mentor_name'] = x['first_name'] + " " + x['last_name']
		h['student']['scholarships'] = tables.getScholarships(id)

		#find next june 21st.
		today = datetime.date.today()
		comparison = ""
		x = str(today).split("-")
		if int(x[1]) <= 6:
			comparison = str(x[0] + '-' + '06' + '-' + '30')
		else:
			comparison = str(str(int(x[0]) + 1) + '-' + '06' + '-' + '30')

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

		h['student']['district'] = school_districts[h['student']['school']]

		return render(request, 'wkit/Students/studentProfile.html', h)
	else:
		print('recognized post: ', request.POST)
		if 'first_name' in request.POST: #edit mode
			loop = asyncio.new_event_loop()
			asyncio.set_event_loop(loop)
			loop = asyncio.get_event_loop()
			loop.run_until_complete(tables.updateStudent(request.POST['id'], request.POST))

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
			if request.POST['search_entry'] != "":
				if request.POST['search_type'] == 'email':
					allMentors, allMentors['mentors'] = {}, tables.queryMentors(0, request.POST['search_entry'])
					return JsonResponse(allMentors)
				elif request.POST['search_type'] == 'phone_number':
					allMentors, allMentors['mentors'] = {}, tables.queryMentors(1, request.POST['search_entry'])
					return JsonResponse(allMentors)
				else:
					allMentors, allMentors['mentors'] = {}, tables.queryMentors(2, request.POST['search_entry'])
					return JsonResponse(allMentors)
			else:
				if request.POST['search_type'] != 'full_scan':
					allMentors, allMentors['mentors'] = {}, []
					return JsonResponse(allMentors)
				else:
					allMentors, allMentors['mentors'] = {}, tables.queryMentors(2, request.POST['search_entry'])
					return JsonResponse(allMentors)
		elif 'pair_mentor' in request.POST: #pair mentor to user
			loop = asyncio.new_event_loop()
			asyncio.set_event_loop(loop)
			loop = asyncio.get_event_loop()
			loop.run_until_complete(tables.pairMentor(request.POST['id'], request.POST['mentor_id']))
			loop.close()

			return HttpResponse(status=204)
		elif 'get_scholarships' in request.POST: #search for scholarships
			allScholarships, allScholarships['scholarships'] = {}, tables.queryScholarships(request.POST['id'], request.POST['name'], request.POST['min_amount'], request.POST['max_amount'], request.POST['type'])
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

	



	
			



@login_required(login_url = '/admin/')
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

@login_required(login_url = '/admin/')
def searchMentor(request, key=None):
	if request.method == 'GET':
		return render(request, 'wkit/Mentors/searchMentor.html', {})
	else:
		if request.POST['search_entry'] != "":
			if request.POST['search_type'] == 'email':
				allMentors, allMentors['mentors'] = {}, tables.queryMentors(0, request.POST['search_entry'])
				return render(request, 'wkit/Mentors/searchMentor.html', allMentors)
			elif request.POST['search_type'] == 'phone_number':
				allMentors, allMentors['mentors'] = {}, tables.queryMentors(1, request.POST['search_entry'])
				return render(request, 'wkit/Mentors/searchMentor.html', allMentors)
			else:
				allMentors, allMentors['mentors'] = {}, tables.queryMentors(2, request.POST['search_entry'])
				return render(request, 'wkit/Mentors/searchMentor.html', allMentors)
		else:
			if request.POST['search_type'] != 'full_scan':
				return render(request, 'wkit/Mentors/searchMentor.html', {})
			else:
				allMentors, allMentors['mentors'] = {}, tables.queryMentors(2, request.POST['search_entry'])
				return render(request, 'wkit/Mentors/searchMentor.html', allMentors)

@login_required(login_url = '/admin/')
def mentorProfile(request, id):
	if request.method == 'GET':
		h = {}
		h, h['cities'], h['schools'], h['assessments'], h['interests'] = {}, cities, schools, assessments, tables.getInterests()
		h['mentor'] = tables.getMentor(id)

		return render(request, 'wkit/Mentors/mentorProfile.html', h)
	else:
		loop = asyncio.new_event_loop()
		asyncio.set_event_loop(loop)
		loop = asyncio.get_event_loop()
		x, x['what'] = {}, request.POST
		print(x)
		#loop.run_until_complete(tables.updateStudent(int(request.POST['studentID']), request.POST))
		loop.close()

		return redirect('/mentor/profile/'+request.POST['mentorID'])
		return render(request, 'wkit/Mentors/mentorProfile.html', {})

@login_required(login_url = '/admin/')
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

@login_required(login_url = '/admin/')
def searchProgram(request):
	if request.method == 'GET':
		h, h['cities'], h['interests'] = {}, cities, tables.getInterests()

		return render(request, 'wkit/Programs/searchProgram.html', h)
	else:
		print('this done worked: ', request.POST)
		if request.POST['program_name'] == "" and request.POST['search_duration'] == 'Any' and 'city' not in request.POST and 'interest' not in request.POST:
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


@login_required(login_url = '/admin/')
def programProfile(request, id):
	if request.method == 'GET':
		h = {}
		h, h['cities'], h['interests'] = {}, cities, tables.getInterests()
		h['organizations'] = tables.getOrganizations()
		h['program'] = tables.getProgram(id)
		h['organization'] = tables.getProgram(h['program']['organizationID'])

		return render(request, 'wkit/Programs/programProfile.html', h)
	else:
		loop = asyncio.new_event_loop()
		asyncio.set_event_loop(loop)
		loop = asyncio.get_event_loop()
		x, x['what'] = {}, request.POST
		print(x)
		loop.close()

		return redirect('/program/profile/'+request.POST['programID'])
		return render(request, 'wkit/Programs/programProfile.html', {})

	return render(request, 'wkit/Programs/programProfile.html', {})

@login_required(login_url = '/admin/')
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
			h	= {}
			return render(request, 'wkit/Organizations/createOrganization.html', h)
	else:
		return HttpResponseRedirect('/')

@login_required(login_url = '/admin/')
def searchOrganization(request):
	if request.method == 'GET':
		return render(request, 'wkit/Organizations/searchOrganization.html', {})
	else:
		if request.POST['search_entry'] != "":
			if request.POST['search_type'] == 'Name':
				allOrganizations, allOrganizations['organizations'] = {}, tables.queryOrganizations(0, request.POST['search_entry'])
				return render(request, 'wkit/Organizations/searchOrganization.html', allOrganizations)
			else:
				allOrganizations, allOrganizations['organizations'] = {}, tables.queryOrganizations(1, request.POST['search_entry'])
				return render(request, 'wkit/Organizations/searchOrganization.html', allOrganizations)
		else:
			if request.POST['search_type'] != 'full_scan':
				return render(request, 'wkit/Organizations/searchOrganization.html', {})
			else:
				allOrganizations, allOrganizations['organizations'] = {}, tables.queryOrganizations(2, request.POST['search_entry'])
				return render(request, 'wkit/Organizations/searchOrganization.html', allOrganizations)

@login_required(login_url = '/admin/')
def organizationProfile(request, id):
	if request.method == 'GET':
		h = {}
		h, h['cities'] = {}, cities
		h['organization'] = tables.getOrganization(id)

		return render(request, 'wkit/Organizations/organizationProfile.html', h)
	else:
		loop = asyncio.new_event_loop()
		asyncio.set_event_loop(loop)
		loop = asyncio.get_event_loop()
		x, x['what'] = {}, request.POST
		print(x)
		#loop.run_until_complete(tables.updateStudent(int(request.POST['studentID']), request.POST))
		loop.close()

		return redirect('/mentor/profile/'+request.POST['mentorID'])
		return render(request, 'wkit/Mentors/mentorProfile.html', {})


	return render(request, 'wkit/Organizations/organizationProfile.html', {})

@login_required(login_url = '/admin/')
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

@login_required(login_url = '/admin/')
def searchInterest(request):
	if request.method == 'GET':
		return render(request, 'wkit/Interests/searchInterest.html', {})
	else:
		if 'interest' in request.POST:
			print('request.POST is: ', request.POST)
			tables.deleteInterest(request.POST['interest'])
			return HttpResponse(status=204)

		if request.POST['search_entry'] != "":
			allInterests, allInterests['interests'] = {}, tables.queryInterests(request.POST['search_entry'])
			return render(request, 'wkit/Interests/searchInterest.html', allInterests)
		else:
			allInterests, allInterests['interests'] = {}, tables.queryInterests('')
			return render(request, 'wkit/Interests/searchInterest.html', allInterests)

@login_required(login_url = '/admin/')
def deleteInterest(request):
	print('delete called');
	return redirect('/interest/search/')



@login_required(login_url = '/admin/')
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

@login_required(login_url = '/admin/')
def searchScholarship(request):
	if request.method == 'GET':
		return render(request, 'wkit/Scholarships/searchScholarship.html', {})
	else:
		allScholarships, allScholarships['scholarships'] = {}, tables.queryScholarships('foo', request.POST['name'], request.POST['min_amount'], request.POST['max_amount'], request.POST['type'])
		return render(request, 'wkit/Scholarships/searchScholarship.html', allScholarships)

@login_required(login_url = '/admin/')
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


@login_required(login_url = '/admin/')
def downloadGraph(request):
	if request.method == 'GET':
		return render(request, 'wkit/Graphs/downloadGraph.html', {})
	else:
		if 'interest' in request.POST:
			print('request.POST is: ', request.POST)
			tables.deleteInterest(request.POST['interest'])
			return HttpResponse(status=204)

		if request.POST['search_entry'] != "":
			allInterests, allInterests['interests'] = {}, tables.queryInterests(request.POST['search_entry'])
			return render(request, 'wkit/Interests/searchInterest.html', allInterests)
		else:
			allInterests, allInterests['interests'] = {}, tables.queryInterests('')
			return render(request, 'wkit/Interests/searchInterest.html', allInterests)







def logout(request):
	return redirect('admin/logout/')



@login_required(login_url = '/admin/')
def index(request):
	return render(request, 'wkit/index.html', {})









