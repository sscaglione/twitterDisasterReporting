var images = [];

images[0] = "images/crowdstorm/crowdstorm-icon-search-1.png";
images[1] = "images/crowdstorm/crowdstorm-icon-search-2-a.png";
images[2] = "images/crowdstorm/crowdstorm-icon-search-2-b.png";
images[3] = "images/crowdstorm/crowdstorm-icon-search-2.png";

var hurricanes = ["Hurricane Irene", "Hurricane Sandy", "Hurricane Matthew", "Hurricane Isaac", "Hurricane Ike", 
"Hurricane Arthur"];

// Front page code

function autocomplete(inp, arr) {
  /*the autocomplete function takes two arguments,
  the text field element and an array of possible autocompleted values:*/
  var currentFocus;
  /*execute a function when someone writes in the text field:*/
  inp.addEventListener("input", function(e) {
      var a, b, i, val = this.value;
      /*close any already open lists of autocompleted values*/
      closeAllLists();
      if (!val) { return false;}
      currentFocus = -1;
      /*create a DIV element that will contain the items (values):*/
      a = document.createElement("DIV");
      a.setAttribute("id", this.id + "autocomplete-list");
      a.setAttribute("class", "autocomplete-items");
      /*append the DIV element as a child of the autocomplete container:*/
      this.parentNode.appendChild(a);
      /*for each item in the array...*/
      for (i = 0; i < arr.length; i++) {
        /*check if the item starts with the same letters as the text field value:*/
        if (arr[i].substr(0, val.length).toUpperCase() == val.toUpperCase()) {
          /*create a DIV element for each matching element:*/
          b = document.createElement("DIV");
          /*make the matching letters bold:*/
          b.innerHTML = "<strong>" + arr[i].substr(0, val.length) + "</strong>";
          b.innerHTML += arr[i].substr(val.length);
          /*insert a input field that will hold the current array item's value:*/
          b.innerHTML += "<input type='hidden' value='" + arr[i] + "'>";
          /*execute a function when someone clicks on the item value (DIV element):*/
          b.addEventListener("click", function(e) {
              /*insert the value for the autocomplete text field:*/
              inp.value = this.getElementsByTagName("input")[0].value;
              /*close the list of autocompleted values,
              (or any other open lists of autocompleted values:*/
              closeAllLists();
          });
          a.appendChild(b);
        }
      }
  });
  /*execute a function presses a key on the keyboard:*/
  inp.addEventListener("keydown", function(e) {
      var x = document.getElementById(this.id + "autocomplete-list");
      if (x) x = x.getElementsByTagName("div");
      if (e.keyCode == 40) {
        /*If the arrow DOWN key is pressed,
        increase the currentFocus variable:*/
        currentFocus++;
        /*and and make the current item more visible:*/
        addActive(x);
      } else if (e.keyCode == 38) { //up
        /*If the arrow UP key is pressed,
        decrease the currentFocus variable:*/
        currentFocus--;
        /*and and make the current item more visible:*/
        addActive(x);
      } else if (e.keyCode == 13) {
        /*If the ENTER key is pressed, prevent the form from being submitted,*/
        e.preventDefault();
        if (currentFocus > -1) {
          /*and simulate a click on the "active" item:*/
          if (x) x[currentFocus].click();
        }
      }
  });
  function addActive(x) {
    /*a function to classify an item as "active":*/
    if (!x) return false;
    /*start by removing the "active" class on all items:*/
    removeActive(x);
    if (currentFocus >= x.length) currentFocus = 0;
    if (currentFocus < 0) currentFocus = (x.length - 1);
    /*add class "autocomplete-active":*/
    x[currentFocus].classList.add("autocomplete-active");
  }
  function removeActive(x) {
    /*a function to remove the "active" class from all autocomplete items:*/
    for (var i = 0; i < x.length; i++) {
      x[i].classList.remove("autocomplete-active");
    }
  }
  function closeAllLists(elmnt) {
    /*close all autocomplete lists in the document,
    except the one passed as an argument:*/
    var x = document.getElementsByClassName("autocomplete-items");
    for (var i = 0; i < x.length; i++) {
      if (elmnt != x[i] && elmnt != inp) {
        x[i].parentNode.removeChild(x[i]);
      }
    }
  }
  /*execute a function when someone clicks in the document:*/
  document.addEventListener("click", function (e) {
      closeAllLists(e.target);
      });
}

/*initiate the autocomplete function on the "myInput" element, and pass along the countries array as possible autocomplete values:*/
autocomplete(document.getElementById("search-box"), hurricanes);
// End: front page code


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

