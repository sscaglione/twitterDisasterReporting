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
			response = JSON.parse(xhttp.responseText);
			console.log(response);
			// Get div for table 
			var tableDiv = document.getElementById('table-div');

			// creates a <table> element and add the appropriate id
			// and class
        		var tbl = document.createElement("table");
        		tbl.setAttribute("id", "latest-tweets");
        		tbl.setAttribute("class", "table");

        		console.log("response length: ", response.length);
			for (var i = 0; i < response.length; i++) {
				tweet = response[i];
				console.log(tweet);
				text = tweet[0];
				date = tweet[1];

				// Create table structure
				var row = document.createElement("tr");
				var textCell = document.createElement("td");
				textCell.appendChild(document.createTextNode(text));
                		row.appendChild(textCell);

				var dateCell = document.createElement("td");
				dateCell.appendChild(document.createTextNode(date));
                		row.appendChild(dateCell);
				
				// Add the row to the table
				tbl.appendChild(row)
			}

			// Add the table to the div
			tableDiv.appendChild(tbl);
		}
	};
	xhttp.open("GET", "http://localhost:8080", true);
	xhttp.send();
	setTimeout('loadSandy()',5000);
}

