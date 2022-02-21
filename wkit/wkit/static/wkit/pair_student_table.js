function nextPage() {
  var id = document.getElementById('mentor_id').value;
  var num = document.getElementById('page_num').innerHTML;

  fetch('', {
    method: 'POST',
    headers: {
      'X-CSRFToken': csrftoken,
      'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
    },
    body: new URLSearchParams({
      'next_page': num,
    })
  })	
  .then( (response) => {
    if (response.status === 500) {
      return {};
    } else {
      return response.json();
    }
   })
	.then(data => {
    if (data.students == null) {
      return;
    }
    if (data.students.length > 0) { 
	    num  = (parseInt(num)+1);
      document.getElementById('page_num').innerHTML = num;
    }

    //for (var i=0;mentor=data.mentors[i];i++) {
    table = document.getElementById('student-search-table');
    var i=0;
    var len = table.getElementsByTagName('tr').length;
    while (i < len-1) { 
      table.deleteRow(1);
      i += 1;
    }

    for (var i=0;i<data.students.length;i++) { 
      var newRow = table.insertRow(1); 
      var firstCell = newRow.insertCell();
      var secondCell = newRow.insertCell();
      var thirdCell = newRow.insertCell();
			var fourthCell = newRow.insertCell();

      var fullName = data.students[i].first_name + " " + data.students[i].last_name;
      firstCell.innerHTML = "<a style='text-decoration:none' href=\"/student/profile/" + data.students[i].id + "\">" + data.students[i].first_name + " " + data.students[i].last_name + "</a>";
      secondCell.innerHTML = "<a style='text-decoration:none' href=\"/student/profile/" + data.students[i].id + "\">" + data.students[i].phone_number + "</a>";
      thirdCell.innerHTML = "<a style='text-decoration:none' href=\"/student/profile/" + data.students[i].id + "\">" + data.students[i].email + "</a>";
			fourthCell.innerHTML = "<button onClick=\"pairStudent('"+ id + "', '"  + data.students[i].id + "', '" + fullName + "', '" + newRow.rowIndex + "')\">Pair</button";
    }

	});

}

function lastPage() {
  var id = document.getElementById('mentor_id').value;
  var num = document.getElementById('page_num').innerHTML;
  if (parseInt(num) > 0) {
    fetch('', {
      method: 'POST',
      headers: {
        'X-CSRFToken': csrftoken,
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
      },
      body: new URLSearchParams({
        'last_page': num,
      })
    })	
    .then( (response) => {
    if (response.status === 500) {
      return {};
    } else {
      return response.json();
    }
   })
	.then(data => {
      if (data.students == null) {
        return;
      } 
      if (parseInt(num) > 0) { 
        num  = (parseInt(num)-1);
        document.getElementById('page_num').innerHTML = num;
      }
      
      table = document.getElementById('student-search-table');
      var i=0;
      var len = table.getElementsByTagName('tr').length;
      while (i < len-1) { 
        table.deleteRow(1);
        i += 1;
      }

      for (var i=0;i<data.students.length;i++) { 
        var newRow = table.insertRow(1); 
        var firstCell = newRow.insertCell();
        var secondCell = newRow.insertCell();
        var thirdCell = newRow.insertCell();
	      var fourthCell = newRow.insertCell();

        var fullName = data.students[i].first_name + " " + data.students[i].last_name;
        firstCell.innerHTML = "<a style='text-decoration:none' href=\"/student/profile/" + data.students[i].id + "\">" + data.students[i].first_name + " " + data.students[i].last_name + "</a>";
        secondCell.innerHTML = "<a style='text-decoration:none' href=\"/student/profile/" + data.students[i].id + "\">" + data.students[i].phone_number + "</a>";
        thirdCell.innerHTML = "<a style='text-decoration:none' href=\"/student/profile/" + data.students[i].id + "\">" + data.students[i].email + "</a>";
        fourthCell.innerHTML = "<button onClick=\"pairStudent('"+ id + "', '"  + data.students[i].id + "', '" + fullName + "', '" + newRow.rowIndex + "')\">Pair</button";
      }

    });
  }

}
