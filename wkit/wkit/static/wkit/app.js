
//save old values
var oldValues = ['0', '1', '2', '3', '4', '5', '6', '7'];
var elements = document.getElementsByClassName('enableEdit');
for (var i = 0; i < elements.length; i++) {
	oldValues[i] = elements[i].value;
}

function enableEdit() {
	var elements = document.getElementsByClassName('enableEdit');

	for (var i = 0; i < elements.length; i++) {
		elements[i].removeAttribute('readonly');
	}

	var element = document.getElementById('editContent');

	element.innerHTML = "<button type='button' onClick='cancelChanges()'>Cancel</button>";

	var city_change = document.getElementById('changeCity');
	city_change.removeAttribute("hidden");

	var opts = city_change.options;
	for (var i = 0; opt = opts[i]; i++) {
		if (opt.value == document.getElementById('city').value) {
			opt.setAttribute('selected', 'true');
			break;
		}
	}

	var school_change = document.getElementById('changeSchool');
	school_change.removeAttribute("hidden");

	var opts = school_change.options;
	for (var i = 0; opt = opts[i]; i++) {
		if (opt.value == document.getElementById('school')) {
			opt.setAttribute('selected', 'true');
			break;
		}
	}

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

	var interest = document.getElementById('interest');
	var allInterests = interest.value.split(", ");

	if (allInterests.length == 1) {
		var add_another_interest = document.getElementById('add-another-interest');
		var add_another_interest_button = document.getElementById('add-another-interest-button');
		
		add_another_interest.value=document.getElementById('interest').value;

		add_another_interest.removeAttribute("hidden");
		add_another_interest_button.removeAttribute("hidden");
	} else {
		var add_another_interest = document.getElementById('add-another-interest');
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
			nextInterest.id = 'field-of-interest-' + num;

			var opts = nextInterest.options;
			//alert(opts[1].value);
			for (var i = 0; opt = opts[i]; i++) {
				if (opt.value == allInterests[extras]) {
					opt.setAttribute('selected', 'true');
					break;
				}
			}

			num += 1;

			add_another_interest.innerHTML = add_another_interest.innerHTML + '<br>' + nextInterest.outerHTML;
			extras += 1;
		}
		add_another_interest.removeAttribute("hidden");
		add_another_interest_button.removeAttribute("hidden");

	}

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

	var nonEditStuff = document.getElementsByClassName('nonEditMode');

	for (var i = 0; i < nonEditStuff.length; i++) {
		nonEditStuff[i].style.display = 'none';
	}

	var save = document.getElementById('saveButton');
	save.removeAttribute("hidden");


}

function enableEditMentor() {
	var elements = document.getElementsByClassName('enableEdit');

	for (var i = 0; i < elements.length; i++) {
		elements[i].removeAttribute('readonly');
	}

	var element = document.getElementById('editContent');

	element.innerHTML = "<button type='button' onClick='cancelChanges()'>Cancel</button>";
	
	var city_change = document.getElementById('changeCity');
	city_change.removeAttribute("hidden");

	var opts = city_change.options;
	for (var i = 0; opt = opts[i]; i++) {
		if (opt.value == document.getElementById('city').value) {
			opt.setAttribute('selected', 'true');
			break;
		}
	}

	var interest = document.getElementById('interest');
	var allInterests = interest.value.split(", ");

	if (allInterests.length == 1) {
		var add_another_interest = document.getElementById('add-another-interest');
		var add_another_interest_button = document.getElementById('add-another-interest-button');
		
		add_another_interest.value=document.getElementById('interest').value;

		add_another_interest.removeAttribute("hidden");
		add_another_interest_button.removeAttribute("hidden");
	} else {
		var add_another_interest = document.getElementById('add-another-interest');
		var add_another_interest_button = document.getElementById('add-another-interest-button');
		
		add_another_interest.value=document.getElementById('interest').value;

		var fieldOfInterest = document.getElementById('field-of-interest-1');

		var opts = fieldOfInterest.options;
		//alert(opts[1].value);
		for (var i = 0; opt = opts[i]; i++) {
			if (opt.value == allInterests[0]) {
				opt.setAttribute('selected', 'true');
				break;
			}
		}

		var extras = 1;
		while(extras != allInterests.length) {
			var nextInterest = fieldOfInterest.cloneNode(true);
			nextInterest.id = 'field-of-interest-' + num;

			var opts = nextInterest.options;
			//alert(opts[1].value);
			for (var i = 0; opt = opts[i]; i++) {
				if (opt.value == allInterests[extras]) {
					opt.setAttribute('selected', 'true');
					break;
				}
			}

			num += 1;

			add_another_interest.innerHTML = add_another_interest.innerHTML + nextInterest.outerHTML;
			extras += 1;
		}
		add_another_interest.removeAttribute("hidden");
		add_another_interest_button.removeAttribute("hidden");

	}

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

	var nonEditStuff = document.getElementsByClassName('nonEditMode');

	for (var i = 0; i < nonEditStuff.length; i++) {
		nonEditStuff[i].style.display = 'none';
	}

	var save = document.getElementById('saveButton');
	save.removeAttribute("hidden");

}

