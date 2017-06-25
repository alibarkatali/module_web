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

	/* # Ajouter une recette dans le panier du joueur */
	$( "#formproduction" ).submit(function( event ) {
	  event.preventDefault();

	  var recette = $('#recettadd').val();
	  var quantite = parseInt($('#quantity').val());
	  var prixvente = parseFloat($('#prixvente').val());

	  if(Number.isInteger(quantite)){
	  	addPlayerPipe(recette,quantite,prixvente);
	  }
	  

	});

	/* # raffraichir les données */
	$('#btnRefreshGameInfo').click(function() {
		getMetrology();
	})

	/* # récupérer une recette */
	if($('#recipes') != undefined){
		$('#recipes').change(function() {
			getRepiceByName($(this).val())
		})
	}

	/* # supprimer une recette dans le pipe */
	$('.btnSuppRecette').click(function (event) {
		$('#'+event.target.id).parent().remove()
	})


	/* ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ */
	/* # Les fonctions */
	/* ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ */

	var rand = function() {
	    return Math.random().toString(36).substr(2); // remove `0.`
	};

	var token = function() {
	    return rand() + rand(); // to make it longer
	};


	/**
	*
	*/
	function addPlayerPipe(recette,quantite,prixvente) {
		console.log(recette)

		var elemTr = $('<tr id="'+token()+'"></tr>');
		elemTr.append($('<td></td>').html(recette));
		elemTr.append($('<td></td>').html(0));
		elemTr.append($('<td></td>').html(prixvente));
		elemTr.append($('<td></td>').html(quantite));
		elemTr.append($('<td></td>').html(quantite*0));
		elemTr.append($('<td></td>').html(quantite*prixvente));
		elemTr.append($('<td></td>').html($('<a href="#"><span class="btnSuppRecette glyphicon glyphicon-trash"></span></a>')));
		$('#playerpipe').append(elemTr);
	}

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
						item.append($('<li>'+ result[i].pl_pseudo +'</li>'))
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


				$.each(result.recipes, function( index, value ) {
					console.log(value)
					$('#recipes').append($('<option value="'+ value['rec_nom'] +'">'+ value['rec_nom'] +'</option>'))
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
				//console.log(result)

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
