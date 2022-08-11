window.onload=function(){

const subject = document.getElementById('subject');
const body = document.getElementById('content');
const emails = document.getElementsByTagName("input").type == "checkbox";
const form = document.getElementById('form');


// document.getElementById("myText").value = "your string"; 


form.addEventListener('submit', (e) => {
	let errors = 0


	if (subject.value == '' || subject.value == null) {
		errors++
		error(subject, "Please mention Subject")
	}
	else {
		success(subject)
	}



	if (body.value == '' || body.value == null) {
		errors++
		error(body, "Body name cannot be empty")
	}
	else {
		success(body)
	}


	// let submit=false;
 //    for(let i=0,l=emails.length;i<l;i++)
 //    {
 //        if(emails[i].checked)
 //        {
 //            submit=true;
 //            break;
 //        }
 //    }
 //    if(submit){}
 //    else{
 //    	errors++;
 //    	alert("Please select atleast one customer")
 //    }
 	var checkboxes = document.querySelectorAll('input[type="checkbox"]');
	var checkedOne = Array.prototype.slice.call(checkboxes).some(x => x.checked);

 	if (checkedOne == false || checkedOne == null){
 		errors++
 		alert("Please select atleast one customer")
 	}

	

	

	if (errors>0){
		e.preventDefault();
	}

	// console.log(errors)

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