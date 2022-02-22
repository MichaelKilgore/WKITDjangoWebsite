function scholarshipNextPage() {
  var num = document.getElementById('page_num').innerHTML;

  fetch('', {
    method: 'POST',
    headers: {
      'X-CSRFToken': csrftoken,
      'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
    },
    body: new URLSearchParams({
      'next_page': num,
      'scholarship': true,
    })
  })	
  .then(response => response.json())
	.then(data => {
    if (data.students.length > 0) { 
	    num  = (parseInt(num)+1);
      document.getElementById('page_num').innerHTML = num;
    }

    table = document.getElementById('scholarship-search-table');
    var i=0;
    var len = table.getElementsByTagName('tr').length;
    while (i < len-1) { 
      table.deleteRow(1);
      i += 1;
    }

    for (var i=0;i<data.scholarships.length;i++) { 
      var newRow = table.insertRow(1); 
      var firstCell = newRow.insertCell();
      var secondCell = newRow.insertCell();

      firstCell.innerHTML = "<a style='text-decoration:none' href=\"/scholarship/profile/" + data.scholarships[i].id + "\">" + data.scholarships[i].scholarship_name + "</a>";
      secondCell.innerHTML = "<a style='text-decoration:none' href=\"/scholarship/profile/" + data.scholarships[i].id + "\">" + data.scholarships[i].amount + "</a>";
   }
	});

}

function scholarshipLastPage() {
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
        'scholarship': true,
      })
    })	
    .then(response => response.json())
    .then(data => {
      
      if (parseInt(num) > 0) { 
        num  = (parseInt(num)-1);
        document.getElementById('page_num').innerHTML = num;
      }
      
      table = document.getElementById('scholarship-search-table');
      var i=0;
      var len = table.getElementsByTagName('tr').length;
      while (i < len-1) { 
        table.deleteRow(1);
        i += 1;
      }

      for (var i=0;i<data.scholarships.length;i++) { 
        var newRow = table.insertRow(1); 
        var firstCell = newRow.insertCell();
        var secondCell = newRow.insertCell();

        firstCell.innerHTML = "<a style='text-decoration:none' href=\"/scholarship/profile/" + data.scholarships[i].id + "\">" + data.scholarships[i].scholarship_name + "</a>";
        secondCell.innerHTML = "<a style='text-decoration:none' href=\"/scholarship/profile/" + data.scholarships[i].id + "\">" + data.scholarships[i].amount + "</a>";
      }

    });
  }

}
