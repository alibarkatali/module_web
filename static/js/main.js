$(document).ready(function () {

	/* # Initialisation de la partie */
	gameInit();

	/* ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ */
	/* # Gestionnaires d'événements */
	/* ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ */

	/* # Rejoindre une partie */
	$( "#formGameJoin" ).submit(function( event ) {
	  event.preventDefault();

	  /* # le joueur rejoin la partie */
	  var playerName = $('#playerName').val();
	  gameRejoin(playerName);

	  /* # liste de joueur */
	  getPlayers();

	});

	$('#btnRefreshGameInfo').click(function() {
		getMetrology();
	})

	if($('#recipes') != undefined){
		$('#recipes').change(function() {
			getRepiceByName($(this).val())
		})
	}


	/* ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ */
	/* # Les fonctions */
	/* ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ */
	
	/**
	*
	*/
	function getMetrology () {
		$.ajax({
			url: "/metrology", 
			type: "GET",
			contentType: 'application/json',
			success: function(result){
				$('#timer').html(result.timestamp);
	        	$('#weatherToday').html(result.weatherToday);
	        	$('#weatherTomorrow').html(result.weatherTomorow);
	    	}
		});
	}

	/**
	*
	*/
	function getPlayers() {
		$.ajax({
			url: "/players", 
			type: "GET",
			contentType: 'application/json',
			success: function(result){
				//console.log(result)
				if(result.length > 0){
					var item = $('<ul></ul>');

					$('#playerList').html("");
					for (var i = 0; i < result.length; i++) {
						item.append($('<li>'+ result[i] +'</li>'))
					};
					$('#playerList').append(item);
				}else{
					$('#playerList').html("Liste vide :(");
				}
	    	}
		});
	}

	function getRepices() {
		$.ajax({
			url: "/recipes", 
			type: "GET",
			contentType: 'application/json',
			success: function(result){
				

				$.each(result, function( index, value ) {
					console.log(value)
					$('#recipes').append($('<option value="'+ value['name'] +'">'+ value['name'] +'</option>'))
				});

				//$('#recipes').html("");
				/*for (var i = 0; i < result.length; i++) {
					
				};*/
	    	}
		});
	}

	function getRepiceByName(name) {
		$.ajax({
			url: "/recipes/"+name, 
			type: "GET",
			contentType: 'application/json',
			success: function(result){
				console.log(result)

	    	}
		});
	}
	
	/**
	*
	*/
	function gameRejoin(playerName) {
		var data = {"playerName": playerName}
		$.ajax({
			url: "/players", 
			data : JSON.stringify(data),
			type: "POST",
			contentType: 'application/json',
			success: function(result){
	        	resetFormGameJoin()
	    	}
		});
	}

	/**
	* 
	*/
	function resetFormGameJoin () {
		$('#playerName').val("");
	}

	/**
	* 
	*/
	function gameInit () {
		/* # récupération de la météo */
	  	getMetrology ();

	  	/* # Liste de joueurs */
	  	getPlayers();

	  	if($('#blocSimul') != undefined)
	 		getRepices();
	}

})