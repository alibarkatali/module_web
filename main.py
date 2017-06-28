from flask import Flask, request
from flask_cors import CORS
import random
import func
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
	
	

	return '', 200

@app.route('/players',methods=['GET'])
def getPlayers():
	""" Retourne la liste des participants dans la partie en cours
		...
	"""
	
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

	# Je dois recuperer la latitude et longitude de la map normalement
	
	data['longitude'] = random.uniform(0, 700)
	data['latitude'] = random.uniform(0, 400)
	
	db.execute("""INSERT INTO Player(pl_pseudo, pl_budget_ini) VALUES (@(name), 100);""", data)

	db.execute("""
					INSERT INTO stand(loc_longitude, loc_latitude, loc_rayon, pl_id)
		       		SELECT @(longitude), @(latitude),0, player.pl_id FROM Player player 
					WHERE pl_pseudo = @(name); 
			  """, data)

	db.execute("""	
					INSERT INTO Participate(present, ga_id, pl_id) 
					SELECT 'true', '"""+ gameId +"""', player.pl_id FROM Player player 
					WHERE pl_pseudo = @(name); 
			  """, data)		

	coordinates = db.select("""
								SELECT loc_longitude, loc_latitude FROM Stand 
								WHERE pl_id = 
									(SELECT player.pl_id FROM Player player 
									WHERE pl_pseudo = '"""+ data['name'] +"""' )
							""")

	playerInfo =  func.makePlayerInfo(data['name'])
	

	return func.makeJsonResponse({ "name" : data['name'], "location" : { "latitude" : coordinates[0]['loc_longitude'], "longitude" : coordinates[0]['loc_latitude']}, "info" : playerInfo })


@app.route('/metrology',methods=['GET'])
def getMetrology():
	""" Retourne le timestamp, la meteo d'aujourd'hui et la meteo de demain
		...
	"""

	weather = db.select("SELECT * FROM Date ORDER BY da_day DESC LIMIT 1")

	if len(weather):
		wToday = weather[0]["da_weather"]
		wTomorrow = weather[0]["da_weather_tomorrow"]
		tStam = weather[0]["da_timestamp"]

		outData = {
		"timestamp" : tStam,
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
	lastDay = db.select("SELECT da_day FROM Date ORDER BY da_day DESC LIMIT 1")
	if len(lastDay) == 0:
		lastDay = 1
	else:
		lastDay = lastDay[0]['da_day']

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

	if timestamp % 24 == 0 :
		dataSql['day'] = lastDay+1

		# Insertion dans la base
		db.execute("""INSERT INTO Date(da_day,da_weather, da_weather_tomorrow,da_timestamp) 
			VALUES (@(day),@(weatherToday),@(weatherTomorrow),@(timestamp));""", dataSql)
	else:
		db.execute("""UPDATE Date SET da_timestamp = @(timestamp) WHERE da_day = @(lastDay);""", dataSql)

	return func.makeJsonResponse(data,200)


@app.route('/players/<playerName>', methods=['DELETE'])
def leave(playerName):
	""" Permet de supprimer un joueur dans la partie en cours
		...
	"""

	#pl_id = db.select("SELECT pl_id FROM Player WHERE pl_pseudo = "+playerName+"")[0]['pl_id']
	#data['pl_id'] = pl_id
	#db.execute("""UPDATE Participate par SET par.present = 'false' WHERE par.pl_id = @(pl_id);""",data)
	
	return '', 200


@app.route('/sales', methods=['POST'])
def simulCmd():
	""" Retourne les ventes du joueur apres simulation (Programme JAVA)
		...
	"""

	day = func.getDayIdCurr()
	data = request.get_json()
	
	for rows in data['sales']:
		
		playerId = func.recupIdFromName(rows['player'])
		recId = func.recupIdRecFromName(rows['item'])
		
		db.execute("""
					UPDATE Transaction SET qte_sale = @(quantity) WHERE da_id = '"""+ str(day) +"""' 
					AND pl_id = """+ str(playerId) +"""' 
					AND rec_id = """+ str(recId) +"""';
				   """)
			

	return func.makeJsonResponse(data)


@app.route('/actions/<playerName>',methods=['POST'])
def simulActions(playerName):
	""" Permet d'effectuer les actions possibles des joueurs
		...
	"""

	data = request.get_json()
	if not data['actions']:
		return '"Not find actions"', 412

	if not data['simulated']:
		return '"Not find simulated"', 412

	return "Instructions du joueur pour le jour suivant"


@app.route('/map',methods=['GET'])
def getMap():
	""" Retourne l'ensemble des informations relatives aux joueurs
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


if __name__ == "__main__":
    app.run()
