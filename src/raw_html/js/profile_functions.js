var lastStar;
var starBar;
var scoreSet = false;

function switchReviews(show, hide) {
	var title_show = document.getElementById(show + "_title");
	var block_show = document.getElementById(show);

	var title_hide = document.getElementById(hide + "_title");
	var block_hide = document.getElementById(hide);

	title_show.style.fontWeight = "bold";
	title_hide.style.fontWeight = "normal";

	block_show.style.display = "flex";
	block_hide.style.display = "none";
}

function switchBlock(id, state) {
	var block = document.getElementById(id);
	block.style.display = state;
}

function showPhoto(clickedElement) {
	var body = document.body;
	body.style.overflow = "hidden";
	body.scroll = "no";

	var preview = document.getElementById("preview");
	preview.style.display = "block";

	var photo = document.getElementById("photo");
	photo.style.backgroundImage = clickedElement.style.backgroundImage;
}

function hidePhoto() {
	var body = document.body;
	body.style.overflow = "scroll";
	body.scroll = "yes";

	var preview = document.getElementById("preview");
	preview.style.display = "none";
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
	var scoreHolder = document.getElementById("score_holder");
	console.log(lastStar);
	console.log(scoreHolder);
	if (scoreHolder != null && lastStar >= 1 && lastStar <= 5) {
		scoreHolder.value = lastStar;
		scoreSet = true;
	}
}

$(document).ready(function() {
	starBar = document.getElementById("bright-stars");
});