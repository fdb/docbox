function lbInit() {
	var objBody = document.getElementsByTagName("body").item(0);

	// create overlay div and hardcode some functional styles (aesthetic styles are in CSS file)
	var objOverlay = document.createElement("div");
	objOverlay.setAttribute('id','lbOverlay');
	objOverlay.style.display = 'none';
	objOverlay.style.position = 'absolute';
	objOverlay.style.top = '0';
	objOverlay.style.left = '0';
	objOverlay.style.zIndex = '90';
	objOverlay.style.width = '100%';
	objBody.insertBefore(objOverlay, objBody.firstChild);
}

function lbShow(contentDiv) {
	var objOverlay = document.getElementById('lbOverlay');

	var arrayPageSize = lbGetPageSize();
	var arrayPageScroll = lbGetPageScroll();

	// set height of Overlay to take up whole page and show
	objOverlay.style.height = (arrayPageSize[1] + 'px');
	objOverlay.style.display = 'block';

	contentDiv.style.position = 'absolute';
	contentDiv.style.zIndex = '120';
	
	var w = parseInt(contentDiv.style.width) || 0;
	var h = parseInt(contentDiv.style.height) || 0;
	// console.log(w, h);
	
	// center lightbox and make sure that the top and left values are not negative
	// and the image placed outside the viewport
	var lightboxTop = arrayPageScroll[1] + ((arrayPageSize[3] - 35 - h) / 2);
	var lightboxLeft = ((arrayPageSize[0] - 20 - w) / 2);
	
	contentDiv.style.top = (lightboxTop < 0) ? "0px" : lightboxTop + "px";
	contentDiv.style.left = (lightboxLeft < 0) ? "0px" : lightboxLeft + "px";

	// Hide select boxes as they will 'peek' through the image in IE
	selects = document.getElementsByTagName("select");
	for (i = 0; i != selects.length; i++) {
			selects[i].style.visibility = "hidden";
	}
	
	contentDiv.style.display = 'block';
}

function lbHide(contentDiv) {
	// get objects
	objOverlay = document.getElementById('lbOverlay');

	// hide lightbox and overlay
	objOverlay.style.display = 'none';
	contentDiv.style.display = 'none';	

	// make select boxes visible
	selects = document.getElementsByTagName("select");
    for (i = 0; i != selects.length; i++) {
		selects[i].style.visibility = "visible";
	}
}

//
// getPageScroll()
// Returns array with x,y page scroll values.
// Core code from - quirksmode.org
//
function lbGetPageScroll(){

	var yScroll;

	if (self.pageYOffset) {
		yScroll = self.pageYOffset;
	} else if (document.documentElement && document.documentElement.scrollTop){	 // Explorer 6 Strict
		yScroll = document.documentElement.scrollTop;
	} else if (document.body) {// all other Explorers
		yScroll = document.body.scrollTop;
	}

	arrayPageScroll = new Array('',yScroll) 
	return arrayPageScroll;
}

//
// getPageSize()
// Returns array with page width, height and window width, height
// Core code from - quirksmode.org
// Edit for Firefox by pHaez
//
function lbGetPageSize(){
	
	var xScroll, yScroll;
	
	if (window.innerHeight && window.scrollMaxY) {	
		xScroll = document.body.scrollWidth;
		yScroll = window.innerHeight + window.scrollMaxY;
	} else if (document.body.scrollHeight > document.body.offsetHeight){ // all but Explorer Mac
		xScroll = document.body.scrollWidth;
		yScroll = document.body.scrollHeight;
	} else { // Explorer Mac...would also work in Explorer 6 Strict, Mozilla and Safari
		xScroll = document.body.offsetWidth;
		yScroll = document.body.offsetHeight;
	}
	
	var windowWidth, windowHeight;
	if (self.innerHeight) {	// all except Explorer
		windowWidth = self.innerWidth;
		windowHeight = self.innerHeight;
	} else if (document.documentElement && document.documentElement.clientHeight) { // Explorer 6 Strict Mode
		windowWidth = document.documentElement.clientWidth;
		windowHeight = document.documentElement.clientHeight;
	} else if (document.body) { // other Explorers
		windowWidth = document.body.clientWidth;
		windowHeight = document.body.clientHeight;
	}	
	
	// for small pages with total height less then height of the viewport
	if(yScroll < windowHeight){
		pageHeight = windowHeight;
	} else { 
		pageHeight = yScroll;
	}

	// for small pages with total width less then width of the viewport
	if(xScroll < windowWidth){	
		pageWidth = windowWidth;
	} else {
		pageWidth = xScroll;
	}


	arrayPageSize = new Array(pageWidth,pageHeight,windowWidth,windowHeight) 
	return arrayPageSize;
}

//
// addLoadEvent()
// Adds event to window.onload without overwriting currently assigned onload functions.
// Function found at Simon Willison's weblog - http://simon.incutio.com/
//
function lbAddLoadEvent(func)
{	
	var oldonload = window.onload;
	if (typeof window.onload != 'function'){
    	window.onload = func;
	} else {
		window.onload = function(){
		oldonload();
		func();
		}
	}

}



lbAddLoadEvent(lbInit);	// run initLightbox onLoad