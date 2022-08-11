window.onload=function(){

const fname = document.getElementById('fname');
const lname = document.getElementById('lname');
const dob = document.getElementById('dob') ;
const email = document.getElementById('email');
const phone = document.getElementById('phone');
const form = document.getElementById('form');

form.addEventListener('submit', (e) => {
	let errors = 0

	if (fname.value == '' || fname.value == null) {
		errors++
		error(fname, "First name cannot be empty")
	}
	else {
		success(fname)
	}



	if (lname.value == '' || lname.value == null) {
		errors++
		error(lname, "Last name cannot be empty")
	}
	else {
		success(lname)
	}

	if (dob.value == '' || dob.value == null) {
		errors++
		error(dob, "date of birth is required")
	}
	else {
		success(dob)
	}

	if (email.value == '' || email.value == null) {
		errors++
		error(email, "Please enter a valid email")
	}
	else {
		success(email)
	}

	if (phone.value == '' || phone.value == null) {
		errors++
		error(phone, "contact number is required")
	}
	else {
		success(phone)
	}

	if (errors>0){
		e.preventDefault();
	}

	console.log(errors)

})

function error(input, message) {
	input.className = 'form-control is-invalid'
	const parentdiv = input.parentElement;
	parentdiv.className = 'form-group row invalid';
	const small = parentdiv.querySelector('small');
	small.innerText = message;
}

function success(input) {
	input.className = 'form-control is-valid'
	const parentdiv = input.parentElement;
	parentdiv.className = 'form-group row';
}


}


