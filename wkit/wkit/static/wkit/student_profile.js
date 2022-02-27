function cancelChanges() {
	//revert enableEdit values back to original values
	revertEnableEditChanges();	

	toggleEditReadOnly();

	changeEditButtonToCancelButton();

	toggleEditCity();
	toggleEditSchool();
	toggleEditGrade();	
	toggleEditInterest();
	toggleEditAssessment();
	toggleEditPreferredMethod();
	toggleEditGender();
	toggleEditEthnicity();
	toggleEditMentorDelete();
	toggleEditScholarships();

	toggleSaveOption();

	//reveal non edit values again.
	toggleNonEditMode();

	removeScholarship('', '');

	editMode = false;	
}

///////////////////////////////////////////////////////////////
//calls following functions:
//
//  toggleEditReadOnly() ->             toggles readonly attributes of
//                                      elements that are changed with
//                                      writing and switches between
//                          						readonly and edittable.
//
//  changeEditButtonToCancelButton() -> just toggles the edit button
//																			to a cancel button or vise
//																			versa.
//
//	toggleEditCity() ->									toggle city element between 
//																			edit and non-edit.
//
// toggleEditSchool() ->								toggle school element between
//																			edit and non-edit.
//
// toggleEditGrade() ->									toggle grade element between
//																			edit and non-edit.
//
// toggleEditInterest() ->							toggle interest element between
//																			edit and non-edit.
//
// toggleEditGender() ->								toggle gender element between
//																			edit and non-edit.
//
// toggleEditEthnicity() ->							toggle ethnicity element between
//																			edit and non-edit.
//
// toggleNonEditMode() ->								toggle nonEditMode elements between
//																			hidden or not.
//
// toggleSaveOption() ->								toggle save button between
//																			showing and hiding.
function enableEdit() {
	setOldValues();

	toggleEditReadOnly();

	changeEditButtonToCancelButton();

	toggleEditCity();
	toggleEditSchool();
	toggleEditGrade();	
	toggleEditInterest();
	toggleEditAssessment();
	toggleEditPreferredMethod();
	toggleEditGender();
	toggleEditEthnicity();
	toggleEditMentorDelete();
	toggleEditScholarships();

	toggleNonEditMode();
	toggleSaveOption();

	editMode = true;
}

function convertToMentor(id) {
	let isExecuted = confirm("Are you would like to convert this user to a mentor?");

	if (isExecuted) {

		fetch('', {
			method: 'POST',
			headers: {
				'X-CSRFToken': csrftoken,
				'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
			},
			body: new URLSearchParams({
				'convert_to_mentor': 'conversion',
        'id': id
    	})
		})

		location.href="/";
	}

}

