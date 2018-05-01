var images = [];

images[0] = "images/crowdstorm/crowdstorm-icon-search-1.png";
images[1] = "images/crowdstorm/crowdstorm-icon-search-2-a.png";
images[2] = "images/crowdstorm/crowdstorm-icon-search-2-b.png";
images[3] = "images/crowdstorm/crowdstorm-icon-search-2.png";

var oImage   =  null;
var iIdx     =  0;
function startAnimation(){
try{
  //look only once in DOM and cache it
  if(oImage===null){
	oImage  =  window.document.getElementById("logo-animate");
  }
  oImage.src  =  images[(++iIdx)%(images.length)];
  setTimeout('startAnimation()',1500);
}catch(oEx){
  //some error handling here
}
}


