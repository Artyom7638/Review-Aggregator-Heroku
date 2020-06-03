var maxWidth = 0;
var maxHeight = 0;
var uploaded = null;
var loadedW = 0, loadedH = 0;

var loadFile = function(event) {
	var preview = document.getElementById("preview");
	var blob = URL.createObjectURL(event.target.files[0]);
	url_ = blob;
	var url = 'url("' + blob + '")';
	preview.style.backgroundImage = url;
	preview.style.display = "flex";

	var filler = document.getElementById("filler");
	filler.style.display = "none";
	uploaded = preview;

	var img = new Image();
	img.onload = function() { 
		loadedW = this.naturalWidth;
		loadedH = this.naturalHeight;
		resizeImage();
	}
	img.src = blob;
}


function resizeImage() {
	if(uploaded == null)
		return;

	var curH = $(window).height();
	var curW = $(document).width();

	if(curW > maxWidth)
		maxWidth = curW;
	if(curH > maxHeight)
		maxHeight = curH;

	var photo = uploaded;

	var parent = document.getElementById("imgParent");

	if(loadedH > maxHeight * 0.8) {
		photo.style.removeProperty("height");
		photo.style.paddingTop = (curH / maxHeight) * 100 + "%";
	}
	else {
		photo.style.height = loadedH + "px";
	}

	if(loadedW > parent.offsetWidth){
		photo.style.width = "100%";
	}
	else {
		photo.style.width = loadedW * (curW / maxWidth) + "px";
		photo.style.removeProperty("padding-top");
	}
}

$(document).ready(function() {
	maxWidth = $(document).width();
	maxHeight = $(window).height();
	window.onresize = resizeImage;
});