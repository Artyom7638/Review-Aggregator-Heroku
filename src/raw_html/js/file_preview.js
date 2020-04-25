var loadFile = function(event) {
	var preview = document.getElementById("preview");
	var url = URL.createObjectURL(event.target.files[0]);
	preview.style.backgroundImage = 'url("' + url + '")';
	preview.style.display = "flex";

	var filler = document.getElementById("filler");
	filler.style.display = "none";
}