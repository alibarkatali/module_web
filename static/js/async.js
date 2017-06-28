/* # Mise à jour du timstamp */
setTimeout(function () {
	$.ajax({
		url: "/metrology", 
		type: "GET",
		contentType: 'application/json',
		success: function(result){

			$('#timer').html(result.timestamp);
			$.each(result.weather, function( index, value ) {
				if(value['dfn'] == 0) 
					$('#weatherToday').html(value['weather']);
        		else 
        			$('#weatherTomorrow').html(value['weather']);
			});
    	}
	});
}, 100);