function enableEditOrganization() {
	var elements = document.getElementsByClassName('enableEdit');

	for (var i = 0; i < elements.length; i++) {
		elements[i].removeAttribute('readonly');
	}

	var city_change = document.getElementById('changeCity');
	city_change.removeAttribute("hidden");

	var opts = city_change.options;
	for (var i = 0; opt = opts[i]; i++) {
		if (opt.value == document.getElementById('city').value) {
			opt.setAttribute('selected', 'true');
			break;
		}
	}

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


	var nonEditStuff = document.getElementsByClassName('nonEditMode');

	for (var i = 0; i < nonEditStuff.length; i++) {
		nonEditStuff[i].style.display = 'none';
	}

	var save = document.getElementById('saveButton');
	save.removeAttribute("hidden");


	var element = document.getElementById('editContent');

	element.innerHTML = "<button type='button' onClick='cancelChanges()'>Cancel</button>";

}
	


function enableEditProgram() {

	var elements = document.getElementsByClassName('enableEdit');

	for (var i = 0; i < elements.length; i++) {
		elements[i].removeAttribute('readonly');
	}

	var new_organization = document.getElementById('newOrganization');
	new_organization.removeAttribute('hidden');


	var new_interest = document.getElementById('newInterest');
	new_interest.removeAttribute('hidden');


	var nonEditStuff = document.getElementsByClassName('nonEditMode');

	for (var i = 0; i < nonEditStuff.length; i++) {
		nonEditStuff[i].style.display = 'none';
	}

	var save = document.getElementById('saveButton');
	save.removeAttribute("hidden");


	var element = document.getElementById('editContent');

	element.innerHTML = "<button type='button' onClick='cancelChanges()'>Cancel</button>";

}








//change editable function to false, and revert back to old values.
function cancelChanges() {
	window.location.reload();	
	return;

	var elements = document.getElementsByClassName('enableEdit');

	for (var i = 0; i < elements.length; i++) {
		elements[i].readOnly = 'true';

		elements[i].value = oldValues[i];
	}

	var element = document.getElementById('editContent');
	
	element.innerHTML = "<button type='button' onClick='enableEdit()'>Edit</button><br>"
	
}

function saveChanges() {
	var elements = document.getElementsByClassName('enableEdit');

	let data = {
		id: elements[0],
		first_name: elements[1],
		last_name: elements[2],
		phone_number: elements[3],
		email: elements[4],
		address: elements[5],
		school_district: elements[6],
		school: elements[7],
		interest: elements[8],
		assessment: elements[9],
		notes: elements[10]
	}
  alert("saveChanges data = " + data);

	fetch("/student/update/", {
  	method: "POST",
  	headers: {'Content-Type': 'application/json'},
  	body: JSON.stringify(data)
	}).then(res => {
  	console.log("Request complete! response:", res);
	});

}


function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');



function deleteInterest(interest) {
	document.getElementById('interest_' + interest).remove();
	
		fetch('', {
			method: 'POST',
			headers: {
				'X-CSRFToken': csrftoken,
				'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
			},
			body: new URLSearchParams({
        'interest': interest
    	})
		})
	
}











