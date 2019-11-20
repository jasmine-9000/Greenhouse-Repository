async function setup_graph(baseURL) {
	
	// retrieve form contents
	var form = document.getElementById("BMS_form");
	let start = parseYMDHM(form["startdate"].value);
	let end = parseYMDHM(form["enddate"].value);
	let interval = form["interval"].value;

	// interval validation
	// default interval value if none provided.	
	console.log("Interval before validation: " + interval);
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
	console.log("Interval after validation: " + interval);
	// retrieve graph metadata from form.
	let trace_name = form["units"].value;
	let x_title = form["xaxistitle"].value;
	let y_title = form["yaxistitle"].value;
	let main_title = form["title"].value;
	
	// log form contents.
	console.log("Start Date: " + start);
	console.log("End Date: " + end);
	console.log("Interval: " + interval);
	console.log("Trace Name: " + trace_name);
	console.log("X Title: " + x_title);
	console.log("Y Title: " + y_title);
	console.log("Main Title: " + main_title);
	
	/*
	// Generate All Dates required.
	let dates = [start];
	while(start < end) {
		start = addMinutes(start, interval);
		dates.push(start);
	}
	*/
	// Retrieve Graph Data
	let allData = await RetrieveAllData( start,  
										end, 
										interval, 
										'battery', 
										baseURL)
	// Log data retrieved.
	console.log("Data Retrived: ");
	console.log(allData);
	
	// Create data dictionary out of form data.
	let data = {};
	data["title"] = main_title;
	data["x title"] = x_title;
	data["y title"] = y_title;
	data["trace name"] = trace_name;
	data["interval"] = interval;
	data["start date"] = start;
	data["end date"] = end;
	data["x values"] = allData["x"];
	data["y values"] = allData["y"];
	console.log(data);
	
	// Chart the graph using the ChartIt() method created earlier.
	ChartIt(data);
	return false;
}	

// In HTML:
// %3C === <
// %3E === >
// Character Translation from Python strings to HTML using the Jinja2 template engine is weird.
var parameter_placeholder = "%3Cparameter%3E";
var date_placeholder = "%3Cdate%3E";
function returnURL(baseURL,date,parameter ) {
	return baseURL.replace(date_placeholder, date).replace(parameter_placeholder, parameter);
}







function dateLessThan(start, end) {
	console.log("Difference: " + (end - start));
	if(start.getTime() > end.getTime()) {
		return false;
	} else {
		return true;
	}
	
}	
// based on form contents, retrieve data from database from the Base URL provided by the website.
// RetrieveData() calls the fetch() method. It returns a promise, so you use the await keyword to wait until it is done fetching.


async function RetrieveAllData(start, end, interval, parameter, baseURL) {
	let data = {};
	
	let dates = [];
	let y_values = [];
	console.log("Start: ");
	console.log(start);
	console.log("End: ");
	console.log(end);

	while(dateLessThan(start, end)) {
		dates.push(start);
		console.log(start);
		start = addMinutes(start, interval);
		console.log(start);
	}
	// console.log(returnURL(baseURL, DateFormatter("10-31-2019", "baby")));
	
	let requests = dates.map(date_item => fetch( returnURL(baseURL, DateFormatter(date_item), parameter ) ) );
	console.log("Dates: ");
	console.log(dates);
	console.log("Requests: ");
	console.log(requests);
	
	Promise.all(requests).then(responses => {
		for(let response of responses) {
		 console.log(`${response.url}: ${response.status}`); // shows 200 for every url
		}
		return responses;
	})
	.then(responses => Promise.all(responses.map(r => r.json() )))
	.then(values => values.forEach(value => {
		y_values.push(value["x"])
		console.log(value);
	}
	));
	data["x"] = dates;
	data["y"] = y_values;
	console.log(data);
	return data;
}


async function RetrieveData(URL) {
	const response = await fetch(URL);
	return response.json();
}

function ChartIt(data) {
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
	Plotly.plot('chart', [trace], layout);
}

function parseYMDHM(s) {
  var b = s.split(/\D+/);
  return new Date(b[0], --b[1], b[2], b[3], b[4], b[5]||0, b[6]||0);
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








































// source: https://stackoverflow.com/questions/2276463/how-can-i-get-form-data-with-javascript-jquery
		/*
			takes a datetime-local form data, turns it into a new date.
			source: https://stackoverflow.com/questions/24356638/converting-to-a-date-object-from-a-datetime-local-element
		*/
		
		
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
		
		
		var str = "{{ url_for('bms.BMS_data_retrieval', date='<date>', parameter='<parameter>') }}"; 
		// BMS_data_retrieval_URL = BMS_data_retrieval_URL.replace('<date>', '<
		async function chartIt(BMS_URL) {
			var BMS_data_retrieval_URL = BMS_URL;
			var form = document.getElementById("BMS_form");
			var start = parseYMDHM(form["startdate"].value);
			var end = parseYMDHM(form["enddate"].value);
			var interval = form["interval"].value;
			
			let start_URL = await BMS_data_retrieval_URL.replace('<date>',DateFormatter(start));
			console.log('str: ' + str);
			var x = str.replace('<date>', DateFormatter(start));
			console.log('x: ' + x);
			var y = x.replace('<date>',DateFormatter(start));
			console.log('y: ' + y);
			// console.log(start_URL);
			
			const response = await fetch(start_URL);
			const myJSON = await response.json();
			console.log(myJSON);
			
			
			var x_values = [];
			var y_values = [];
			
			// Y value is linear for now.
			// using the formula y = mx+b 
			
			var m = 1;
			var b = 2;
			var y = b;
			
			while(start < end) {
				var current_date = DateFormatter(start);
				console.log(current_date);
				x_values.push(current_date);
				y += m;
				y_values.push(y);
				
				start = addMinutes(start, interval);
			}
			var trace_name = form["units"].value;
			var x_title = form["xaxistitle"].value;
			var y_title = form["yaxistitle"].value;
			var main_title = form["title"].value;
			var trace = {
				x: x_values,
				y: y_values,
				name: trace_name,
				type: 'line'
			};
			var layout = {
				title: {
					text: main_title
				},
				xaxis: {
					title: {
						text: x_title
					},
					type: 'date' // you should specify that xaxis is a date.
				},
				yaxis: {
					title: {
						text: y_title
					},
					type: 'linear',
					autorange: true
				},
				margin: {
					t: 0
				}
			};
			// plot the graph. Will be displayed in the 'chart' div.
			Plotly.plot('chart', [trace], layout);
			return;
		}
		
		
		
	
		
		
		
		
		
		
		
		
		