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
    if (data.interests.length > 0) { 
	    num  = (parseInt(num)+1);
      document.getElementById('page_num').innerHTML = num;
    }
    document.getElementById('prev_page').disabled = num < 1;
    document.getElementById('next_page').disabled = !data.hasNext;

    //for (var i=0;mentor=data.mentors[i];i++) {
    table = document.getElementById('interest-search-table');
    var i=0;
    var len = table.getElementsByTagName('tr').length;
    while (i < len-1) { 
      table.deleteRow(1);
      i += 1;
    }

    for (var i=0;i<data.interests.length;i++) { 
      var newRow = table.insertRow(-1);
      var firstCell = newRow.insertCell();
      var secondCell = newRow.insertCell();

      firstCell.innerHTML = data.interests[i].interest;
      secondCell.innerHTML = "<button style=\"margin: auto; text-align: center; color: red;\" onclick=\"deleteInterest('" + data.interests[i].interest + "')\">delete</button>";
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
      
      table = document.getElementById('interest-search-table');
      var i=0;
      var len = table.getElementsByTagName('tr').length;
      while (i < len-1) { 
        table.deleteRow(1);
        i += 1;
      }

      for (var i=0;i<data.interests.length;i++) { 
        var newRow = table.insertRow(-1);
        var firstCell = newRow.insertCell();
        var secondCell = newRow.insertCell();

        firstCell.innerHTML = data.interests[i].interest;
        secondCell.innerHTML = "<button style=\"margin: auto; text-align: center; color: red;\" onclick=\"deleteInterest('" + data.interests[i].interest + "')\">delete</button>";
      }
    });
  }

}

function deleteInterest(interest) {
	document.getElementById('interest_' + interest).remove();
	
		fetch('', {
			method: 'POST',
			headers: {
				'X-CSRFToken': csrftoken,
				'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
			},
			body: new URLSearchParams({
        'delete': 'interest',
        'interest': interest
    	})
		})
}

