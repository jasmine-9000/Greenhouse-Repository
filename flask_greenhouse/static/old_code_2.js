/*
		while(dateLessThan(start, end)) {
			dates.push(start);
			start = addMinutes(start, interval);
		}
		var URL_list = dates.map(date => returnURL(BMSBaseURL, DateFormatter(date), parameter ));
		console.log(URL_list);
		
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
		*/