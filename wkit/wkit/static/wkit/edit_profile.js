//save old values
var oldValues = ['', '', '', '', '', '', '', ''];
var oldInterestElement = document.getElementById('add-another-interest');
var oldInterest = "";
var oldOrganization = ""
if (oldInterestElement) {
  oldInterest = oldInterestElement.innerHTML;
}


var editMode = false;

/////////////////////////////////////////////////////////////////
//All the elements in a profile that are written fields can be
//editted by writting, their readonly mode is toggled with this
//function.
function toggleEditReadOnly() {
	if (editMode == false) {
		var elements = document.getElementsByClassName('enableEdit');

		for (var i = 0; i < elements.length; i++) {
			elements[i].removeAttribute('readonly');
		}
	} else {
		var elements = document.getElementsByClassName('enableEdit');

		for (var i = 0; i < elements.length; i++) {
			elements[i].setAttribute('readonly', true);
		}
	}
}

///////////////////////////////////////////////////////////////////////
//toggles edit button between an edit button and a cancel button
//  edit button toggles enableEdit() and that allows user to edit
//  profile values.
// 
//  and cancelChanges() basically reverts what ever enableEdit()
//  change does.
function changeEditButtonToCancelButton() {
	if (editMode == false) {
		var element = document.getElementById('editContent');

		element.innerHTML = "<button type='button' onClick='cancelChanges()'>Cancel</button>";
	} else {
		var element = document.getElementById('editContent');

		element.innerHTML = "<button type='button' onClick='enableEdit()'>Edit</button><br>";
	}
}

function toggleEditCity() {
	if (editMode == false) {
		var city_change = document.getElementById('changeCity');
		city_change.removeAttribute("hidden");

		var opts = city_change.options;
		for (var i = 0; opt = opts[i]; i++) {
			if (opt.value == document.getElementById('city').value) {
				opt.setAttribute('selected', 'true');
				break;
			}
		}
	} else {
		var city_changes = document.getElementById('changeCity');
		city_changes.setAttribute('hidden', true);
	}
}

function toggleEditSchool() {
	if (editMode == false) {
		var school_change = document.getElementById('changeSchool');
		school_change.removeAttribute("hidden");

		var opts = school_change.options;
		for (var i = 0; opt = opts[i]; i++) {
			if (opt.value == document.getElementById('school')) {
				opt.setAttribute('selected', 'true');
				break;
			}
		}	
	} else {
		var school_change = document.getElementById('changeSchool');
		school_change.setAttribute('hidden', true);
	}
}

function toggleEditGrade() {
	if (editMode == false) {
		var curGrade = document.getElementById('grade').value;
		var grade_change = document.getElementById('changeGrade');
		grade_change.removeAttribute("hidden");

		var opts = grade_change.options;
		for (var i = 0; opt = opts[i]; i++) {
			if (opt.value == curGrade) {
				opt.setAttribute('selected', 'true');
				break;
			}
		}
	} else {
		var grade_change = document.getElementById('changeGrade');
		grade_change.setAttribute('hidden', true);
	}
}

function toggleEditInterest() {
	if (editMode == false) {
		var interest = document.getElementById('interest');
		var allInterests = interest.value.split(", ");

		if (allInterests.length == 1) {
			var add_another_interest = document.getElementById('add-another-interest');

      if (document.getElementById('remove-interest-button') != null) {
        var remove_interest_button = document.getElementById('remove-interest-button');
        var add_another_interest_button = document.getElementById('add-another-interest-button');
        add_another_interest_button.removeAttribute("hidden");
        remove_interest_button.removeAttribute("hidden");
      }
			
			add_another_interest.value=document.getElementById('interest').value;

			add_another_interest.removeAttribute("hidden");

		} else {
			var add_another_interest = document.getElementById('add-another-interest');
			var remove_interest_button = document.getElementById('remove-interest-button');
			var add_another_interest_button = document.getElementById('add-another-interest-button');

			
			add_another_interest.value=document.getElementById('interest').value;

			var fieldOfInterest = document.getElementById('field-of-interest-1');

			var opts = fieldOfInterest.options;
			for (var i = 0; opt = opts[i]; i++) {
				if (opt.value == allInterests[0]) {
					opt.setAttribute('selected', 'true');
					break;
				}
			}

			var extras = 1;
			while(extras != allInterests.length) {
				var nextInterest = fieldOfInterest.cloneNode(true);
				nextInterest.id = 'field-of-interest-' + (extras+1);

				var opts = nextInterest.options;

				for (var i=0; opt=opts[i]; i++) {
					opt.removeAttribute('selected');
				}

				for (var i = 0; opt = opts[i]; i++) {
					if (opt.value == allInterests[extras]) {
						opt.setAttribute('selected', 'true');
						break;
					}
				}

				add_another_interest.innerHTML = add_another_interest.innerHTML + "<br id='div-field-of-interest-" + (extras+1) + "'>" + nextInterest.outerHTML;
				extras += 1;
			}
			add_another_interest.removeAttribute("hidden");
			add_another_interest_button.removeAttribute("hidden");
			remove_interest_button.removeAttribute("hidden");
		} //: ELSE
	} else {
		var interest_change = document.getElementById('add-another-interest');
    
    if (document.getElementById('remove-interest-button') != null) {
      var remove_interest_button = document.getElementById('remove-interest-button');
      var add_another_interest_button = document.getElementById('add-another-interest-button');
      remove_interest_button.setAttribute("hidden", true);
      add_another_interest_button.setAttribute('hidden', true);
    }


		interest_change.innerHTML = oldInterest;

		interest_change.setAttribute('hidden', true);
	}
}

