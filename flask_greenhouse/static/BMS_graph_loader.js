// source: https://stackoverflow.com/questions/2276463/how-can-i-get-form-data-with-javascript-jquery
		/*
			takes a datetime-local form data, turns it into a new date.
			source: https://stackoverflow.com/questions/24356638/converting-to-a-date-object-from-a-datetime-local-element
		*/
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