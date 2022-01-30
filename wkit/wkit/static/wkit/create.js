
function addAnotherField() {
	var num = 5;
	while (num>1) {
		var element = document.getElementById("field-of-interest-"+num);

		if (element) {
			break;
		}

		num -= 1;

	}
	num += 1;

	if (num != 6) {
		var element = document.getElementById('add-another-interest');

		var fieldOfInterest = document.getElementById('field-of-interest-1');

		var newField = fieldOfInterest.cloneNode(true);

		newField.id = 'field-of-interest-' + num;


		element.innerHTML = element.innerHTML + "<br id='div-field-of-interest-" + num + "'>" + newField.outerHTML;
		num += 1;
	}
}

function removeField() {
	var element = document.getElementById('add-another-interest');

	var numtwo = 5;
	
	while (numtwo != 1) {	
		var element = document.getElementById("field-of-interest-"+numtwo);

		if (element) {
			element.outerHTML = "";
			var div_element = document.getElementById("div-field-of-interest-"+numtwo);
			div_element.outerHTML = "";
			break;
		}

			numtwo -= 1;
	}
}

