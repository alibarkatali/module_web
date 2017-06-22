
from flask import Flask, request
from flask_cors import CORS
import json
import random
from db import Db

app = Flask(__name__)
app.debug = True
CORS(app)

WEATHER = ["RAINNY","CLOUDY","SUNNY","HEATWAVE","THUNDERSTORM"]

COORDINATES = {}

FORECAST = {
	"dfn" : 0, # aujourdhui = 0, demain = 1
	"weather" : random.choice(WEATHER)
}

#TEMPS = {
#	"timestamp" : 0, # nombre d heure ecoulees depuis le debut du jeu
#	"weather" : random.choice(WEATHER)
#}

# {"timestamp" : "24","weather" : {"dfn" : "0", "weather" : "RAINNY"}}

TEMPS = {}

COORDINATESSPAN = {
	"latitudeSpan" : 0.0,
	"longitudeSpan" : 0.0
}

REGION = {
	"center" : COORDINATES,
	"span" : COORDINATESSPAN
}

MAPITEM = {
	"kind" : "", # accepte la valeur : "stand" ou "ad"
	"owner" : "", # le player
	"location" : "", # localisation dans la map
	"influence" : 0.0 # distance
}

PLAYERINFO = {
	"cash" : 1000.0, # le budget initial du player
	"sales" : 0, # nombre de boissons consommes = solde - total, pour toutes les recettes
	"profit" : 0 # le chiffre d affaire de la vente, si < 0 il a perdu la partie
}

GAMEINFO = {}

DRINKINFO = {
	"name" : "None",
	"price": 0.0
}

#MAP = {
#	"region" : REGION,
#	"ranking" : [] # les noms des players
#	"itemByPlayer" : [], 
#	"playerInfo" : [], 
#	"drinkByPlayer" : [] 
#}

SALE = {
	"player" : "None", # nom du player
	"item" : "None", # nom de la recette achater
	"quantity" : 0 # combien d article vendus
}

INGREDIENT = []

INGREDIENT.append({
			"name" : "sucre",
			"cost" : 2,
			"hasAlcohol" : 0, # 0 : non alcole, 1 : alcolise,  2 : autres
			"isCold" : 2 # 0 : pas chaud, 1 : chaud,  2 : autres
		}
	)

INGREDIENT.append({
			"name" : "eau gazeuse",
			"cost" : 1.5,
			"hasAlcohol" : 2, # 0 : non alcole, 1 : alcolise,  2 : autres
			"isCold" : 0 # 0 : pas chaud, 1 : chaud,  2 : autres
		}
	)

INGREDIENT.append({
			"name" : "citrone",
			"cost" : 3,
			"hasAlcohol" : 2, # 0 : non alcole, 1 : alcolise,  2 : autres
			"isCold" : 0 # 0 : pas chaud, 1 : chaud,  2 : autres
		}
	)

INGREDIENT.append({
			"name" : "cafe moulu",
			"cost" : 5,
			"hasAlcohol" : 0, # 0 : non alcole, 1 : alcolise,  2 : autres
			"isCold" : 1# 0 : pas chaud, 1 : chaud,  2 : autres
		}
	)

INGREDIENT.append({
			"name" : "eau",
			"cost" : 0,
			"hasAlcohol" : 0, # 0 : non alcole, 1 : alcolise,  2 : autres
			"isCold" : 2 # 0 : pas chaud, 1 : chaud,  2 : autres
		}
	)

RECIPE = {
	"name" : "Limonade",
	"ingredients" : INGREDIENT,
	"hasAlcohol" : 0, # 0 : non alcole, 1 : alcolise,  2 : autres
	"isCold" : 0 # 0 : pas chaud, 1 : chaud,  2 : autres
}

PLAYERACTION = {
	"name" : "None", # prends une valeur : recipe ou ppurchase ou pub
}

PLAYERACTIONNEWRECIPE = {
	"kind" : "recipe",
	"recipe" : RECIPE
}

PLAYERACTIONAD = {
	"kind" : "ad",
	"location" : COORDINATES
}

PLAYERACTIONDRINKS = {
	"kind" : "drink",
	"prepare" : {
		"limonade" : 0 
	}
}

################################################################
####	VARIABLES DES TESTS

playersList = []
recipesList = {}

meteos = {
	"timestamp" : 0,
	"weatherToday" : random.choice(WEATHER),
	"weatherTomorow" : random.choice(WEATHER)
}

recipesList['Limonade'] = {
		"name" : "Limonade",
		"ingredients" : [
			{
				"name" : "sucre",
				"cost" : 2,
				"hasAlcohol" : 0, 
				"isCold" : 2 
			},
			{
				"name" : "eau gazeuse",
				"cost" : 1.5,
				"hasAlcohol" : 2, 
				"isCold" : 0 
			},
			{
				"name" : "citrone",
				"cost" : 3,
				"hasAlcohol" : 2, 
				"isCold" : 0 
			}
		],
		"hasAlcohol" : 0, # 0 : non alcole, 1 : alcolise,  2 : autres
		"isCold" : 0 # 0 : pas chaud, 1 : chaud,  2 : autres
	}

