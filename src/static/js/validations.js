$(document).ready(function(){
  $(":input").inputmask();
  or
  Inputmask().mask(document.querySelectorAll("input"));
});

function isSecondPasswordEqual(input) {
	pw1 = document.getElementById("password");
	if(input.value != pw1.value) {
		input.setCustomValidity('Пароли должны совпадать!');
	}
	else {
		input.setCustomValidity('');
	}
}

function isFirstPasswordEqual(input) {
	pw2 = document.getElementById("repeat_password");
	if(input.value != pw2.value) {
		pw2.setCustomValidity('Пароли должны совпадать!');
	}
	else {
		pw2.setCustomValidity('');
	}
}