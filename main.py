
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

TEMPS =  {"timestamp" : "24","weather" : {"dfn" : "0", "weather" : random.choice(WEATHER)}}

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

dataMatt = {
  "map" : {
    "region" :{
      "center" : {
        "latitude": 40.2,
        "longitude" : 40.2
      },
      "span" : {
        "latitudeSpan" : 40.2,
        "longitudeSpan" : 44.2
      }
    },
    "ranking":[
      "mat","jul"
    ],
    "itemsByPlayer" : {
      "mat":[{
        "kind" : "STAND",
        "owner" : "michel",
        "location":{
          "latitude" : 40.2,
          "longitude" : 40.2
        },
        "influence" : 40.3
      }],
      "jul" :[{
        "kind" : "STAND",
        "owner" : "michel",
        "location":{
          "latitude" : 40.2,
          "longitude" : 40.2
        },
        "influence" : 40.3
      }]
    },
    "playerInfo" : {
      "mat" : {
        "cash" : 40.3,
        "sales" : 40,
        "profit" : 40,
        "drinksOffered" : [{
          "name" : "the",
          "price" : 40.3,
          "hasAlcohol" : "false",
          "isCold" : "false"
        }]
      },
      "jul":{
        "cash" : 40.3,
        "sales" : 40,
        "profit" : 40,
        "drinksOffered" : [{
          "name" : "the",
          "price" : 40.3,
          "hasAlcohol" : "false",
          "isCold" : "false"
        }]
      }
    },
    "drinksByPlayer" : {
      "mat" : [{
        "name" : "the",
        "price" : 40.3,
        "hasAlcohol" : "false",
        "isCold" : "false"
      }],
      "jul" : [{
        "name" : "the",
        "price" : 40.3,
        "hasAlcohol" : "false",
        "isCold" : "false"
      }]
    }
  }
  }

