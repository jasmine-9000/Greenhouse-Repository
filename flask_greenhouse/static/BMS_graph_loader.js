/*In HTML:
// %3C === <
// %3E === >
// Character Translation from Python strings to HTML using the Jinja2 template engine is weird.

*/
var parameter_placeholder = "%3Cparameter%3E";
var date_placeholder = "%3Cdate%3E";
function returnURL(baseURL, date, parameter ) {
	return baseURL.replace(date_placeholder, date).replace(parameter_placeholder, parameter);
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
	var absolute_localhost_URL = "http://localhost/sensors/get-sensor-json-data-by-id/1/10-31-2019";
	var sensorBaseURL = "http://localhost/sensors/get-sensor-json-data-by-id/<sensor_id>/<date>";
	var BMSBaseURL = $('#BMS_form').data('base_url');// on a local machine, it's http://localhost/BMS/date/<date>/<parameter>
	
	
	$('#BMS_form').on('submit', function() {
		// retrieve dates
		console.log($('#startdate').val());
		let start = parseYMDHM($("#startdate").val());
		let end = parseYMDHM($("#enddate").val());
		let interval = $("#interval").val();
		let dates = [];
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
		
		while(dateLessThan(start, end)) {
			dates.push(start);
			start = addMinutes(start, interval);
		}
		
		// parameter to graph.
		let parameter = $('#units').val()
		// graph metadata
		let trace_name = $("#units").val();
		let x_title = $("#xaxistitle").val();
		let y_title = $("#yaxistitle").val();
		let main_title = $("#title").val();
		
		var URL_list = dates.map(date => returnURL(BMSBaseURL, DateFormatter(date), parameter ));
		console.log(URL_list);
		let y_values = [];
		URL_list.forEach(URL => {
			$.ajax({
				type: "GET",
				url: URL, 
				success: function(data) {
					console.log(data);
					y_values.push(data);
				},
				error: function() {
					console.log("Error loading data.");
				}
			});
		})
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