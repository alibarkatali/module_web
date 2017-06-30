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
	setInterval(getMetrology, 6000);
	setInterval(getPlayers, 12000);


	/* ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ */
	/* # Gestionnaires d'événements */
	/* ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ */

	/* # Rejoindre une partie */
	$( "#formGameJoin" ).submit(function( event ) {
	  event.preventDefault();


	  /* # le joueur rejoint la partie */
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


	/* # rafraichir les données */
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

	/* # Réinitialiser le jeu */
	$('#btnquitterpartie').click(function() {
		resetGame()
	})

	/* Quitter la partie au chargement de la page */
	$( window ).ready(function() {
		if(playerName != "")
			exitGameByName()
	});


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
	function getBudgetByName () {
		$.ajax({
			url: "/player/info/"+playerName, 
			type: "GET",
			contentType: 'application/json',
			success: function(result){
				$('#budgetplayer').empty()
				$('#budgetplayer').html(result.cash)

				$('#profit').html(result.profit);
				$('#sales').html(result.sales);

				/* GAME OVER */
				if (result.cash < 0.6){
					var title = 'Vous n avez plus d argent !';
	        		var msg = ' Vous ne pouvez plus acheter de recette. GAME OVER :(';
	        		var status = 'danger';
	        		showMessage(title,msg,status);
					exitGameByName()
				}
	    	}
		});
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

				var itemRecette = $('<div id="'+token+'" class="row suppaction"><div class="col-md-3">'+result.recipe[0].rec_nom+'</div><div class="col-md-3">'+quantite+'</div><div class="col-md-3">'+prixvente+'</div><div class="col-md-3">'+quantite*prixvente+'<a href="#"><span id="'+token+'-btn" class="btnSuppRecette glyphicon glyphicon-trash"></span></a></div></div>');
				$('#additemrecette').before(itemRecette);

				/* # Event : supprimer une recette dans le pipe */
				callbackDelPlayerPipe()

				/* # Ajout dans la liste pipePlayers */				
				var tmp1 = {};
				var tmp2 = {};
				recette = (result.recipe[0].rec_nom).toString();
				tmp1[recette] = quantite;
				tmp2[recette] = prixvente;

				pipePlayers.actions[0].prepare.push(tmp1);
				pipePlayers.actions[0].price.push(tmp2);
				
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
				if (playerName != ""){
					getBudgetByName()
				}
				var disDay = "Jour "+Math.trunc(result.timestamp/24)+" - "+result.timestamp%24+"H00";
				$('#timer').html(disDay);
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

				/* # Cacher le bouton "Quitter la partie" */
				$('#btnexitgame').addClass('hidden');

				/* # Cacher le paneau "Actions du lendemain" */
				$('#infogamebloc').addClass('hidden');

				$('#inscriptionbloc').removeClass('hidden');

				/* # Vider le panier du player */
				initPipePlayers();

				/* # reinitialiser le jeu */
				gameInit () ;

	    	}
		});
	}

	function suppItems () {
		var itemssupp = $('.suppaction');
		for (var i = 0; i < itemssupp.length; i++) {
			itemssupp[i].remove();
		};
	}



	/**
	*
	*/
	function gameRejoin(name) {
		var data = {"name": name}
		var title, msg ,status;

		$.ajax({
			url: "/players",
			data : JSON.stringify(data),
			type: "POST",
			contentType: 'application/json',
			 
		    success: function(result,textStatus) {
		
	    		resetFormGameJoin();

	        	/* Supprimer le bloque rejoindre la partie */
	        	$('#inscriptionbloc').addClass('hidden');

	        	/* Mise à jour des informations relatives au player */
	        	$('#username').html(result.name);
	        	playerName = result.name
	        	$('#budgetplayer').html(result.info.cash)

	        	/* Affichage d'un message de bienvenue */
	        	var title = 'Coucou '+playerName+'. ';
	        	var msg = 'C est bon de vous voir :) !';
	        	var status = 'success';
	        	showMessage(title,msg,status);

	        	/* Afficher l'interface de simulation */
	        	$('#infogamebloc').removeClass("hidden");
	        	$('#btnexitgame').removeClass('hidden');

	        	exitGame();
		    	
		    	
		    },
		    complete : function(jqXHR,textStatus ){
		    	
		    	if(textStatus == "412"){
		    		title = 'Impossible de rejoindre la partie !';
			    	msg = 'Le pseudo '+result.name+' est déjà utilisé. Merci de saisir un nouveau pseudo.';
			    	status = 'warning';
			      	showMessage(title,msg,status);
		    	}
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

		if(playerName != ""){
			$('#infogamebloc').removeClass("hidden");

			/* # Confirmation du player pour quitter une partie */
			exitGame();
		}else{
			$('#username').html("");
			$('#infogamebloc').addClass("hidden");
		}

	  	/* # Liste de joueurs */
	  	getPlayers();

	  	if($('#blocSimul') != undefined)
	 		getRepices();


	}

	function exitGame () {
		window.onbeforeunload = function(event) {
		    return "Etes-vous sûr de quitter la partie ?";
		}
	}

	function resetGame() {
		$.ajax({
			url: "/reset",
			type: "GET",
			success: function(result){
				if(result == "ok"){

					/* # Cacher le bouton "Quitter la partie" */
					$('#btnexitgame').addClass('hidden');

					/* # Cacher le paneau "Actions du lendemain" */
					$('#infogamebloc').addClass('hidden');

					$('#inscriptionbloc').removeClass('hidden');

					/* # Vider le banier du player */
					initPipePlayers();
					suppItems ();

					/* # reinitialiser le jeu */
					gameInit () ;

					setTimeout(function () {
						var title = 'Réinitialisation de la partie. ';
						var msg = ' La partie a été réinitialisation avec succès !';
						var status = 'success';
						showMessage(title,msg,status);
					},1000)
				}
				
	    	}
		});
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
		})
	}


	function initPipe () {
		pipePlayers = { "actions" : 
			[
				{
					"kind" : "drinks",
					"prepare" : [],
					"price" : []
				}
			]
		};
	}


	function initPipePlayers () {
		pipePlayers = { "actions" : 
			[
				{
					"kind" : "drinks",
					"prepare" : [],
					"price" : []
				}
			]
		};
		playerName = "";
	}


	/**
	*
	*/
	function sendAction() {
		$.ajax({
			url: "/actions/"+playerName,
			data : JSON.stringify(pipePlayers),
			type: "POST",
			contentType: 'application/json',
			success: function(result){
				var title, msg, status;

				if(result.sufficientFunds == "false"){
					title = 'Solde insuffisant :';
					msg = 'Vous ne pouvez pas acheter ces boissons !';
					status = 'danger';
					showMessage(title,msg,status)
					initPipe(); /* Je vide le panier si le budget est insuffisant */
				}else if(result.sufficientFunds == "true"){
					if(result.already == '1'){
						title = 'Attention :';
						msg = 'Certaine(s) de vos boissons n ont pas ete rajoute car vous les avez deja achetees ce jour-ci !';
						status = 'warning';
						showMessage(title,msg,status)
					}else{
						title = 'Félicitations :';
						msg = 'Vos boissons ont été ajoutés avec succès !';
						status = 'success';
						showMessage(title,msg,status)

					}	
				}
				/* # Vide le panier */
				initPipe();
				suppItems ();
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