function toggleEditAssessment() {
	if (editMode == false) {
		var assessment_change = document.getElementById('changeAssessment');

		var assessment = document.getElementById('assessment').value;
		var opts = assessment_change.options;
		for (var i = 0; opt = opts[i]; i++) {
			if (opt.value == assessment) {
				opt.setAttribute('selected', 'true');
				break;
			}
		}
		assessment_change.removeAttribute("hidden");
	} else {
		var assessment_change = document.getElementById('changeAssessment');
		assessment_change.setAttribute('hidden', true);
	}
}

function toggleEditPreferredMethod() {
	if (editMode == false) {
		var method_change = document.getElementById('changePreferredMethod');

		var preferred_method = document.getElementById('preferred_method').value;
		var opts = method_change.options;
		for (var i = 0; opt = opts[i]; i++) {
			if (opt.value == preferred_method) {
				opt.setAttribute('selected', 'true');
				break;
			}
		}
		method_change.removeAttribute("hidden");
	} else {
		var method_change = document.getElementById('changePreferredMethod');
		method_change.setAttribute('hidden', true);
	}
}

function toggleEditGender() {
	if (editMode == false) {	
		var gender_change = document.getElementById('changeGender');
		var gender = document.getElementById('gender').value;

		if (gender == document.getElementById("Cisgender Women").value) {
			document.getElementById("Cisgender Women").checked = true;
		} else if (gender == document.getElementById("Cisgender Male").value) {
			document.getElementById("Cisgender Male").checked = true;
		} else if (gender == document.getElementById("Genderqueer").value) {
			document.getElementById("Genderqueer").checked = true;
		} else if (gender == document.getElementById("transF").value) {
			document.getElementById("transF").checked = true;
		} else if (gender == document.getElementById("transM").value) {
			document.getElementById("transM").checked = true;
		} else if (gender == document.getElementById("other").value) {
			document.getElementById("other").checked = true;
		}
		gender_change.removeAttribute("hidden");	
		gender_change.style.display='block';
	} else {
		var gender_change = document.getElementById('changeGender');
		gender_change.style.display='none';

	}
}

function toggleEditEthnicity() {
	if (editMode == false) {
		var ethnic_change = document.getElementById('changeEthnicity');	
		var ethnic = document.getElementById('ethnicity').value;

		if (ethnic == document.getElementById("white").value) {
			document.getElementById("white").checked = true;
		} else if (ethnic == document.getElementById("aioan").value) {
			document.getElementById("aioan").checked = true;
		} else if (ethnic == document.getElementById("asian").value) {
			document.getElementById("asian").checked = true;
		} else if (ethnic == document.getElementById("black").value) {
			document.getElementById("black").checked = true;
		} else if (ethnic == document.getElementById("hispanic").value) {
			document.getElementById("hispanic").checked = true;
		} else if (ethnic == document.getElementById("hawaiian").value) {
			document.getElementById("hawaiian").checked = true;
		}
		ethnic_change.removeAttribute("hidden");
		ethnic_change.style.display='block';
	} else {
		var ethnic_change = document.getElementById('changeEthnicity');
		ethnic_change.style.display='none';
	}
}

function toggleEditMentorDelete() {
	var element = document.getElementById('paired_mentor_delete');	
	if (editMode == false) {
		element.removeAttribute('hidden');
	} else {
		element.setAttribute('hidden', true);
	}
}

function toggleEditScholarships() {
	var elements = document.getElementsByClassName('scholarship_table_delete_button');
	
	if (editMode == false) {
		for (var i =0;i<elements.length; i++) {
			elements[i].removeAttribute('hidden');
		}
	} else {
		for (var i =0;i<elements.length; i++) {
			elements[i].setAttribute('hidden', true);
		}
	}
}

///////////////////////////////////////////////////////////////////////////////
//all the nonEditMode elements are toggled as hidden or not.
function toggleNonEditMode() {
	if (editMode == false) {
		var nonEditStuff = document.getElementsByClassName('nonEditMode');

		for (var i = 0; i < nonEditStuff.length; i++) {
			nonEditStuff[i].style.display = 'none';
		}
	} else {
		var nonEditStuff = document.getElementsByClassName('nonEditMode');

		for (var i = 0; i < nonEditStuff.length; i++) {
			nonEditStuff[i].style.display = 'block';
		}
	}
}

