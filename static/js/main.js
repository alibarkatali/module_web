$(document).ready(function () {

	/* ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ */
	/* # Variables globales */
	/* ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ */
	lastNumberAssigned = 0;


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
	  var prixu = $('#prixunitaire').text()
	  var quantite = parseInt($('#quantity').val());
	  var prixvente = parseFloat($('#prixvente').val());

	  if(Number.isInteger(quantite)){
	  	addPlayerPipe(recette,prixu,quantite,prixvente);
	  }
	  

	});

	/* # raffraichir les données */
	$('#btnRefreshGameInfo').click(function() {
		getMetrology();
	})

	/* # Choix d'une recette */
	if($('#recettadd') != undefined){
		$('#recettadd').change(function() {
			getRepiceByName($(this).val())
		})
	}

	


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
	function addPlayerPipe(recette,prixu,quantite,prixvente) {
		//console.log(recette)

		var token = lastNumberAssigned++;
		var elemTr = $('<tr id="'+token+'"></tr>');
		elemTr.append($('<td></td>').html(recette));
		elemTr.append($('<td></td>').html(prixu));
		elemTr.append($('<td></td>').html(prixvente));
		elemTr.append($('<td></td>').html(quantite));
		elemTr.append($('<td></td>').html(quantite*prixu));
		elemTr.append($('<td></td>').html(quantite*prixvente));
		elemTr.append($('<td></td>').html($('<a id="'+token+'$btn" class="btnSuppRecette" href="#"><span class="glyphicon glyphicon-trash"></span></a>')));
		$('#playerpipe').append(elemTr);

		callbackDelPlayerPipe()
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
					//console.log(value)
					$('#recettadd').append($('<option value="'+ value['rec_id'] +'">'+ value['rec_nom'] +'</option>'))
				});

				//$('#recipes').html("");
				/*for (var i = 0; i < result.length; i++) {

				};*/
	    	}
		});
	}

	function getRepiceByName(rc_id) {
		$.ajax({
			url: "/recipe/"+rc_id,
			type: "GET",
			contentType: 'application/json',
			success: function(result){
				var totalCost = 0;
				$.each(result.ingredients, function( index, value ) {
					totalCost += value['ing_prix'];
				});
				$('#prixunitaire').html(totalCost)
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

	function callbackDelPlayerPipe () {
		/* # supprimer une recette dans le pipe */
		$('.btnSuppRecette').click(function (event) {
			var tmp  = '#'+event.target.id.split("$")[0];
			console.log(tmp)

			$(tmp).remove()
		})
	}

})
