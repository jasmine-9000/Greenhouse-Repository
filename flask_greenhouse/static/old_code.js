var absolute_localhost_URL = "http://localhost/sensors/get-sensor-json-data-by-id/1/10-31-2019";
	// var sensorBaseURL = "http://localhost/sensors/get-sensor-json-data-by-id/<sensor_id>/<date>";
		
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
		
// sample jQuery code. 

// document ready page.
$(function() {
	var $orders = $('#orders');
	$.ajax({
		type: "GET", 
		url: "/api/orders",
		success: function(orders) {
			$.each(orders, function(i, order) {
				$orders.append('<li>'+ order.name + ', drink: ' + order.drink + '</li>');
			});
		},
		error: function() {
			console.log("error loading orders.");
		}
	});
	
});
		
		
		
			
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
		