recipesList['Cafe'] = {
		"name" : "Cafe",
		"ingredients" : [
			{
				"name" : "cafe moulu",
				"cost" : 5,
				"hasAlcohol" : 0, # 0 : non alcole, 1 : alcolise,  2 : autres
				"isCold" : 1# 0 : pas chaud, 1 : chaud,  2 : autres
			},
			{
				"name" : "eau",
				"cost" : 0,
				"hasAlcohol" : 0, # 0 : non alcole, 1 : alcolise,  2 : autres
				"isCold" : 2 # 0 : pas chaud, 1 : chaud,  2 : autres
			},
			{
				"name" : "sucre",
				"cost" : 2,
				"hasAlcohol" : 0, 
				"isCold" : 2 
			}
		],
		"hasAlcohol" : 0, # 0 : non alcole, 1 : alcolise,  2 : autres
		"isCold" : 0 # 0 : pas chaud, 1 : chaud,  2 : autres
	}



####	FIN VARIABLES DES TESTS
################################################################


def joinResponse(name):
	global GAMEINFO
	GAMEINFO['name'] = name
	GAMEINFO['location'] = COORDINATES
	GAMEINFO['info'] = PLAYERINFO

	return GAMEINFO


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Fonction : Permet de convert une liste en JSON et ajouter le code de retour.
# paramsIn : data de type list
# paramsOut : data de type JSON
def getJSONResponse(data):
	return json.dumps(data), 200, {'Content-Type' : 'application/json'}


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# R8 - Reinitialisation d une partie
# GET /reset
@app.route('/reset',methods=['GET'])
def resetSimulation():
	GAMEINFO = []
	return '', 200


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# R4.1 - Affiche la liste de joueur - OK -
# GET /players
@app.route('/players',methods=['GET'])
def getPlayers():
	return getJSONResponse(playersList)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# R4.2 - Rejoindre une partie 
# POST /players
@app.route('/players', methods=['POST'])
def rejoin():
	data = request.get_json()
	playerName = data['playerName']
	db = Db()
	#Info = db.select("SELECT * FROM Player WHERE pl_pseudo = '@(playerName)'")
	if db.select("SELECT EXISTS(SELECT * FROM Player WHERE pl_pseudo = '@(playerName)')"):
		return getJSONResponse(playerName)
	else:
		db.execute("""INSERT INTO Player(pl_pseudo) VALUES (@(playerName));""", data)
		db.execute(""" INSERT INTO stand(loc_coordX, loc_coordY, loc_rayon, pl_id)
			       SELECT 0,0,0, player.pl_id FROM player player where pl_pseudo = @(playerName); """, data)

	db.close()
 	return getJSONResponse(playerName)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# R1/R7 - Commande "Temps"
# GET /metrology
@app.route('/metrology',methods=['GET'])
def getMetrology():
	return getJSONResponse(meteos)

# R1/R7 - Commande "Temps"
# POST /metrology
@app.route('/metrology',methods=['POST'])
def setMetrology():
	data = request.get_json()
	TEMPS['timestamp'] = data['timestamp']
	TEMPS['weather'] = data['weather']
	return getJSONResponse(TEMPS)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# R4.2 - Quitter une partie
# DELETE /players/<playerName>
@app.route('/players/<playerName>', methods=['DELETE'])
def leave(playerName):
	global GAMEINFO
	if not GAMEINFO['name'] not in GAMEINFO:
		return '"Not find player"', 412
	
	GAMEINFO['name'].remove()

	return '', 200


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# R3 - Commande "simulateur"
# POST /sales
@app.route('/sales',methods=['POST'])
def simulCmd():
	data = request.get_json()
	for sale in data:
		SALE.append(sale)
	return getJSONResponse(SALE)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# R6 - Instructions du joueur pour le jour suivant
# POST /actions/<playerName>
@app.route('/actions/<playerName>',methods=['POST'])
def simulActions(playerName):
	data = request.get_json()
	if not data['actions']:
		return '"Not find actions"', 412

	if not data['simulated']:
		return '"Not find simulated"', 412

	#if data['simulated'] == True:
		
	return "Instructions du joueur pour le jour suivant"


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# R2 - Obtenir les details d une partie (JAVA)
# GET /map
@app.route('/map',methods=['GET'])
def getMap():
	return "Obtenir les details d une partie (JAVA)"


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# R5 Obtenir les details d une partie (Client Web)
# GET /map/<playerName>
@app.route('/map/<playerName>',methods=['GET'])
def getPlayerMap(playerName):
	return "Obtenir les details d une partie (Client Web)"


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# R9 - Obtenir la liste des ingredients
# GET /ingredients
@app.route('/ingredients',methods=['GET'])
def getIngredients():
	return getJSONResponse(INGREDIENT)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# R10 - Obtenir la liste des recettes
# GET /recipes
@app.route('/recipes',methods=['GET'])
def getRecipes():
	return getJSONResponse(recipesList)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# R10 - Obtenir une recette a partie son nom
# GET /recipes/<name>
@app.route('/recipes/<name>',methods=['GET'])
def getRecipeByName(name):
	recipe = db.select("SELECT * FROM Recipe WHERE rec_nom = '@(name)'")
	if recipe:
		return getJSONResponse(recipe)
	else:
		return '"Recipe Not Found"', 412

if __name__ == "__main__":
    app.run()
