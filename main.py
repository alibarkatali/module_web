from flask import Flask, request
from flask_cors import CORS
import random
import func
import json
from db import Db

app = Flask(__name__)
app.debug = True
CORS(app)

# VARIABLES GLOBALES
db = Db()


@app.route('/reset',methods=['GET'])
def resetSimulation():
	""" Permet de reinitialiser la partie en cours
		...
	"""
	gameId = getDayIdCurr()

	if gameId[0]["max"] == None:
		func.creerGame()
	else:
		func.supprimerGame(gameId[0]["max"])
		func.creerGame()


	return func.makeJsonResponse(OK)

@app.route('/players',methods=['GET'])
def getPlayers():
	""" Retourne la liste des participants dans la partie en cours
		...
	"""
	# On regarde ceux present dans la partie (table Participate)
	playersInfo = db.select("SELECT pl.pl_pseudo FROM Player pl INNER JOIN Participate par ON par.pl_id = pl.pl_id WHERE par.present = true")
	
	return func.makeJsonResponse({ "players" : playersInfo },200)


@app.route('/players', methods=['POST'])
def rejoin():
	""" Permet de joindre la partie en cours
		...
	"""

	data = request.get_json()

	# Je verifie que le pseudo de ce joueur n'existe deja pas
	info = db.select("SELECT pl_pseudo FROM Player WHERE pl_pseudo = '"+ data['name'] +"'")

	if len(info) > 0 :
		return func.makeJsonResponse(data,400)

	gameId = func.recupGameId()

	longI = db.select("SELECT ga_longitude FROM Game WHERE ga_id = '"+ str(gameId) +"'")[0]["ga_longitude"] 
	latI = db.select("SELECT ga_latitude FROM Game WHERE ga_id = '"+ str(gameId) +"'")[0]["ga_latitude"]
	
	# Coordonnees du stand generees aleatoirement
	data['longitude'] = random.uniform(0, longI)
	data['latitude'] = random.uniform(0, latI)

	# J'incris le joueur avec son nom et son budget initial (100, fixe)
	db.execute("""INSERT INTO Player(pl_pseudo, pl_budget_ini) VALUES (@(name), 100);""", data)

	# Je lui affilie un stand avec les coordonnees generees
	db.execute("""
					INSERT INTO stand(loc_longitude, loc_latitude, loc_rayon, pl_id)
		       		SELECT @(longitude), @(latitude),20, player.pl_id FROM Player player 
					WHERE pl_pseudo = @(name); 
			  """, data)
	# J'update la table Participate afin de dire que ce nouveau candidat participe a la partie courante
	db.execute("""	
					INSERT INTO Participate(present, ga_id, pl_id) 
					SELECT 'true', '"""+ str(gameId) +"""', player.pl_id FROM Player player 
					WHERE pl_pseudo = @(name); 
			  """, data)		

	# J'appelle la fonction playerInfo qui cree une donne Json type PlayerInfo
	playerInfo =  func.makePlayerInfo(data['name'])
	

	return func.makeJsonResponse({ "name" : data['name'], "location" : { "latitude" : data['latitude'], "longitude" : data['longitude']}, "info" : playerInfo })


@app.route('/metrology',methods=['GET'])
def getMetrology():
	""" Retourne le timestamp, la meteo d'aujourd'hui et la meteo de demain
		...
	"""
	# On prend la meteo d'aujourd'hui
	weather = db.select("SELECT * FROM Date ORDER BY da_id DESC LIMIT 1")

	# Mettre test de nullite des donnees

	if len(weather):
		wToday = weather[0]["da_weather"]
		wTomorrow = weather[0]["da_weather_tomorrow"]
		tStam = weather[0]["da_timestamp"]
		dDay = weather[0]["da_day"]

		outData = {
		"timestamp" : tStam+24*dDay,
		"weather" : [ {
		        "weather" : wToday,
		        "dfn" : 0,
		    },
		    {
		        "weather" : wTomorrow,
		        "dfn" : 1,
		    }]
		}
	else:
		return func.makeJsonResponse({},2000)

	return func.makeJsonResponse(outData)


