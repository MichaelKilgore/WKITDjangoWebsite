function cancelChanges() {
  revertEnableEditChanges();	
	toggleEditReadOnly();
	changeEditButtonToCancelButton();

  toggleEditOrgType();
  toggleEditCity();

  toggleSaveOption();
	toggleNonEditMode();

  editMode = false;
}

function enableEdit() {
  setOldValues();

  toggleEditReadOnly();
	changeEditButtonToCancelButton();

  //not done
  toggleEditOrgType();
  toggleEditCity();

  toggleSaveOption();
	toggleNonEditMode();

  editMode = true;
}

function deleteOrganization(id) {
  let isExecuted = confirm("Are you sure you would like to delete this user?");

	if (isExecuted) {
		fetch('', {
			method: 'POST',
			headers: {
				'X-CSRFToken': csrftoken,
				'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
			},
			body: new URLSearchParams({
				'delete': 'delete',
        'id': id
    	})
		})

		location.href="/";
	}
}