//////////////////////////////////////////////////////////////////////
//toggles save button between showing and hidden.
function toggleSaveOption() {
	if (editMode == false) {
		var save = document.getElementById('saveButton');
		save.removeAttribute("hidden");
	} else {
		var save = document.getElementById('saveButton');
		save.setAttribute("hidden", true);
	}
}

function setOldValues() {
	var elements = document.getElementsByClassName('enableEdit');
	for (var i = 0; i < elements.length; i++) {
		oldValues[i] = elements[i].value;
	}
}

function revertEnableEditChanges() {
	var elements = document.getElementsByClassName('enableEdit');
	for (var i=0; i<elements.length; i++) {
		elements[i].value = oldValues[i];
	}
}

function reloadEthnicity(ethnic) {
	var ethnic_change = document.getElementById('changeEthnicity');	
	if (ethnic == document.getElementById("white").value) {
		document.getElementById("white").checked = true;
	} else if (ethnic == document.getElementById("aioan").value) {
		document.getElementById("aioan").checked = true;
	} else if (ethnic == document.getElementById("asian").value) {
		document.getElementById("asian").checked = true;
	} else if (ethnic == document.getElementById("black").value) {
		document.getElementById("black").checked = true;
	} else if (ethnic == document.getElementById("hispanic").value) {
		document.getElementById("hispanic").checked = true;
	} else if (ethnic == document.getElementById("hawaiian").value) {
		document.getElementById("hawaiian").checked = true;
	}
	ethnic_change.removeAttribute("hidden");
}

function reloadGender(gender) {
	var gender_change = document.getElementById('changeGender');

	if (gender == document.getElementById("Cisgender Women").value) {
		document.getElementById("Cisgender Women").checked = true;
	} else if (gender == document.getElementById("Cisgender Male").value) {
		document.getElementById("Cisgender Male").checked = true;
	} else if (gender == document.getElementById("Genderqueer").value) {
		document.getElementById("Genderqueer").checked = true;
	} else if (gender == document.getElementById("transF").value) {
		document.getElementById("transF").checked = true;
	} else if (gender == document.getElementById("transM").value) {
		document.getElementById("transM").checked = true;
	} else if (gender == document.getElementById("other").value) {
		document.getElementById("other").checked = true;
	}
	gender_change.removeAttribute("hidden");	
}

function toggleIsVolunteer() {
  if (editMode == false) {
    var is_volunteer_change = document.getElementById('changeVolunteerStatus');

    var is_volunteer = document.getElementById('is_volunteer').value;
    var opts = is_volunteer_change.options;
    for (var i = 0; opt = opts[i]; i++) {
      if (opt.value == is_volunteer) {
        opt.setAttribute('selected', 'true');
        break;
      }
    }
    is_volunteer_change.removeAttribute("hidden");
  } else {
     var is_volunteer_change = document.getElementById('changeVolunteerStatus');
     is_volunteer_change.setAttribute("hidden", true);
  }

 
}

function toggleEditPairedStudents() {
 var elements = document.getElementsByClassName('student_table_delete_button');
	
	if (editMode == false) {
		for (var i =0;i<elements.length; i++) {
			elements[i].removeAttribute('hidden');
		}
	} else {
		for (var i =0;i<elements.length; i++) {
			elements[i].setAttribute('hidden', true);
		}
	}  
}

function toggleType() {
  if (editMode == false) {
    var type_change = document.getElementById('changeScholarshipType');

    var type = document.getElementById('type').value;
    var opts = type_change.options;
    for (var i = 0; opt = opts[i]; i++) {
      if (opt.value == type) {
        opt.setAttribute('selected', 'true');
        break;
      }
    }
    type_change.removeAttribute("hidden");
  } else {
     var type_change = document.getElementById('changeScholarshipType');
     type_change.setAttribute("hidden", true);
  }
}

function toggleEditOrgType() {
  if (editMode == false) {
    var type_change = document.getElementById('changeType');
    type_change.removeAttribute("hidden");

    var school = document.getElementById("school");
    var business = document.getElementById("business");

    var type = document.getElementById("type");
    if (type.value == "School") {
      school.checked = true;
    } else {
      business.checked = true;
    }
  } else {
    var type_change = document.getElementById('changeType');
    type_change.setAttribute("hidden", true);
  }
}

function toggleEditOrganization() {
	if (editMode == false) {
		var org = document.getElementById('organization_name');

    var new_org = document.getElementById('newOrganization');

    new_org.value=document.getElementById('organization_id').value;

    new_org.removeAttribute("hidden");

	} else {
		var org = document.getElementById('organozation_name');
    var new_org = document.getElementById('newOrganization');

		//org.innerHTML = oldOrganization;

		new_org.setAttribute('hidden', true);
	}
}

function toggleEditTimeCommitment() {
  var time_com = document.getElementById('change-time-commitment');
  if (editMode == false) {
    time_com.value=document.getElementById('time_commitment').value;

    time_com.removeAttribute("hidden");
  } else {
    time_com.setAttribute('hidden', true);
  }

}