@app.route('/metrology',methods=['POST'])
def setMetrology():
	""" Permet de poster le timestamp, la meteo d'aujourd'hui et la meteo de demain
		...
	"""

	data = request.get_json()
	dataSql = {}
	weatherToday = None
	weatherTomorrow =  None

	# Dernier jour du jeu
	result = db.select("SELECT da_id, da_day FROM Date ORDER BY da_id DESC LIMIT 1")
	if len(result) == 0:
		lastDay = 1
	else:
		lastDay = result[0]['da_day']

	# Le Timestamp
	timestamp = int(data['timestamp'])

	# La meteo d'aujourd'hui et de demain
	for weather in data['weather']:
		if weather['dfn'] == '0':
			weatherToday = weather['weather']
		else:
			weatherTomorrow = weather['weather']

	dataSql['weatherToday'] = weatherToday
	dataSql['weatherTomorrow'] = weatherTomorrow
	dataSql['timestamp'] = timestamp%24
	dataSql['lastDay'] = lastDay
	dataSql['da_id'] = result[0]['da_id']

	dataSql['day'] = int(timestamp/24)
	if dataSql['day'] != result[0]['da_day']:
		# Insertion dans la base
		db.execute("""INSERT INTO Date(da_day, da_weather, da_weather_tomorrow, da_timestamp) 
			VALUES (@(day),@(weatherToday),@(weatherTomorrow),@(timestamp));""", dataSql)
	else:
		db.execute("""UPDATE Date da SET da_timestamp = @(timestamp) WHERE da.da_day = @(lastDay) AND da.da_id = @(da_id);""", dataSql)

	return func.makeJsonResponse(data,200)


@app.route('/players/<playerName>', methods=['DELETE'])
def leave(playerName):
	""" Permet de supprimer un joueur dans la partie en cours
		...
	"""

	plId = func.recupIdFromName(playerName)
	# Je le passe a 'false' dans la table Participate
	db.execute("""UPDATE Participate par SET present = 'false' WHERE par.pl_id = '"""+ str(plId) +"""';""")
	
	return func.makeJsonResponse("OK")


@app.route('/sales', methods=['POST'])
def simulCmd():
	""" Inserer les ventes du joueur apres simulation JAVA
		...
	"""
	
	day = func.getDayIdCurr()
	data = request.get_data()
	datas = json.loads(data)

	for rows in datas["sales"]:
	
		if len(rows['item']) > 0:
		
			# Alors le joueur n'a rien mit en vente : la table Transaction n'a pas ete remplit
			playerId = func.recupIdFromName(rows['name'])
			recId = func.recupIdRecFromName(rows['item'])
			qte = rows['quantity']
		
			db.execute("""
					UPDATE Transaction SET qte_sale = '"""+ str(qte) +"""' WHERE da_id = '"""+ str(day) +"""' 
					AND pl_id = """+ str(playerId) +"""' 
					AND rec_id = """+ str(recId) +"""';
				   """)
			

	return func.makeJsonResponse(OK)



@app.route('/actions/<playerName>',methods=['POST'])
def simulActions(playerName):
	""" Permet d'effectuer les actions possibles des joueurs
		...
	"""

	listRecipe = []
	tmp = {}
	data = request.get_json()

	# Si le player ne demande pas d'actions
	if not data['actions']:
		return '"Not find actions"', 412

	#if not data['simulated']:
	#	return '"Not find simulated"', 412

	# On recupere l'ID du player
	playerInfo = func.recupIdFromName(playerName)

	# Si le player n'existe pas
	if len(playerInfo) <= 0:
		return '"Player ID Not Found"', 412

	tmp['playerId'] = playerInfo[0]['pl_id']

	# On recupere le jour en cours
	dayInfo = func.getDayIdCurr()

	if len(playerInfo) <= 0:
		return '"Current day Not Found"', 412

	tmp['dayId'] = dayInfo[0]['da_id']

	totalCost = 0
	if playerName :

		for action in data['actions']:

			# Action pour ajouter les recettes dans la base de donnees
			if action['kind'] == "drinks":

				for prepare in action['prepare']:
					for k, v in prepare.iteritems():
						listRecipe.append({"recipeId":k,"quantity":v,"price":0})
					print prepare

				for price in action['price']:
					for k, v in price.iteritems():						
						for re in listRecipe:
							if re['recipeId'] == str(k):
								re['price'] = v
			print listRecipe

			# insertion dans la base de donnees
			for drinksOffered in listRecipe:
				
				tmp['recipeId'] = drinksOffered['recipeId']
				tmp['quantity'] = drinksOffered['quantity']
				tmp['price'] = drinksOffered['price']

				totalCost += drinksOffered['quantity'] * drinksOffered['price']

				db.execute("""INSERT INTO Transaction(pl_id, rec_id, da_id, price, qte_prev) 
					VALUES ( @(playerId), @(recipeId), @(dayId), @(price), @(quantity) );""", tmp)


	if totalCost <= func.calculeMoneyInfo(playerName,1)['cash']:
		sufficientFunds = "true"
	else:
		sufficientFunds = "false"

	return func.makeJsonResponse({ "sufficientFunds" : sufficientFunds, "totalCost" : totalCost})


