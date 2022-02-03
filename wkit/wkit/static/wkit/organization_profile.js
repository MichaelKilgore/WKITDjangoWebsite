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

