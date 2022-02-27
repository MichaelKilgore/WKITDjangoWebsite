function mentorNextPage(student_id = null) {
  var num = document.getElementById('mentors_page_num').innerHTML;

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
    if (data.mentors.length > 0) { 
	    num  = (parseInt(num)+1);
      document.getElementById('mentors_page_num').innerHTML = num;
    }
    document.getElementById('prev_page').disabled = num < 1;
    document.getElementById('next_page').disabled = !data.hasNext;

    //for (var i=0;mentor=data.mentors[i];i++) {
    table = document.getElementById('mentor-search-table');
    var i=0;
    var len = table.getElementsByTagName('tr').length;
    while (i < len-1) { 
      table.deleteRow(1);
      i += 1;
    }

    for (var i=0;i<data.mentors.length;i++) {
      var newRow = table.insertRow(-1);
      var firstCell = newRow.insertCell();
      var secondCell = newRow.insertCell();
      var thirdCell = newRow.insertCell();
      var fourthCell = null;
      if (student_id != null) {
        fourthCell = newRow.insertCell();
      }

      var mentor = data.mentors[i];
      var fullName = mentor.first_name + " " + mentor.last_name;
      firstCell.innerHTML = "<a style='text-decoration:none' href=\"/mentor/profile/" + mentor.id + "\">" + fullName + "</a>";
      secondCell.innerHTML = "<a style='text-decoration:none' href=\"/mentor/profile/" + mentor.id + "\">" + mentor.phone_number + "</a>";
      thirdCell.innerHTML = "<a style='text-decoration:none' href=\"/mentor/profile/" + mentor.id + "\">" + mentor.email + "</a>";
      if (student_id != null) {
        fourthCell.innerHTML = "<button onClick=\"pairMentor('"+ student_id + "', '"  + mentor.id + "', '" + fullName + "', '" + newRow.rowIndex + "')\">Pair</button>"; 
      }
    }

	});

}

function mentorLastPage(student_id) {
  var num = document.getElementById('mentors_page_num').innerHTML;
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
        document.getElementById('mentors_page_num').innerHTML = num;
      }
      document.getElementById('prev_page').disabled = num <= 1;
      document.getElementById('next_page').disabled = !data.hasNext;
      
      table = document.getElementById('mentor-search-table');
      var i=0;
      var len = table.getElementsByTagName('tr').length;
      while (i < len-1) { 
        table.deleteRow(1);
        i += 1;
      }

      for (var i=0;i<data.mentors.length;i++) {
        var newRow = table.insertRow(-1);
        var firstCell = newRow.insertCell();
        var secondCell = newRow.insertCell();
        var thirdCell = newRow.insertCell();
        var fourthCell = null;
        if (student_id != null) {
          fourthCell = newRow.insertCell();
        }

        var mentor = data.mentors[i];
        var fullName = mentor.first_name + " " + mentor.last_name;
        firstCell.innerHTML = "<a style='text-decoration:none' href=\"/mentor/profile/" + mentor.id + "\">" + fullName + "</a>";
        secondCell.innerHTML = "<a style='text-decoration:none' href=\"/mentor/profile/" + mentor.id + "\">" + mentor.phone_number + "</a>";
        thirdCell.innerHTML = "<a style='text-decoration:none' href=\"/mentor/profile/" + mentor.id + "\">" + mentor.email + "</a>";
        if (student_id != null) {
          fourthCell.innerHTML = "<button onClick=\"pairMentor('"+ student_id + "', '"  + mentor.id + "', '" + fullName + "', '" + newRow.rowIndex + "')\">Pair</button>"; 
        }
      }

    });
  }
}
