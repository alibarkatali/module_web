
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

cash_init = 100;

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
def makeJsonResponse(data,status=200):
	return json.dumps(data), status, {'Content-Type': 'application/json'}


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
	return makeJsonResponse(playersList)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# R4.2 - Rejoindre une partie
# POST /players
@app.route('/players', methods=['POST'])
def rejoin():
	data = request.get_json()
	playerName = data['playerName']
	db = Db()

	info = db.select("SELECT pl_pseudo FROM Player WHERE pl_pseudo = '" + playerName +"'")

	print (info)

	if len(info) == 0 :
		db.execute("""INSERT INTO Player(pl_pseudo) VALUES (@(playerName));""", data)
		db.execute(""" INSERT INTO stand(loc_coordX, loc_coordY, loc_rayon, pl_id)
			       SELECT 0,0,0, player.pl_id FROM player player where pl_pseudo = @(playerName); """, data)
	else:
		return makeJsonResponse(data,400)

	db.close()
 	return makeJsonResponse(data)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# R1/R7 - Commande "Temps"
# GET /metrology
@app.route('/metrology',methods=['GET'])
def getMetrology():
	return makeJsonResponse(meteos)

# R1/R7 - Commande "Temps"
# POST /metrology
@app.route('/metrology',methods=['POST'])
def setMetrology():
	data = request.get_json()
	TEMPS['timestamp'] = data['timestamp']
	TEMPS['weather'] = data['weather']
	return makeJsonResponse(TEMPS)


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

	return makeJsonResponse(SALE)


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
# R9 - Obtenir la liste des ingredients ----------- OK ---------------
# GET /ingredients
@app.route('/ingredients',methods=['GET'])
def getIngredients():
	db = Db()
	ingredient_list = db.select("SELECT ing_nom, ing_prix, ing_alcohol, ing_cold FROM Ingredient")
	db.close()
	return makeJsonResponse({ "ingredients": ingredient_list })


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# R10 - Obtenir la liste des recettes
# GET /recipes
@app.route('/recipes',methods=['GET'])
def getRecipes():
	db = Db()
	recipes_List = db.select("SELECT rec_nom FROM Recipe")
	db.close()
	return makeJsonResponse({ "recipes": recipes_List })


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# R10 - Obtenir une recette a partir de son nom
# GET /recipes/<name>
@app.route('/recipes/<name>',methods=['GET'])
def getRecipeByName(name):
	db = Db()
	recipe = db.select("SELECT rec_nom,rec_alcohol,rec_cold FROM Recipe WHERE rec_nom = '"+ name +"'")
	ingredient_list = db.select("SELECT ing.ing_nom FROM Ingredient ing INNER JOIN Contains con ON ing.ing_id = con.ing_id INNER JOIN Recipe rec ON rec.rec_id = con.rec_id WHERE rec.rec_nom = '"+ name +"'")

	if len(recipe) > 0:
		return makeJsonResponse({ "recipe": recipe, "ingredients": ingredients_list } )
	else:
		return '"Recipe Not Found"', 412
	db.close()

if __name__ == "__main__":
    app.run()
