$(document).ready(function () {

	/* ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ */
	/* # Variables globales */
	/* ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ */
	lastNumberAssigned = 0;

	pipePlayers ={ "actions" : [
			{
				"kind" : "drinks",
				"prepare" : [],
				"price" : []
			}
		]
	}
	pipePlayers = {};

	//{"actions" : [ {"kind" : "drinks","prepare" : [{1:50},{3:20}],"price" : [{1:8},{3:2}]} ] }


	/* # Initialisation de la partie */
	gameInit();

	/* ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ */
	/* # Gestionnaires d'événements */
	/* ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ */

	/* # Rejoindre une partie */
	$( "#formGameJoin" ).submit(function( event ) {
	  event.preventDefault();

	  /* # le joueur rejoin la partie */
	  var name = $('#name').val();
	  gameRejoin(name);

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

	/* # maj données de la liste du joueur */
	$('#btnaddrecette').click(function() {
		valAction();
	})

	/* # maj actions du joueur */
	$('#valAction').click(function() {
		valAction();
	})

	/* # supprimer une recette dans le pipe */
	callbackDelPlayerPipe()


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
		$.ajax({
			url: "/recipe/"+recette,
			type: "GET",
			contentType: 'application/json',
			success: function(result){
				var token = lastNumberAssigned++;
				var elemTr = $('<tr id="'+token+'"></tr>');

				elemTr.append($('<td></td>').html(result.recipe[0].rec_nom));
				elemTr.append($('<td></td>').html(prixu));
				elemTr.append($('<td></td>').html(prixvente));
				elemTr.append($('<td></td>').html(quantite));
				elemTr.append($('<td></td>').html(quantite*prixu));
				elemTr.append($('<td></td>').html(quantite*prixvente));
				elemTr.append($('<td></td>').html($('<a href="#"><span id="'+token+'-btn" class="btnSuppRecette glyphicon glyphicon-trash"></span></a>')));
				$('#playerpipe').append(elemTr);

				/* # Event : supprimer une recette dans le pipe */
				callbackDelPlayerPipe()

				/* # Ajout dans la liste pipePlayers */
				var tmp1 = {};
				var tmp2 = {};
				tmp1[recette] = quantite;
				tmp2[recette] = prixvente;

				pipePlayers.prepare.push(tmp1);
				pipePlayers.price.push(tmp2);
				
				console.log(pipePlayers)
	    	}
		});

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
				$.each(result.weather, function( index, value ) {
					if(value['dfn'] == 0) 
						$('#weatherToday').html(value['weather']);
	        		else 
	        			$('#weatherTomorrow').html(value['weather']);
				});
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

				if(result.players.length > 0){
					var item = $('<ul class="list-group"></ul>');

					$('#playerList').html("");
					for (var i = 0; i < result.players.length; i++) {
						item.append($('<li class="list-group-item">'+ result.players[i].pl_pseudo +'</li>'))
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
	function gameRejoin(name) {
		var data = {"name": name}
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
		$('#name').val("");
	}

	/**
	* 
	*/
	function gameInit () {

		//$('#playgamebloc').addClass("hidden");
		//$('#mapbloc').removeClass("col-md-7");
		//$('#mapbloc').addClass("col-md-12");

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
			var tmp  = '#'+event.target.id.split("-")[0];
			$(tmp).remove()

			$.each(pipePlayers.prepare, function( index, value ) {
				//if(index == event.target.id.split("-")[0])
				console.log(value[0])
			});

			/*jQuery.grep(pipePlayers.prepare, function(n,i) {
				console.log(n)
			  return n == event.target.id.split("-")[0];
			});
			console.log(pipePlayers)*/

		})
	}

	/**
	*
	*/
	$("#valAction").on("click",function(){
      $.ajax("/order",{
      	url: "/actions/<name>",
        method: 'POST',
        contentType: 'application/json',
        pipePlayers : JSON.stringify(pipePlayers),
        success : function(pipePlayers){
        	console.log('OK')
        }
      })
      })

	/**
	*
	*/
	function sendAction() {
		$.ajax({
			url: "/actions/<name>",
			pipePlayers : JSON.stringify(pipePlayers),
			type: "POST",
			contentType: 'application/json',
			success: function(pipePlayers){
				console.log('OK')
	    	}
		});
	}

})
