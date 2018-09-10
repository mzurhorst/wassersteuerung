$(function() {
	// Register global variables;

	var currentdate;
	var stopWatchRunning1 = false;
	var stopWatchRunning2 = false;
	var startTime1;
	var startTime2;

	var settingsVersion = 0;
	var previousSettings = 0;
	var pushUpdate = false;
	var updateIterator = 0;
	
	
	
	// Register permanent functions for clock/time
	registerClock();
	setTime();

	
// add leading zero to single digit numbers
function leadingzero(number) {
	return (number < 10) ? '0' + number : number;
};

// fires the updateClock() function every 1000ms
function registerClock() {
  setInterval(updateClock, 1000);
};

// 
function updateClock() {
  setTime();
  setStopWatch1();
  setStopWatch2();
};


function setTime() {
  currentdate = new Date(); 
  var datetime = + currentdate.getDate() + "."
                + (currentdate.getMonth()+1)  + "."
                + currentdate.getFullYear() + " " 
                + leadingzero(currentdate.getHours()) + ":" 
                + leadingzero(currentdate.getMinutes()) + ":"
                + leadingzero(currentdate.getSeconds());
  $("#time1").text(datetime);
};



$("#startstop1").click(function() {
  if (stopWatchRunning1 == false) {
    startTime1 = new Date();
    stopWatchRunning1 = true;
  } else {
    stopWatchRunning1 = false;
	$("#tracker1").text("00s");
  }
});


$("#startstop2").click(function() {
  if (stopWatchRunning2 == false) {
    startTime2 = new Date();
    stopWatchRunning2 = true;
  } else {
    stopWatchRunning2 = false;
	$("#tracker2").text("00s");
  }
});

// setStopWatch1 needs to be duplicated 5x
function setStopWatch1() {
  if (stopWatchRunning1 == false) {
    return;
  }
  var duration = new Date(currentdate - startTime1);
  var durationHours = leadingzero(duration.getHours()-1);
  var durationMinutes = leadingzero(duration.getMinutes());
  var durationSeconds = leadingzero(duration.getSeconds());
  showDuration = formatTimeString(durationHours, durationMinutes, durationSeconds);
  $("#tracker1").text(showDuration);
};

function setStopWatch2() {
  if (stopWatchRunning2 == false) {
    return;
  }
  var duration = new Date(currentdate - startTime2);
  var durationHours = leadingzero(duration.getHours()-1);
  var durationMinutes = leadingzero(duration.getMinutes());
  var durationSeconds = leadingzero(duration.getSeconds());
  showDuration = formatTimeString(durationHours, durationMinutes, durationSeconds);
  $("#tracker2").text(showDuration);
};




function formatTimeString(hours, minutes, seconds) {
	var returnstring ="";
	var arr = ["00", "01", "02", "03", "04", "05"];   // first five minutes:  display mm:ss min
	if (hours == "00") {
		if (minutes == "00") {
			returnstring = seconds + "s";     // first minute:    display ss s
		} else {
			if ( $.inArray(minutes, arr) > -1 ) {
				console.log("var minutes: " + minutes);
				returnstring = minutes + ":" + seconds + "min";
				return returnstring;
				// the value is in the array
			}
			returnstring = hours + ":" + minutes + "h";    // starting with sixth minutes:   display  hh:mm h
			return returnstring;
		};
	} else {
		returnstring = hours + ":" + minutes + "h";
	};
	return returnstring;
};


// Sampe function:   each click will elevate the global settingsVersion counter
$("#changesettings").click(function() {
	settingsVersion++;
	if (pushUpdate == false) {
		// this is either the first change or all previous changes have already been saved to disk
		pushUpdate = true;
		previousSettings = settingsVersion-1;
		setTimeout(function(){checkUpdates(previousSettings, settingsVersion);}, 1000);
	};
});



function checkUpdates(prevSettings, settingsVer) {
	if (prevSettings == settingsVer) {
		 //console.log("Settings identical to previous loop");
		 if (updateIterator < 20) {
			 updateIterator = updateIterator + 1;    // add 1 seconds for each loop
			setTimeout(function(){checkUpdates(previousSettings, settingsVersion);}, 1000);
		 } else {
			 // trigger AJAX request to save changed settings back to disk
			 updateIterator = 0;
			 settingsVersion  = 0;
			 ajaxPushSettings();
			 pushUpdate = false;
		 };
	} else {
		// console.log("Settings Level has been changed recently");
		updateIterator = 0;
		previousSettings = settingsVersion;
		setTimeout(function(){checkUpdates(previousSettings, settingsVersion);}, 1000);
	};		
};
	

function ajaxPushSettings() {
	console.log("Settings will be saved to disk");
};






});
