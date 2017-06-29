$(document).ready(function () {

	/* ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ */
	/* # Variables globales */
	/* ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ */
	lastNumberAssigned = 0;
	playerName = "";


	pipePlayers = { "actions" : 
			[
				{
					"kind" : "drinks",
					"prepare" : [],
					"price" : []
				}
			]
		}

	/* # Initialisation de la partie */
	gameInit();
	
	/* # Synchronisations */
	//setInterval(getMetrology, 12000);
	//setInterval(getPlayers, 30000);

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

	  getInfoRecette()
	  
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

	/* # supprimer une recette dans le pipe */
	callbackDelPlayerPipe()

	/* # Valider les actions : achat des recettes,... */
	$('#valideracions').click(function() {
		sendAction()
	})

	/* # Quitter la partie en cours */
	$('#btnexitgame').click(function() {
		exitGameByName()
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

	function getInfoRecette(){
		var recette = $('#recettadd').val();
		  var prixu = $('#prixunitaire').text()
		  var quantite = parseInt($('#quantity').val());
		  var prixvente = parseFloat($('#prixvente').val());

		  if(Number.isInteger(quantite)){
		  	addPlayerPipe(recette,prixu,quantite,prixvente);
		  }
	}


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

				var itemRecette = $('<div id="'+token+'" class="row"><div class="col-md-3">'+result.recipe[0].rec_nom+'</div><div class="col-md-3">'+quantite+'</div><div class="col-md-3">'+prixvente+'</div><div class="col-md-3">'+quantite*prixvente+'<a href="#"><span id="'+token+'-btn" class="btnSuppRecette glyphicon glyphicon-trash"></span></a></div></div>');
				$('#additemrecette').before(itemRecette);

				
				/* # Event : supprimer une recette dans le pipe */
				callbackDelPlayerPipe()

				/* # Ajout dans la liste pipePlayers */
				// {"actions" : [{"kind" : "drinks","prepare" : [{"1":50},{"3":20}],"price" : [{"1":8},{"3":2}]} ]}
				
				var tmp1 = {};
				var tmp2 = {};
				recette = (result.recipe[0].rec_nom).toString();
				tmp1[recette] = quantite;
				tmp2[recette] = prixvente;

				pipePlayers.actions[0].prepare.push(tmp1);
				pipePlayers.actions[0].price.push(tmp2);
				
				console.log(JSON.stringify(pipePlayers))
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

	function loadTime() {
		
	}
	loadTime();

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

	function exitGameByName(rc_id) {
			$.ajax({
				url: "/players/"+playerName,
				type: "DELETE",
				contentType: 'application/json',
				success: function(result){
					
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
	        	resetFormGameJoin();

	        	/* Supprimer le bloque rejoindre la partie */
	        	$('#inscriptionbloc').remove();

	        	/* Mise à jour des informations relatives au player */
	        	$('#username').html(result.name);
	        	playerName = result.name
	        	$('#budgetplayer').html(result.info.cash)

	        	/* Affichage d'un message de bienvenue */
	        	var title = 'Coucou '+playerName+'. ';
	        	var msg = 'Toujours aussi BD ?';
	        	var status = 'success';
	        	showMessage(title,msg,status);

	        	/*console.log(result.info.profit)
	        	console.log(result.info.sales)
	        	console.log(result.info.drinksOffered)
	        	console.log(result.info.longitude)
	        	console.log(result.info.latitude)*/

	        	/* Afficher l'interface de simulation */
	        	$('#infogamebloc').removeClass("hidden");

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

		if(playerName.length > 0){
			$('#infogamebloc').removeClass("hidden");

			/* # Confirmation du player pour quitter une partie */
			exitGame();
		}else{
			$('#infogamebloc').addClass("hidden");
		}

	  	/* # Liste de joueurs */
	  	getPlayers();

	  	if($('#blocSimul') != undefined)
	 		getRepices();


	}

	function exitGame () {
		window.onbeforeunload = function() {
		    return "Etes-vous sûr de quitter la partie ?";
		}
	}

	function callbackDelPlayerPipe () {
		/* # supprimer une recette dans le pipe */
		$('.btnSuppRecette').click(function (event) {
			var tmp  = '#'+event.target.id.split("-")[0];
			

			$.each(pipePlayers.actions[0].prepare, function( index, value ) {
				if (parseInt(index) == parseInt(event.target.id.split("-")[0]))
					pipePlayers.actions[0].prepare.splice(index, 1);
			});

			$.each(pipePlayers.actions[0].price, function( index, value ) {
				if (parseInt(index) == parseInt(event.target.id.split("-")[0]))
					pipePlayers.actions[0].price.splice(index, 1);
			});


			$(tmp).remove()

			//console.log(pipePlayers)

		})
	}

	/**
	*
	*/
	function sendAction() {
		console.log(pipePlayers.toString())

		$.ajax({
			url: "/actions/"+playerName,
			data : JSON.stringify(pipePlayers),
			type: "POST",
			contentType: 'application/json',
			success: function(result){
				var title, msg, status;

				if(result.sufficientFunds == "false"){
					title = 'Solde insuffisant';
					msg = 'Nous ne pouvez pas acheter ces boissons !';
					status = 'danger';
					showMessage(title,msg,status)
				}else if(result.sufficientFunds == "true"){
					title = 'Félicitation';
					msg = 'Vos boissons ont été ajoutés avec succès !';
					status = 'success';
					showMessage(title,msg,status)
				}
	    	}
		});
	}

	function showMessage (title,msg,status) {
		$.notify({
					title: title,
					message: msg
				},{
					type: status
				});
	}

})