@app.route('/map',methods=['GET'])
def getMap():
	""" Retourne l'ensemble des informations relatives aux joueurs dans la partie
		...
	"""

	tmp = db.select("SELECT ga_id FROM Game WHERE ga_run = 'true'")
	if len(tmp) > 0 :
		game_id = tmp[0]["ga_id"]

		itemByPlayer = {}
		playerInfo = {}
		drinkByPlayer = {}

		players_actifs_id = db.select("""SELECT par.pl_id FROM Participate par 
										 INNER JOIN Game ga ON par.ga_id = ga.ga_id 
										 WHERE par.ga_id = '"""+ str(game_id) +"""' AND par.present = 'true'""")

		for players in players_actifs_id:	
			pseudo = db.select("SELECT pl_pseudo FROM Player WHERE pl_id = '"+ str(players["pl_id"]) +"'")[0]["pl_pseudo"]
			itemByPlayer[pseudo] = func.makeMapItem(players["pl_id"])
			playerInfo[pseudo] = func.makePlayerInfo(pseudo)
			drinkByPlayer[pseudo] = func.makeDrinkEveryTime(pseudo)
	
		ranking = func.rankingPlayer(game_id)
		region = func.makeRegion(game_id)

	else:
		return '"Game ID Not Found"', 412

	map = { "region" : region, "ranking" : ranking, "itemsByPlayer" : itemByPlayer , "playerInfo" : playerInfo, "drinksByPlayer" : drinkByPlayer }
	return func.makeJsonResponse({ "map" : map })


@app.route('/map/<playerName>',methods=['GET'])
def getPlayerMap(playerName):
	""" Retourne l'ensemble des informations relatives a un joueur
		...
	"""
	
	player_id = func.recupIdFromName(playerName)
	game_id = func.recupGameId()

	plInfo = func.makePlayerInfo(playerName)
	region = func.makeRegion(game_id)
	itemPlayer = func.makeMapItem(player_id)

	availableIngredients = func.getAvailableIngredients(playerName)

	map = { "availableIngredients" : availableIngredients, "region" : region, "itemPlayer" : itemPlayer }
	return "Obtenir les details d une partie (Client Web)"


@app.route('/ingredients',methods=['GET'])
def getIngredients():
	""" Retourne l'ensemble des ingredients disponibles
		...
	"""

	ingredient_list = db.select("SELECT ing_nom, ing_prix, ing_alcohol, ing_cold FROM Ingredient")

	return func.makeJsonResponse({ "ingredients": ingredient_list })


@app.route('/recipes',methods=['GET'])
def getRecipes():
	""" Retourne l'ensemble des recettes disponibles
		...
	"""

	recipes_List = db.select("SELECT * FROM Recipe")

	return func.makeJsonResponse({ "recipes": recipes_List })


@app.route('/recipe/<int:rc_id>',methods=['GET'])
def getRecipeById(rc_id):
	""" Retourne une recette
		...
	"""

	recipe = db.select("SELECT * FROM Recipe WHERE rec_id = '"+ str(rc_id) +"'")
	ingredient_list = db.select("""SELECT ing.* FROM Ingredient ing 
								   INNER JOIN Contains con ON ing.ing_id = con.ing_id 
								   INNER JOIN Recipe rec ON rec.rec_id = con.rec_id 
								   WHERE rec.rec_id = '"""+ str(rc_id) +"""'""")

	if len(recipe) > 0:
		return func.makeJsonResponse({ "recipe": recipe, "ingredients": ingredient_list } )
	else:
		return '"Recipe Not Found"', 412

@app.route('/player/info/<playerName>', methods=['GET'])
def getInfoPlayer(playerName):
	
	playerInfo = func.makePlayerInfo(playerName)
	return func.makeJsonResponse(playerInfo)
	

if __name__ == "__main__":
    app.run()
