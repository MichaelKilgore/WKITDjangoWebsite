
// does not keep fields old state
function addAnotherField() {
	var num = 5;
  //figures out what the next number element is to add.
	while (num>1) {
		var element = document.getElementById("field-of-interest-"+num);

		if (element) {
			break;
		}

		num -= 1;

	}
	num += 1;

  var oldValues = ['', '', '', '', ''];
	if (num != 6) {
    //get old values
    for (var i=0; i<num-1; i++) {
      oldValues[i] = document.getElementById('field-of-interest-'+(i+1)).value;
    } 


		var element = document.getElementById('add-another-interest');

		var fieldOfInterest = document.getElementById('field-of-interest-1');

		var newField = fieldOfInterest.cloneNode(true);

		newField.id = 'field-of-interest-' + num;


		element.innerHTML = element.innerHTML + "<br id='div-field-of-interest-" + num + "'>" + newField.outerHTML;
		num += 1;

    // basically helps the other field of interests keep there state.
    for (var i=0; i<num-2; i++) {
      var fieldOfInterest = document.getElementById('field-of-interest-'+(i+1));

      var opts = fieldOfInterest.options;
			for (var j = 0; opt = opts[j]; j++) {
				if (opt.value == oldValues[i]) {
					opt.setAttribute('selected', 'true');
					break;
			  }
		  }

    } //: FOR

	} //: IF

}

// does not keep fields old state
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

