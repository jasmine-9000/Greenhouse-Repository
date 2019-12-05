/************************************************************************************************
*								URL Translation													*
*************************************************************************************************/
/*In HTML:
// %3C === <
// %3E === >
// Character Translation from Python strings to HTML using the Jinja2 template engine is weird.
*/

var date_placeholder = "%3Cdate%3E";
var start_date_placeholder = "%3Cstart_date%3E";
var end_date_placeholder = "%3Cend_date%3E";
var parameter_placeholder = "%3Cparameter%3E";
var interval_placeholder = "5555";

/***********************************************
		SingleReturnURL
		
		Arguments:
			baseURL: baseURL to replace with. Usually retrieved from the form.
			date: the date you want to request from.
			parameter: the parameter you want.
		Returns:
			 a valid Single Data Point Retrival URL.
***********************************************/
function SingleReturnURL(baseURL, date, parameter ) {
	return baseURL.replace(date_placeholder, date).replace(parameter_placeholder, parameter);
}
/***********************************************
		MultiReturnURL
		
		Arguments:
			baseURL: baseURL to replace with. Usually retrieved from the form.
			start_date: the starting date
			end_date: the end date
			interval: interval
			parameter: the parameter you want.
		Returns:
			 a valid Multi Data Point Retrival URL.
***********************************************/
function MultiReturnURL(baseURL, start_date, end_date, interval, parameter) {
	
	console.log(start_date);
	console.log(end_date);
	console.log(interval);
	console.log(parameter);
	var u =  baseURL
			.replace(start_date_placeholder, start_date)
			.replace(end_date_placeholder, end_date)
			.replace( interval_placeholder, interval)
			.replace(parameter_placeholder, parameter);
	console.log(baseURL);
	console.log(u);
	return u;
}

/************************************************************************************************
*								DATE PARSING FUNCTIONS											*
*************************************************************************************************/
/***********************************************
parseYMDHM: 
	argument:
		s: a date string
	returns:
		a new JS date object. 
***********************************************/
function parseYMDHM(s) {
  var b = s.split(/\D+/);
  return new Date(b[0], --b[1], b[2], b[3], b[4], b[5]||0, b[6]||0);
}
/***********************************************
addMinutes:
	Arguments:
		date: a Date() object from JS.
		minutes: an interval in minutes you want to add.
	Returns:
		a new Date() object <interval> minutes from the date passed in.
***********************************************/
function addMinutes(date, minutes) {
	return new Date(date.getTime() + minutes*60000);
}
		
/***********************************************
DateFormatter:
A Python-like strftime(). JS does not provide one for you. You must write it yourself.
	Arguments:
		date: a Date() object from JS.
	Returns:
		A string in format: 
			"%Y-%M-%D %H:%M:%S"
************************************************/
function DateFormatter(date) {
	var day = date.getDate();
	var month = date.getMonth() + 1;
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


/***********************************************
dateLessThan:
Date Comparison Function. Replaces the > operator.
	Arguments:
		start: Start Date
		end: End Date
	Returns: 
		True if Start Date is Before End Date
		False if Start Date if After or equal to End Date.
***********************************************/

function dateLessThan(start, end) {
	console.log("Difference: " + (end - start));
	if(start.getTime() > end.getTime()) {
		return false;
	} else {
		return true;
	}
	
}	


/************************************************************************************************
*								MAIN FUNCTIONS													*
*************************************************************************************************/
// upon loading the document, declare these variables, and add these event listeners.
$(function() {
	// retrieve API URLs from the form. These 
	var TristarBaseURL = $('#Tristar_form').data('base_url');
	var MultiTristarBaseURL = $('#Tristar_form').data('multi_base_url');
	
	// upon form submission, retrieve form contents, build multi-data-point API URL endpoint to retrieve data from,
	// fetch JSON content from that URL, extrapolate data from the JSON content, and chart a graph from that data.
	$('#Tristar_form').on('submit', function() {
		// retrieve dates from for.m.
		console.log($('#start_date').val());
		let start = parseYMDHM($("#start_date").val());
		let end = parseYMDHM($("#end_date").val());
		let interval = $("#interval").val();
		let dates = [];
		let parameter = $('#units option:selected').val() // parameter to graph.
		console.log(parameter); // debugging statements.
		
		// retrieve graph metadata from form.
		let trace_name = $("#units option:selected").text();
		let x_title = $("#xaxistitle").val();
		let y_title = $("#yaxistitle").val();
		let main_title = $("#title").val();
		
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
		
		// initialize x_values, y_values, and data dictionary.
		let x_values = [];
		let y_values = [];
		let data = {};
		
		// build endpoint. 
		var URL = MultiReturnURL(MultiTristarBaseURL, DateFormatter(start), DateFormatter(end), interval, parameter);
		
		// start data retrieval.
		$.ajax({
			type: "GET",
			url: URL, 
			success: function(d) {
				console.log(d); // debugging statement.
				y = d["data"]; // retrieve data dictionary from d. 
				console.log(y); // debugging statement.
				for (var key in y) {
					if (y.hasOwnProperty(key)) {
						// skip any dates (keys) that don't have their own values that correspond with them.
						x_values.push(key); // the x_values must have the keys (dates)
						y_values.push(y[key]); // the y_values must have the values (data points)
					}
				}
				console.log(y_values); // debugging statement.
				// create data dictionary used for function ChartIt(). 
				
				data["title"] = main_title;
				data["x title"] = x_title;
				data["y title"] = y_title;
				data["trace name"] = trace_name;
				data["interval"] = interval;
				data["start date"] = start;
				data["end date"] = end;
				data["x values"] = x_values;
				data["y values"] = y_values;
				
				// chart the graph. The chart will go into a div with id == 'chart'.
				ChartIt(data, 'chart');
			},
			error: function() {
				// error handling.
				console.log("Error retrieving data");
			}
		});
		// This on_submit() event handler will always return false so the page doesn't reload.
		return false;
	});
});
/***********************************************
ChartIt: 
Plots a Graph For you.
	Arguments:
		data: a data dictionary to pass in.
		div_id: what div id you want to put the chart into.
	Returns:
		void.
		Fills div_id with a Plotly.js chart.
		
***********************************************/
function ChartIt(data, div_id) {
	console.log("Data Passed to ChartIt(): ", data);
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
	return false;
}
/************************************************************************************************
*								SOURCES															*
*************************************************************************************************/
// https://stackoverflow.com/questions/2276463/how-can-i-get-form-data-with-javascript-jquery
// https://stackoverflow.com/questions/24356638/converting-to-a-date-object-from-a-datetime-local-element