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
  setTimeout('startAnimation()',1000);
}catch(oEx){
  //some error handling here
}
}


/* Server Code */
function loadSandy() {
  console.log("Loading sandy");
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
	if (this.readyState == 4 && this.status == 200) {
          console.log("Sandy loading");
          console.log(xhttp.responseText);
	}
  };
  xhttp.open("GET", "http://localhost:8080", true);
  xhttp.send();
}

