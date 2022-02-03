function cancelChanges() {
  revertEnableEditChanges();
  
  toggleEditReadOnly();
  changeEditButtonToCancelButton(); 
  toggleEditCity();
  toggleEditInterest();
  //not done
  toggleIsVolunteer();
  toggleEditPreferredMethod();  
  toggleEditGender();
  toggleEditEthnicity();
  //not done
  toggleEditPairedStudents();
  toggleSaveOption();
  toggleNonEditMode();

	removeStudent('', '');

  
  editMode = false;
}

function enableEdit() {
	setOldValues();
  
  toggleEditReadOnly();
  
  changeEditButtonToCancelButton();

  toggleEditReadOnly();
  changeEditButtonToCancelButton(); 
  toggleEditCity();
  toggleEditInterest();
  toggleIsVolunteer();
  toggleEditPreferredMethod();  
  toggleEditGender();
  toggleEditEthnicity();
  //not done
  toggleEditPairedStudents();
  toggleSaveOption();
  toggleNonEditMode();
  
  editMode = true;

}

function deleteMentor(id) {
	let isExecuted = confirm("Are you sure you would like to delete this mentor?");

	if (isExecuted) {
		fetch('', {
			method: 'POST',
			headers: {
				'X-CSRFToken': csrftoken,
				'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
			},
			body: new URLSearchParams({
				'delete': 'delete',
        'id': id
    	})
		})

		location.href="/";
	}
}


function getStudents(id) {

	//EMPTIES THE TABLE BEFORE PERFORMING SEARCH TO CLEAR OLD RESULTS
	empty_table = document.getElementById('student-search-table');
	var row_count = empty_table.rows.length;
	for (var i = 1; i < row_count; i++) {
		empty_table.deleteRow(1);
	}
		

	var x = document.getElementById('student_pair_search_type');
	var y = x.options[x.selectedIndex];
	var z = document.getElementById('student_pair_search_entry');

	fetch('', {
		method: 'POST',
		headers: {
			'X-CSRFToken': csrftoken,
			'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
		},
		body: new URLSearchParams({
			'get_students': 'getStudents',
			'search_type': y.value,
			'search_entry': z.value
		})
	})
	.then(response => response.json())
	.then(data => {
		table = document.getElementById('student-search-table');

		for (var i=0;student=data.students[i];i++) {
			var newRow = table.insertRow();
			var firstCell = newRow.insertCell();
			var secondCell = newRow.insertCell();
			var thirdCell = newRow.insertCell();
			var fourthCell = newRow.insertCell();

			var fullName = student.first_name + " " + student.last_name;
			firstCell.innerHTML = fullName;
			secondCell.innerHTML = student.phone_number;
			thirdCell.innerHTML = student.email;
			fourthCell.innerHTML = "<button onClick=\"pairStudent('"+ id + "', '"  + student.id + "', '" + fullName + "', '" + newRow.rowIndex + "')\">Pair</button"; 
		}

	});

}

function pairStudent(id, student_id, fullName, rowIndex) {
	fetch('', {
		method: 'POST',
		headers: {
			'X-CSRFToken': csrftoken,
			'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
		},
		body: new URLSearchParams({
			'pair_student': 'pairMentor',
			'id': id,
			'student_id': student_id,
		})
	})

	document.getElementById('student-search-table').deleteRow(parseInt(rowIndex));

  table = document.getElementById('students_table');

  var newRow = table.insertRow();
  var firstCell = newRow.insertCell();
  var secondCell = newRow.insertCell();
  firstCell.innerHTML = "<a href=\"/mentor/profile/" + id + "\">" + fullName + "</a>";
  secondCell.outerHTML = "<td class=\"students_table_delete_button\" hidden><button style=\"color: red\" type=\"button\" onClick=\"removeStudent('" + student_id  +  "', '" + id +  "')\">delete</button></td>";

  secondCell.setAttribute('hidden', true);

	alert("Student Paired!");
}

function removeStudent(student_id, mentor_id) {
	var ethnic = document.querySelector('input[name="ethnicity"]:checked').value;
	var gender = document.querySelector('input[name="gender"]:checked').value;

  if (student_id != '') {
		var doc = document.getElementById('mentor_profile_edit_form');

		doc.innerHTML = doc.innerHTML + "<input class=\"students_to_be_deleted\" name=\"deleted_students\" value=\"" + student_id + "\" hidden>";

		var row_id = "row_" + student_id;
		var hide_row = document.getElementById(row_id);
		hide_row.setAttribute('hidden', true);
	} else {
		var elements = document.getElementsByClassName('students_to_be_deleted');
		for (var i=0; i<elements.length; i++) {
			elements[i].outerHTML = "";
		}

		var hidden_elements = document.getElementsByClassName('student_table_row');

		for (var i=0; i<hidden_elements.length; i++) {
			hidden_elements[i].removeAttribute('hidden');
		}
	}

	reloadEthnicity(ethnic);	
	reloadGender(gender);	

}