function deleteStudent(id) {
	let isExecuted = confirm("Are you sure you would like to delete this user?");

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

function getMentors(id) {

	//EMPTIES THE TABLE BEFORE PERFORMING SEARCH TO CLEAR OLD RESULTS
	empty_table = document.getElementById('mentor-search-table');
	var row_count = empty_table.rows.length;
	for (var i = 1; i < row_count; i++) {
		empty_table.deleteRow(1);
	}
		

	var search_type_pulldown = document.getElementById('mentor_pair_search_type');
	var search_type = search_type_pulldown.options[search_type_pulldown.selectedIndex];
	var search_field = document.getElementById('mentor_pair_search_entry');

	fetch('', {
		method: 'POST',
		headers: {
			'X-CSRFToken': csrftoken,
			'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
		},
		body: new URLSearchParams({
			'get_mentors': 'getMentors',
			'search_type': search_type.value,
			'search_entry': search_field.value
		})
	})
	.then(response => response.json())
	.then(data => {
		table = document.getElementById('mentor-search-table');
    document.getElementById('prev_page').disabled = true;
    document.getElementById('next_page').disabled = !data.hasNext;

		for (var i=0;mentor=data.mentors[i];i++) {
			var newRow = table.insertRow();
			var firstCell = newRow.insertCell();
			var secondCell = newRow.insertCell();
			var thirdCell = newRow.insertCell();
			var fourthCell = newRow.insertCell();

			var fullName = mentor.first_name + " " + mentor.last_name;
			firstCell.innerHTML = fullName;
			secondCell.innerHTML = mentor.phone_number;
			thirdCell.innerHTML = mentor.email;
			fourthCell.innerHTML = "<button onClick=\"pairMentor('"+ id + "', '"  + mentor.id + "', '" + fullName + "', '" + newRow.rowIndex + "')\">Pair</button>"; 
		}

	});

}


function pairMentor(id, mentor_id, fullName, rowIndex) {
	fetch('', {
		method: 'POST',
		headers: {
			'X-CSRFToken': csrftoken,
			'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
		},
		body: new URLSearchParams({
			'pair_mentor': 'pairMentor',
			'id': id,
			'mentor_id': mentor_id,
		})
	})

	document.getElementById('mentor-search-table').deleteRow(parseInt(rowIndex));

	var mentor_field = document.getElementById('paired_mentor');	
	mentor_field.innerHTML = "<a href=\"/mentor/profile/" + mentor_id + "\">" + fullName + "</a>";

  var paired_msg = document.getElementById('paired_msg');
  paired_msg.innerHTML = "Paired mentor " + fullName;
}

function getScholarships(id) {
	//EMPTIES THE TABLE BEFORE PERFORMING SEARCH TO CLEAR OLD RESULTS
	empty_table = document.getElementById('scholarship-search-table');
	var row_count = empty_table.rows.length;
	for (var i = 1; i < row_count; i++) {
		empty_table.deleteRow(1);
	}

	var name = document.getElementById('scholar_name_search').value;
	var min = document.getElementById('scholar_min_search').value;
	var max = document.getElementById('scholar_max_search').value;
	var type = document.querySelector('input[name="program_type"]:checked').value;

	fetch('', {
		method: 'POST',
		headers: {
			'X-CSRFToken': csrftoken,
			'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
		},
		body: new URLSearchParams({
			'get_scholarships': 'getScholarships',
			'id': id,
			'name': name,
			'min_amount': min,
			'max_amount': max,
			'type': type
		})
	})
	.then(response => response.json() )
	.then(data => {
		table = document.getElementById('scholarship-search-table');

		for (var i=0;scholarship=data.scholarships[i];i++) {
			var newRow = table.insertRow();
			var firstCell = newRow.insertCell();
			var secondCell = newRow.insertCell();
			var thirdCell = newRow.insertCell();
			var fourthCell = newRow.insertCell();

			firstCell.innerHTML = scholarship.name;
			secondCell.innerHTML = scholarship.type;
			thirdCell.innerHTML = scholarship.amount;
			fourthCell.innerHTML = "<button onClick=\"pairScholarship('"+ id + "', '"  + scholarship.id + "', '" + scholarship.name + "', '" + scholarship.amount + "', '" + scholarship.type + "', '"  + newRow.rowIndex + "')\">Pair</button>"; 
		}

	});

}

function pairScholarship(id, scholarship_id, scholarship_name, scholarship_amount, scholarship_type, rowIndex) {
	fetch('', {
		method: 'POST',
		headers: {
			'X-CSRFToken': csrftoken,
			'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
		},
		body: new URLSearchParams({
			'pair_scholarship': 'pairScholarship',
			'id': id,
			'scholarship_id': scholarship_id,
		})
	})

	document.getElementById('scholarship-search-table').deleteRow(parseInt(rowIndex));

	if (scholarship_type == "Internal") {
		i_table = document.getElementById('internal_scholarships_table');

		var newRow = i_table.insertRow();
		var firstCell = newRow.insertCell();
		var secondCell = newRow.insertCell();
		var thirdCell = newRow.insertCell();
		firstCell.innerHTML = scholarship_name;
		secondCell.innerHTML = "$" + scholarship_amount;
		thirdCell.outerHTML = "<td class=\"scholarship_table_delete_button\" hidden><button style=\"color: red\" type=\"button\" onClick=\"removeScholarship('" + scholarship_id  +  "', '" + id +  "')\">delete</button></td>";

		thirdCell.setAttribute('hidden', true);
	} else {
		e_table = document.getElementById('external_scholarships_table');

		var newRow = e_table.insertRow();
		var firstCell = newRow.insertCell();
		var secondCell = newRow.insertCell();
		var thirdCell = newRow.insertCell();
		firstCell.innerHTML = scholarship_name;
		secondCell.innerHTML = "$" + scholarship_amount;
		thirdCell.innerHTML = scholarship_id;
		thirdCell.setAttribute('hidden', true);
	}

	alert("Scholarship Paired!");
	
}

function removeScholarship(scholarship_id, student_id) {
	var ethnic = document.querySelector('input[name="ethnicity"]:checked').value;
	var gender = document.querySelector('input[name="gender"]:checked').value;

	if (scholarship_id != '') {
		var doc = document.getElementById('student_profile_edit_form');

		doc.innerHTML = doc.innerHTML + "<input class=\"scholarships_to_be_deleted\" name=\"deleted_scholarships\" value=\"" + scholarship_id + "\" hidden>  <input class=\"scholarships_to_be_deleted\" name=\"deleted_scholarships\" value=\"" + scholarship_id + "\" hidden>";

		var row_id = "row_" + scholarship_id;
		var hide_row = document.getElementById(row_id);
		hide_row.setAttribute('hidden', true);
	} else {
		var elements = document.getElementsByClassName('scholarships_to_be_deleted');
		for (var i=0; i<elements.length; i++) {
			elements[i].outerHTML = "";
		}
		var hidden_elements = document.getElementsByClassName('scholarship_table_row');

		for (var i=0; i<hidden_elements.length; i++) {
			hidden_elements[i].removeAttribute('hidden');
		}
	}

	reloadEthnicity(ethnic);	
	reloadGender(gender);	

}


		





