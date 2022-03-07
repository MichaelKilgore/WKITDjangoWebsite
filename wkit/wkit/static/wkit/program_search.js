function programNextPage() {
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
    if (data.programs.length > 0) { 
	    num  = (parseInt(num)+1);
      document.getElementById('page_num').innerHTML = num;
    }
    document.getElementById('prev_page').disabled = num < 1;
    document.getElementById('next_page').disabled = !data.hasNext;

    //for (var i=0;mentor=data.mentors[i];i++) {
    table = document.getElementById('program-search-table');
    var i=0;
    var len = table.getElementsByTagName('tr').length;
    while (i < len-1) { 
      table.deleteRow(1);
      i += 1;
    }

    for (var i=0;i<data.programs.length;i++) { 
      var newRow = table.insertRow(-1);
      var firstCell = newRow.insertCell();
      var secondCell = newRow.insertCell();
      var thirdCell = newRow.insertCell();

      firstCell.innerHTML = "<a style='text-decoration:none' href=\"/program/profile/" + data.programs[i].id + "\">" + data.programs[i].program_name + "</a";
      secondCell.innerHTML = "<a style='text-decoration:none' href=\"/program/profile/" + data.programs[i].id + "\">" + data.programs[i].city + "</a";
      thirdCell.innerHTML = "<a style='text-decoration:none' href=\"/program/profile/" + data.programs[i].id + "\">" + data.programs[i].interest + "</a";
    }

	});

}

function programLastPage() {
  var num = document.getElementById('page_num').innerHTML;
  if (parseInt(num) > 0) {
    fetch('', {
      method: 'POST',
      headers: {
        'X-CSRFToken': csrftoken,
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
      },
      body: new URLSearchParams({
        'action': 'last_page',
        'current_page': num,
      })
    })	
    .then(response => response.json())
    .then(data => {
      
      if (parseInt(num) > 0) { 
        num  = (parseInt(num)-1);
        document.getElementById('page_num').innerHTML = num;
      }
      document.getElementById('prev_page').disabled = num <= 1;
      document.getElementById('next_page').disabled = !data.hasNext;
      
      table = document.getElementById('program-search-table');
      var i=0;
      var len = table.getElementsByTagName('tr').length;
      while (i < len-1) { 
        table.deleteRow(1);
        i += 1;
      }

      for (var i=0;i<data.programs.length;i++) { 
        var newRow = table.insertRow(-1);
        var firstCell = newRow.insertCell();
        var secondCell = newRow.insertCell();
        var thirdCell = newRow.insertCell();

        firstCell.innerHTML = "<a style='text-decoration:none' href=\"/program/profile/" + data.programs[i].id + "\">" + data.programs[i].program_name + "</a";
        secondCell.innerHTML = "<a style='text-decoration:none' href=\"/program/profile/" + data.programs[i].id + "\">" + data.programs[i].city + "</a";
        thirdCell.innerHTML = "<a style='text-decoration:none' href=\"/program/profile/" + data.programs[i].id + "\">" + data.programs[i].interest + "</a";
      }

    });
  }

}