meteos = {
	"timestamp" : 0,
	"weather" : {
		"dfn" : 0, # aujourdhui = 0, demain = 1
		"weather" : random.choice(WEATHER)
	}
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

def makePlayerInfo(pl_name):
	info = CalculeMoneyInfo(pl_name)
	return makeJsonResponse(info)

def makeDrinkInfo(name):

	db = Db()
	price = CalculePriceRec(name)
	info = db.select("SELECT rec_nom, rec_alcohol, rec_cold FROM Recipe WHERE rec_nom = '"+ name +"'")
	db.close()

	drinkInfo  = [{ "name" : info[0]["rec_nom"] }, { "price" : price['sum'] }, { "hasAlcohol" : info[1]['rec_alcohol'] }, { "isCold" : info[2]['rec_cold'] }]
	return makeJsonResponse(drinkInfo)



# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Fonction : Permet de calculer les info monetaires du joueur (son budget courant & son profit depuis le debut de la partie)
# paramsIn : a voir, peut etre type Json, liste, variable
# paramsOut : data de type JSON
def CalculeMoneyInfo(player):

	db = Db()

	budget_ini = db.select("SELECT pl_budget_ini FROM Player WHERE pl_pseudo = '"+ player +"'")
	player_id = db.select("SELECT p.pl_id FROM Player p WHERE pl_pseudo = '"+ player +"'")

	print (player_id)

	sales = CalculeSales(player_id[0]["pl_id"])
	spending = CalculeSpend(player_id[0]["pl_id"])

	cash = float(budget_ini[0]['pl_budget_ini']) - float(spending[0]["sum"]) + float(sales[0]["sum"])
	profit = float(sales[0]["sum"]) - float(spending[0]["sum"])

	db.close()

	return makeJsonResponse({ "cash" : cash, "profit" : profit, "sales" : sales })

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Fonction : Permet de calculer les ventes globales (en euros) du joueur depuis le debut de la partie.
# paramsIn : id du joueur (en Json ? En variable ? Liste?)
# paramsOut : data de type JSON
def CalculeSales(player_id):

	db = Db()
	sales = db.select("SELECT SUM(t.qte_sale * t.price) FROM Transaction t WHERE t.pl_id = '" + str(player_id) + "'")
	db.close()

	return makeJsonResponse(sales)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Fonction : Permet de calculer les depenses globales (en euros) du joueur depuis le debut de la partie.
# paramsIn : id du joueur (en Json ? En variable ? Liste?)
# paramsOut : data de type JSON
def CalculeSpend(player_id):
	db = Db()
	spending = db.select("SELECT SUM(t.qte_prev * (SELECT SUM(i.ing_prix) FROM Ingredient i INNER JOIN Contains c ON i.ing_id = c.ing_id INNER JOIN Recipe r ON r.rec_id = c.rec_id WHERE r.rec_id = t.rec_id) ) FROM Transaction t WHERE t.pl_id = '"+ str(player_id) +"'")
	db.close()
	return makeJsonResponse(spending)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Fonction : Permet de calculer le prix d'une recette
# paramsIn : id de la recette (en Json ? En variable ? Liste?)
# paramsOut : data de type JSON
def CalculePriceRec(name):

	db = Db()
	price_rec = ("SELECT SUM(i.ing_prix) FROM Ingredient i INNER JOIN Contains c ON i.ing_id = c.ing_id INNER JOIN Recipe r ON r.rec_id = c.rec_id WHERE r.rec_id = '"+ name +"'")
	db.close()

	return makeJsonResponse(price_rec)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Fonction : Permet de convert une liste en JSON et ajouter le code de retour.
# paramsIn : data de type list
# paramsOut : data de type JSON
def makeJsonResponse(data,status=200):
	return json.dumps(data), status, {'Content-Type': 'application/json'}


# R8 - Reinitialisation d une partie
# GET /reset
@app.route('/reset',methods=['GET'])
def resetSimulation():
	GAMEINFO = []
	return '', 200


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# R4.1 - Affiche la liste de joueur
# GET /players
@app.route('/players',methods=['GET'])
def getPlayers():
	db = Db()
	playersInfo = db.select("SELECT * FROM Player")
	db.close()
	return makeJsonResponse({ "players" : playersInfo },200)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# R4.2 - Rejoindre une partie
# POST /players
@app.route('/players', methods=['POST'])
def rejoin():
	data = request.get_json()
	playerName = data['playerName']
	db = Db()

	info = db.select("SELECT pl_pseudo FROM Player WHERE pl_pseudo = '"+ playerName +"'")

	print (info)

	if len(info) == 0 :
		db.execute("""INSERT INTO Player(pl_pseudo, pl_budget_ini) VALUES (@(playerName), 100);""", data)
		db.execute(""" INSERT INTO stand(loc_coordX, loc_coordY, loc_rayon, pl_id)
			       SELECT 0,0,0, player.pl_id FROM Player player where pl_pseudo = @(playerName); """, data)
	else:
		return makeJsonResponse(data,400)




	coordinates = db.select("SELECT loc_coordX, loc_coordY FROM Stand WHERE pl_id = (SELECT player.pl_id FROM Player player WHERE pl_pseudo = '"+ playerName +"' )")
	playerInfo =  makePlayerInfo(playerName)
	db.close()
	return makeJsonResponse({ "name" : playerName, "location" : coordinates, "playerInfo" : playerInfo })


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
@app.route('/sales', methods=['POST'])
def simulCmd():
	data = request.get_json()

	return makeJsonResponse(data)


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

	return makeJsonResponse(dataMatt)


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
# R10 - Obtenir la liste des recettes -------------- OK, MANQUE A AFFICHER LE PRIX ----------
# GET /recipes
@app.route('/recipes',methods=['GET'])
def getRecipes():
	db = Db()
	recipes_List = db.select("SELECT * FROM Recipe")
	db.close()
	return makeJsonResponse({ "recipes": recipes_List })


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# R10 - Obtenir une recette a partir de son nom ---------------- OK, MANQUE A AFFICHER LE PRIX --------------------
# GET /recipes/<int:rc_id>
@app.route('/recipe/<int:rc_id>',methods=['GET'])
def getRecipeById(rc_id):
	db = Db()
	recipe = db.select("SELECT * FROM Recipe WHERE rec_id = '"+ str(rc_id) +"'")
	ingredient_list = db.select("SELECT ing.* FROM Ingredient ing INNER JOIN Contains con ON ing.ing_id = con.ing_id INNER JOIN Recipe rec ON rec.rec_id = con.rec_id WHERE rec.rec_id = '"+ str(rc_id) +"'")

	if len(recipe) > 0:
		return makeJsonResponse({ "recipe": recipe, "ingredients": ingredient_list } )
	else:
		return '"Recipe Not Found"', 412
	db.close()

if __name__ == "__main__":
    app.run()
