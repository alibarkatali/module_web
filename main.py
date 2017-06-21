from flask import Flask, request
from flask_cors import CORS
import json
from db import Db

app = Flask(__name__)
app.debug = True
CORS(app)

WEATHER = ["RAINNY","CLOUDY","SUNNY","HEATWAVE","THUNDERSTORM"]

FORECAST = {
	"dfn" : 0, # aujourdhui = 0, demain = 1
	"weather" : random.choice(WEATHER)
}

TEMPS = {
	"timestamp" : 0, # nombre d heure ecoulees depuis le debut du jeu
	"weather" : random.choice(WEATHER)
}

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

COORDINATES = {}

PLAYERINFO = {
	"cash" : 1000.0, # le budget initial du player
	"sales" : 0, # nombre de boissons consommés = solde - total, pour toutes les recettes
	"profit" : 0 # le chiffre d affaire de la vente, si < 0 il a perdu la partie
}

GAMEINFO = {}

DRINKINFO = {
	"name" : "None",
	"price": 0.0
}

MAP = {
	"region" : REGION,
	"ranking" : [] # les noms des players
	"itemByPlayer" : {
		MAPITEM
	},
	"playerInfo" : {
		PLAYERINFO
	},
	"drinkByPlayer" : {
		DRINKINFO
	}
}

SALE = {
	"player" : "None", # nom du player
	"item" : "None", # nom de la recette achater
	"quantity" : 0 # combien d article vendus
}

INGREDIENT = []

INGREDIENT.append({
			"name" : "sucre",
			"cost" : 2,
			"hasAlcohol" : 0, # 0 : non alcolé, 1 : alcolisé,  2 : autres
			"isCold" : 2 # 0 : pas chaud, 1 : chaud,  2 : autres
		}
	)

INGREDIENT.append({
			"name" : "eau gazeuse",
			"cost" : 1.5,
			"hasAlcohol" : 2, # 0 : non alcolé, 1 : alcolisé,  2 : autres
			"isCold" : 0 # 0 : pas chaud, 1 : chaud,  2 : autres
		}
	)

INGREDIENT.append({
			"name" : "citrone",
			"cost" : 3,
			"hasAlcohol" : 2, # 0 : non alcolé, 1 : alcolisé,  2 : autres
			"isCold" : 0 # 0 : pas chaud, 1 : chaud,  2 : autres
		}
	)

RECIPE = {
	"name" : "Limonade",
	"ingredients" : INGREDIENT,
	"hasAlcohol" : 0, # 0 : non alcolé, 1 : alcolisé,  2 : autres
	"isCold" : 0 # 0 : pas chaud, 1 : chaud,  2 : autres
}

def joinResponse(name):
	global GAMEINFO
	GAMEINFO['name'] = name
	GAMEINFO['location'] = COORDINATES
	GAMEINFO['info'] = PLAYERINFO

	return GAMEINFO

def getJSONResponse(data):
	return json.dumps(data), 200, {'Content-Type' : 'application/json'}

# R8 - Reinitialisation d une partie
# GET /reset
@app.route('/reset',methods=['GET'])
def resetSimulation():
	return "Reinitialisation d une partie"

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# R4.1 - Rejoindre une partie
# POST /players
@app.route('/players',methods=['POST'])
def rejoin():
	data = request.get_json()
	return getJSONResponse(joinResponse(data['name']))

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# R4.2 - Quitter une partie
# DELETE /players/<playerName>
@app.route('/players/<playerName>',methods=['DELETE'])
def leave(playerName):
	global GAMEINFO
	if not GAMEINFO['name'] not in GAMEINFO:
		return '"Not find player"', 412, {'Content-Type' : 'application/json'}
	
	GAMEINFO['name'].remove()

	return '', 200

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# R3 - Commande "simulateur"
# POST /sales
@app.route('/sales',methods=['POST'])
def simulCmd():
	return "Commande simulateur"

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# R6 - Instructions du joueur pour le jour suivant
# POST /actions/<playerName>
@app.route('/actions/<playerName>',methods=['POST'])
def simulActions(playerName):
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
	return "Obtenir la liste des ingredients"


if __name__ == "__main__":
    app.run()
