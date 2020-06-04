var lastStar;
var starBar;
var scoreSet = false;
var clicked = null;
var maxWidth = 0;
var maxHeight = 0;

function switchReviews(show, hide) {
	var title_show = document.getElementById(show + "_title");
	var block_show = document.getElementById(show);

	var title_hide = document.getElementById(hide + "_title");
	var block_hide = document.getElementById(hide);

	title_show.style.fontWeight = "bold";
	title_hide.style.fontWeight = "normal";

	block_show.style.display = "flex";
	block_hide.style.display = "none";


	var pagination_show = document.getElementById(show + "_pagination");
	var pagination_hide = document.getElementById(hide + "_pagination");
	pagination_show.style.display = "block";
	pagination_hide.style.display = "none";
}

function switchBlock(id, state) {
	var block = document.getElementById(id);
	block.style.display = state;
}

function showPhoto(clickedElement, link) {
	var a = document.getElementById( "delete_link");
	if (a)
		{a.href = link;}

	window.onresize = resizeImage;
	clicked = clickedElement;

	var curH = $(window).height();
	var curW = $(document).width();

	if(curW > maxWidth)
		maxWidth = curW;
	if(curH > maxHeight)
		maxHeight = curH;

	var body = document.body;
	body.style.overflow = "hidden";
	body.scroll = "no";

	var preview = document.getElementById("preview");
	preview.style.display = "block";

	var photo = document.getElementById("photo");
	var newPadTop = 0;
	photo.style.backgroundImage = clickedElement.style.backgroundImage;

	var img = new Image();
	var url = clickedElement.style.backgroundImage;
	img.src = url.replace(/url\((['"])?(.*?)\1\)/gi, '$2');
	var parent = document.getElementById("imgParent");

	if (img.height > maxHeight * 0.8) {
		photo.style.removeProperty("height");
		var h = curH > maxHeight ? maxHeight : curH;
		newPadTop = h - h * 0.10 - 50;
		photo.style.paddingTop = newPadTop + "px";
		if(newPadTop > curH * 0.9){
			photo.style.paddingTop = curH * 0.9 + "px";
		}
	}
	else {
		photo.style.height = img.height  + "px";
		photo.style.removeProperty("padding-top");
	}


	if (img.width > parent.offsetWidth){
		photo.style.width = "100%";
	}
	else {
		photo.style.width = img.width * (parent.width / maxWidth) + "px";
	}

	if(photo.style.width == "" || photo.style.width == "0px"){
		photo.style.width = img.width > maxWidth * 0.7 ? maxWidth * 0.7 : img.width + "px";
	}

	if(photo.style.height == "" || photo.style.height == "0px") {
		photo.style.width = img.height > maxHeight * 0.7 ? maxHeight * 0.7 : img.height + "px";
	}
}

function hidePhoto() {
	var body = document.body;
	body.style.overflow = "scroll";
	body.scroll = "yes";
	var photo = document.getElementById("photo");
	photo.style.removeProperty("height");
	photo.style.removeProperty("width");
	photo.style.removeProperty("padding-top");
	var preview = document.getElementById("preview");
	preview.style.display = "none";
	clicked = null;
}

function highlightStars() {
	if (starBar == null)
		return;

	starBar.style.width = (28 * lastStar).toString() + "px";
}

function setLastStar(star) {
	if(scoreSet)
		return;
	lastStar = Number(star.id.substring(1, 2));
	highlightStars();
}

function submitScore(star) {
	if(scoreSet){
		scoreSet = false;
		setLastStar(star);
		return;
	}
	var scoreHolder = document.getElementById("rating");
	console.log(lastStar);
	console.log(scoreHolder);
	if (scoreHolder != null && lastStar >= 1 && lastStar <= 5) {
		scoreHolder.value = lastStar;
		scoreSet = true;
	}
}

function setDeleteInfo(link) {
	var btn = document.getElementById("deleteReviewConfirm");
	if(btn == null)
		return;

	$("#deleteReviewConfirm").click(function(){ window.location.href=link; });
	/*
	function redirect() {
	  fetch(link);
	}
	btn.on( "click", redirect );

	btn.onclick = function() { fetch(link); };*/
}


function setBlockInfo(link) {
	var btn = document.getElementById("blockUserConfirm");
	if(btn == null)
		return;

	$("#blockUserConfirm").click(function(){ window.location.href=link; });
	// btn.onclick = function() { fetch(link); };
}

function resizeImage() {
	if(clicked == null)
		return;

	//alert("resize called");

	var curH = $(window).height();
	var curW = $(document).width();

	if(curW > maxWidth)
		maxWidth = curW;
	if(curH > maxHeight)
		maxHeight = curH;

	var photo = document.getElementById("photo");
	var newPadTop = 0;
	var img = new Image();
	var url = clicked.style.backgroundImage;
	img.src = url.replace(/url\((['"])?(.*?)\1\)/gi, '$2');
	var parent = document.getElementById("imgParent");

	if (curH > maxHeight){
		if (img.height > maxHeight * 0.8) {
			photo.style.removeProperty("height");
			newPadTop = maxHeight - maxHeight * 0.10 - 50;
			photo.style.paddingTop = newPadTop + "px";
			if(newPadTop > curH * 0.9){
				photo.style.paddingTop = curH * 0.9 + "px";
				//alert("!");
			}
		}
		else {
			photo.style.height = img.height  + "px";
			photo.style.removeProperty("padding-top");
			if(photo.style.height == "0px"){
				photo.style.height = curH * 0.8 + "px";
				//alert("!!");
			}
		}
	}
	else {
		if (img.height > curH * 0.8) {
			photo.style.removeProperty("height");
			newPadTop = curH - curH * 0.10 - 50;
			photo.style.paddingTop = newPadTop + "px";
			if(newPadTop > curH * 0.9){
				photo.style.paddingTop = curH * 0.9 + "px";
				//alert("!!!");
			}
		}
		else {
			photo.style.height = img.height  + "px";
			photo.style.removeProperty("padding-top");
			if(photo.style.height == "0px"){
				photo.style.height = curH * 0.8 + "px";
				//alert("!!!!");
			}
		}
	}

	if(img.width > parent.offsetWidth){
		photo.style.width = "100%";
	}
	else {
		photo.style.width = img.width * (parent.width / maxWidth) + "px";
	}
}

$(document).ready(function() {
	starBar = document.getElementById("bright-stars");
	maxWidth = $(document).width();
	maxHeight = $(window).height();
});