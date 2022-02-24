function nextPage() {
  var num = document.getElementById('page_num').innerHTML;

  fetch('', {
    method: 'POST',
    headers: {
      'X-CSRFToken': csrftoken,
      'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
    },
    body: new URLSearchParams({
      'action': 'next_page',
      'current_page': num,
    })
  })	
  .then(response => response.json())
	.then(data => {
    if (data.students.length > 0) { 
	    num  = (parseInt(num)+1);
      document.getElementById('page_num').innerHTML = num;
    }
    document.getElementById('prev_page').disabled = num < 1;
    document.getElementById('next_page').disabled = !data.hasNext;

    //for (var i=0;mentor=data.mentors[i];i++) {
    table = document.getElementById('student-search-table');
    var i=0;
    var len = table.getElementsByTagName('tr').length;
    while (i < len-1) { 
      table.deleteRow(1);
      i += 1;
    }

    for (var i=0;i<data.students.length;i++) { 
      var newRow = table.insertRow(-1);
      var firstCell = newRow.insertCell();
      var secondCell = newRow.insertCell();
      var thirdCell = newRow.insertCell();

      firstCell.innerHTML = "<a style='text-decoration:none' href=\"/student/profile/" + data.students[i].id + "\">" + data.students[i].first_name + " " + data.students[i].last_name + "</a>";
      secondCell.innerHTML = "<a style='text-decoration:none' href=\"/student/profile/" + data.students[i].id + "\">" + data.students[i].phone_number + "</a>";
      thirdCell.innerHTML = "<a style='text-decoration:none' href=\"/student/profile/" + data.students[i].id + "\">" + data.students[i].email + "</a>";
    }

	});

}

function lastPage() {
  var num = document.getElementById('page_num').innerHTML;
  if (parseInt(num) > 1) {
    fetch('', {
      method: 'POST',
      headers: {
        'X-CSRFToken': csrftoken,
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
      },
      body: new URLSearchParams({
        'action': 'prev_page',
        'current_page': num,
      })
    })	
    .then(response => response.json())
    .then(data => {

      if (parseInt(num) > 1) { 
        num  = (parseInt(num)-1);
        document.getElementById('page_num').innerHTML = num;
      }
      document.getElementById('prev_page').disabled = num <= 1;
      document.getElementById('next_page').disabled = !data.hasNext;
      
      table = document.getElementById('student-search-table');
      var i=0;
      var len = table.getElementsByTagName('tr').length;
      while (i < len-1) { 
        table.deleteRow(1);
        i += 1;
      }

      for (var i=0;i<data.students.length;i++) { 
        var newRow = table.insertRow(-1);
        var firstCell = newRow.insertCell();
        var secondCell = newRow.insertCell();
        var thirdCell = newRow.insertCell();

        firstCell.innerHTML = "<a style='text-decoration:none' href=\"/student/profile/" + data.students[i].id + "\">" + data.students[i].first_name + " " + data.students[i].last_name + "</a>";
        secondCell.innerHTML = "<a style='text-decoration:none' href=\"/student/profile/" + data.students[i].id + "\">" + data.students[i].phone_number + "</a>";
        thirdCell.innerHTML = "<a style='text-decoration:none' href=\"/student/profile/" + data.students[i].id + "\">" + data.students[i].email + "</a>";
      }

    });
  }
}
