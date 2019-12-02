/*In HTML:
// %3C === <
// %3E === >
// Character Translation from Python strings to HTML using the Jinja2 template engine is weird.

*/
var sensor_id_placeholder = "-1";
var date_placeholder = "%3Cdate%3E";
function returnURL(baseURL, sensor_id, date ) {
	return baseURL.replace(date_placeholder, date).replace(sensor_id_placeholder, sensor_id);
}

/*
parseYMDHM: 
	argument:
		s: a date string
	returns:
		a new JS date object. 
*/
function parseYMDHM(s) {
  var b = s.split(/\D+/);
  return new Date(b[0], --b[1], b[2], b[3], b[4], b[5]||0, b[6]||0);
}
/*
	Arguments:
		date: a Date() object from JS.
		minutes: an interval in minutes you want to add.
	Returns:
		a new Date() object <interval> minutes from the date passed in.
*/
function addMinutes(date, minutes) {
	return new Date(date.getTime() + minutes*60000);
}
		
/*
My own date formatter.
JS does not provide one for you, unlike python. You must write it yourself.
	Arguments:
		date: a Date() object from JS.
	Returns:
		A string in format: 
			"%Y-%M-%D %H:%M:%S"
*/
function DateFormatter(date) {
	var day = date.getDate();
	var month = date.getMonth();
	var year = date.getFullYear();
	var hour = date.getHours();
	var minute = date.getMinutes();
	var second = date.getSeconds();
	if(day < 10) day = '0' + day;
	if(month < 10) month = '0' + month;
	if(hour < 10) hour = '0' + hour;
	if(minute < 10) minute = '0' + minute;
	if(second < 10) second = '0' + second;
	return year + '-' + month + '-' + day + ' ' + hour + ':' + minute + ':' + second;		
}

/*
	Date Comparison Function
	Arguments:
		start: Start Date
		end: End Date
	Returns: 
		True if Start Date is Before End Date
		False if Start Date if After or equal to End Date.
*/

function dateLessThan(start, end) {
	console.log("Difference: " + (end - start));
	if(start.getTime() > end.getTime()) {
		return false;
	} else {
		return true;
	}
	
}	


/*
 Main functions
*/

$(function() {
	var SensorBaseURL = $('#sensor_form').data('base_url'); // retrieve the data-* parameter that was added in HTML5. Ours is data-base_url. 
															// the templating engine won't let us pass a variable directly into the JS file.
	console.log("Base URL: ", SensorBaseURL);
	
	// add jQuery event listener. On Submit, it will extrapolate data from the form,
	// request data from the server, and Chart thhat data
	$('#sensor_form').on('submit', function() {
		// retrieve dates from form.
		let start = parseYMDHM($("#start_date").val());
		let end = parseYMDHM($("#end_date").val());
		let interval = $("#interval").val();
	
		// interval validation
		if (interval == null || interval == "") { 
			interval = 10; 
		}
		else if (interval % 10) {
			if (interval < 10) {
				interval = 10
			} else {
				interval = Math.floor(interval / 10);
			}
		}
		// Generate all dates from start to end date in interval steps.
		let dates = [];
		while(dateLessThan(start, end)) {
			dates.push(start);
			start = addMinutes(start, interval);
		}
		
		// sensor_id to retrieve JSON data from.
		let sensor_id = $('#sensors_owned').val()
		// graph metadata
		let trace_name = 'lux' //$("#units").val();
		let x_title = $("#xaxistitle").val();
		let y_title = $("#yaxistitle").val();
		let main_title = $("#title").val();
		
		// generate all URLs from the dates variable, using the Sensor Base URL, and replacing -1 with sensor id, and <date> with the date for each date you want.
		var URL_list = dates.map(date => returnURL(SensorBaseURL, sensor_id, DateFormatter(date) ));
		console.log(URL_list);
		
		// retrieve data from each URL. For each URL, process the data, and push it into the graph.
		let y_values = [];
		URL_list.forEach(URL => {
			$.ajax({
				dataType: "json",
				type: "GET",
				url: URL,
				success: function(data) {
					data = JSON.parse(data);
					console.log(data);
					console.log(data["lux"]);
					y_values.push(data["lux"]);
				},
				error: function() {
					console.log("Error loading data.");
				}
			});
		})
		// create a dictionary containing all of our data to plot in ChartIt() later.
		let data = {};
		data["title"] = main_title;
		data["x title"] = x_title;
		data["y title"] = y_title;
		data["trace name"] = trace_name;
		data["interval"] = interval;
		data["start date"] = start;
		data["end date"] = end;
		data["x values"] = dates;
		data["y values"] = y_values;
		ChartIt(data, 'chart');
		console.log(data);
		return false;
	});
});

function ChartIt(data, div_id) {
	var trace = {
		x: data["x values"],
		y: data["y values"],
		name: data["trace name"],
		type: 'line'
	};
	var layout = {
		title: {
			text: data["main title"]
		},
		xaxis: {
			title: {
				text: data["x title"]
			}
			// type: 'date' // you should specify that xaxis is a date.
		},
		yaxis: {
			title: {
				text: data["y title"]
			},
			type: 'linear',
			autorange: true
		},
		margin: {
			t: 0
		}
	};
	// plot the graph. Will be displayed in the 'chart' div.
	Plotly.plot(div_id, [trace], layout);
}
/* sources: 
https://stackoverflow.com/questions/2276463/how-can-i-get-form-data-with-javascript-jquery

https://stackoverflow.com/questions/24356638/converting-to-a-date-object-from-a-datetime-local-element
*/

function ccchartIt() {
	// sensor data from elements retreival
	var sensors_owned_element = document.getElementById("{{ form.sensors_owned.id }}");
	// range data
	var start_date_element = document.getElementById("{{ form.start_date.id }}");
	var end_date_element = document.getElementById("{{ form.end_date.id}}");
	var interval_element = document.getElementById("{{ form.interval.id}}");
	alert("Hello, " + username);
	
	// extract values
	var username = "{{ current_user.username }}";
	var start_date = start_date_element.value;
	var end_date = end_date_element.value;
	var interval = interval_element.value;
	var sensors_owned = sensors_owned_element.value;
	// log them to the console.
	console.log(start_date);
	console.log(end_date);
	console.log(interval);
	console.log(sensors_owned);
	var sensor_id = sensors_owned.value;  // database id of the sensor number you want. 
	var base_URL = "{{ url_for('sensor_nodes.sensor_id_JSON', sensor_id=-1, date='<d>') }}"
	var promises = [];
	var dates = [];
	
	while(start_date < end_date) {
		dates.push(start_date);
		console.log(start_date);
		start_date = start_date + interval;
	}
	console.log(dates);
		
	
	return false;
}

		