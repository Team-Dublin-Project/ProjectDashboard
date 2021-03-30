/* When the user clicks on the button, 
toggle between hiding and showing the dropdown content */
function OpenSettings() {
	event.stopPropagation();
	document.getElementById("mySettings").classList.toggle("show");
 }

// Close the dropdown if the user clicks outside of it
// Close the dropdown menu if the user clicks outside of it
	window.onclick = function(event) {
	document.getElementById("mySettings").classList.remove("show");
}