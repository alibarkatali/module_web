from flask import Flask, request
from flask_cors import CORS
import json
import random
from db import Db

app = Flask(__name__)
app.debug = True
CORS(app)

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
          "latitude" : 78.2,
          "longitude" : 56.2
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

def joinResponse(name):
	global GAMEINFO
	GAMEINFO['name'] = name
	GAMEINFO['location'] = COORDINATES
	GAMEINFO['info'] = PLAYERINFO

	return GAMEINFO

def MakeRegion(game_id):

	db = Db();

	coord = db.select("SELECT ga_centrex, ga_centrey FROM Game WHERE ga_id = '"+ str(game_id) +"' AND ga_run = 'true'")

	span = db.select("SELECT ga_largeur, ga_longueur FROM Game WHERE ga_id = '"+ str(game_id) +"' AND ga_run = 'true'")

	db.close()

	return ({ "center" : { "longitude" : coord[0]["ga_centrex"], "latitude" : coord[0]["ga_centrey"] }, "span" : { "latitudeSpan" : span[0]["ga_longueur"], "longitude" : span[0]["ga_largeur"] } })


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Fonction : Permet de classer les joueurs, en fonction de leur budget (le plus riche est premier)
# paramsIn : variable
# paramsOut : data de type JSON
def RankingPlayer(game_id):

	ranking = []

	db = Db()

	players_actifs = db.select("SELECT player.pl_pseudo FROM Player INNER JOIN Participate par ON par.pl_id = player.pl_id INNER JOIN Game ga ON par.ga_id = ga.ga_id WHERE par.ga_id = '"+ str(game_id) +"' AND par.present = 'true'")

	for player in players_actifs:
		ranking.append(player["pl_pseudo"])
		#money_info.append({ player["pl_pseudo"] : CalculeMoneyInfo(player["pl_pseudo"], 1) })

	db.close()

	return ranking

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Fonction : Permet de creer une donnee Json de type mapItem
# paramsIn : variable
# paramsOut : data de type JSON
def makeMapItem(pl_id):

	db = Db()
	coordinates = db.select("SELECT loc_longitude, loc_latitude FROM Stand  WHERE pl_id = '"+ str(pl_id) +"'")
	influence = db.select("SELECT loc_rayon FROM Stand WHERE pl_id = '"+ str(pl_id) +"'")[0]["loc_rayon"]
	pl_name = db.select("SELECT pl_pseudo FROM Player WHERE pl_id = '"+ str(pl_id) +"'")[0]["pl_pseudo"]

	db.close()	

	return ({ "kind" : "stand", "owner" : pl_name, "location" : { "latitude" : coordinates[0]['loc_longitude'], "longitude" : coordinates[0]['loc_latitude']}, "influence" : influence })	

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Fonction : Permet de creer une donnee Json de type playerInfo
# paramsIn : variable
# paramsOut : data de type JSON
def makePlayerInfo(pl_name):

	info = CalculeMoneyInfo(pl_name, 0)
	drinkInfo = makeDrinkOffered(pl_name)																																																																																																																																																																										

	return ([{ "cash" : info['cash'], "profit" : info['profit'], "sales" : info['sales'], "drinksOffered" : drinkInfo }])

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Fonction : Permet de calculer les info monetaires du joueur (son budget courant, ses ventes & son profit depuis le debut de la partie)
# paramsIn : variable nom du player, et 0 ou 1 : renvoit toutes les infos si 0, que le budget si 1
# paramsOut : data de type JSON
def CalculeMoneyInfo(player, status=0):

	db = Db()

	budget_ini = db.select("SELECT pl_budget_ini FROM Player WHERE pl_pseudo = '"+ player +"'")[0]["pl_budget_ini"]
	player_id = db.select("SELECT p.pl_id FROM Player p WHERE pl_pseudo = '"+ player +"'")[0]["pl_id"]

	earnings = CalculeEarnings(player_id)
	spending = CalculeSpend(player_id)
	sales = CalculeSales(player_id)

	cash = budget_ini - spending + earnings
	profit = earnings - spending
	
	db.close()

	if status == 0:
		return ({ "cash" : cash, "profit" : profit, "sales" : sales })
	else: 
		return ({ "cash" : cash })


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Fonction : Permet de calculer les info monetaires du joueur (son budget courant & son profit depuis le debut de la partie)
# paramsIn : a voir, peut etre type Json, liste, variable
# paramsOut : data de type dictionnaire
def makeDrinkOffered(pl_name):

	drinkOffered = []

	db = Db()
	
	player_id = db.select("SELECT p.pl_id FROM Player p WHERE p.pl_pseudo = '"+ pl_name +"'")[0]["pl_id"]
	da_max = db.select("SELECT MAX(da_id) FROM Date")[0]["max"]
	drink_id = db.select("SELECT t.rec_id FROM Transaction t WHERE t.pl_id = '"+ str(player_id) +"' AND t.da_id = '"+ str(da_max) +"'")
	
	db.close()
		
	for drink in drink_id:	
		drinkInfo = makeDrinkInfo(drink["rec_id"])	
		drinkOffered.append(drinkInfo)

	return (drinkOffered)
	

def makeDrinkInfo(rec_id):

	db = Db()
	price = CalculePriceRec(rec_id)
	info = db.select("SELECT rec_nom, rec_alcohol, rec_cold FROM Recipe WHERE rec_id = '"+ str(rec_id) +"'")
	db.close()
	
	drinkInfo  = { "name" : info[0]["rec_nom"], "price" : price,  "hasAlcohol" : info[0]["rec_alcohol"], "isCold" : info[0]["rec_cold"] }
	
	return (drinkInfo)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Fonction : Permet de calculer les ventes globales (en euros) du joueur depuis le debut de la partie.
# paramsIn : id du joueur 
# paramsOut :  Nbre (float ou 0)
def CalculeEarnings(player_id):

	db = Db()
	sales = db.select("SELECT SUM(t.qte_sale * t.price) FROM Transaction t WHERE t.pl_id = '" + str(player_id) +"'")[0]["sum"]
	db.close()

	if sales == None:
		return 0
	else: 
		return sales

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Fonction : Permet de calculer le nombre de recette vendu du joueur depuis le debut de la partie.
# paramsIn : id du joueur 
# paramsOut : Nbre (float ou 0)
def CalculeSales(player_id):

	db = Db()
	sales = db.select("SELECT SUM(t.qte_sale) FROM Transaction t WHERE t.pl_id = '" + str(player_id) +"'")[0]["sum"]
	db.close()

	if sales == None:
		return 0
	else: 
		return sales

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Fonction : Permet de calculer les depenses globales (en euros) du joueur depuis le debut de la partie.
# paramsIn : id du joueur (en Json ? En variable ? Liste?)
# paramsOut : data de type JSON
def CalculeSpend(player_id):

	db = Db()
	spending = db.select("SELECT SUM(t.qte_prev * (SELECT SUM(i.ing_prix) FROM Ingredient i INNER JOIN Contains c ON i.ing_id = c.ing_id INNER JOIN Recipe r ON r.rec_id = c.rec_id WHERE r.rec_id = t.rec_id) ) FROM Transaction t WHERE t.pl_id = '"+ str(player_id) +"'")[0]["sum"]
	db.close()

	if spending == None:
		return 0
	else: 
		return spending

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Fonction : Permet de calculer le prix d'une recette
# paramsIn : id de la recette (en Json ? En variable ? Liste?)
# paramsOut : data de type JSON
def CalculePriceRec(rec_id):

	db = Db()
	price_rec = db.select("SELECT SUM(i.ing_prix) FROM Ingredient i INNER JOIN Contains c ON i.ing_id = c.ing_id INNER JOIN Recipe r ON r.rec_id = c.rec_id WHERE r.rec_id	 = '"+ str(rec_id) +"'")[0]['sum']
	db.close()

	return price_rec

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
	playersInfo = db.select("SELECT pl.pl_pseudo FROM Player pl")
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

	if len(info) > 0 :
		return makeJsonResponse(data,400)

	db.execute("""INSERT INTO Player(pl_pseudo, pl_budget_ini) VALUES (@(playerName), 100);""", data)
	db.execute("""INSERT INTO stand(loc_longitude, loc_latitude, loc_rayon, pl_id)
		       SELECT 0,0,0, player.pl_id FROM Player player where pl_pseudo = @(playerName); """, data)
	db.execute("""INSERT INTO Participate(present, ga_id, pl_id) SELECT 'true',1, player.pl_id FROM Player player where pl_pseudo = @(playerName); """, data)		

	coordinates = db.select("SELECT loc_longitude, loc_latitude FROM Stand WHERE pl_id = (SELECT player.pl_id FROM Player player WHERE pl_pseudo = '"+ playerName +"' )")
	playerInfo =  makePlayerInfo(playerName)
	
	db.close()

	return makeJsonResponse({ "name" : playerName, "location" : { "latitude" : coordinates[0]['loc_longitude'], "longitude" : coordinates[0]['loc_latitude']}, "info" : playerInfo })


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# R1/R7 - Commande "Temps"
# GET /metrology
@app.route('/metrology',methods=['GET'])
def getMetrology():
	db = Db()
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
		return '',404
	db.close()
	return makeJsonResponse(outData)


# R1/R7 - Commande "Temps"
# POST /metrology
@app.route('/metrology',methods=['POST'])
def setMetrology():
	data = request.get_json()
	dataSql = {}
	weatherToday = None
	weatherTomorrow =  None
	db = Db()

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

		# lancer le simulateur JAVA

		# Insertion dans la base
		db.execute("""INSERT INTO Date(da_day,da_weather, da_weather_tomorrow,da_timestamp) 
			VALUES (@(day),@(weatherToday),@(weatherTomorrow),@(timestamp));""", dataSql)
	else:
		db.execute("""UPDATE Date SET da_timestamp = @(timestamp) WHERE da_day = @(lastDay);""", dataSql)

	db.close()

	return makeJsonResponse(data,200)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# R4.2 - Quitter une partie
# DELETE /players/<playerName>
@app.route('/players/<playerName>', methods=['DELETE'])
def leave(playerName):
	
	

	return '', 200


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# R3 - Commande "simulateur"
# POST /sales
@app.route('/sales', methods=['POST'])
def simulCmd():
	data = request.get_json()
	# INSERER LES VENTES DANS BDD
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

	# REGARDER DE QUELLES FORMES SONT LES DONNEES POUR LES METTRES DANS LA TABLE Transaction - Easy !!!

	#if data['simulated'] == True:

	return "Instructions du joueur pour le jour suivant"

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# R2 - Obtenir les details d une partie (JAVA)
# GET /map
@app.route('/map',methods=['GET'])
def getMap():
	
	db = Db()

	game_id = db.select("SELECT ga_id FROM Game WHERE ga_run = 'true'")[0]["ga_id"]

	itemByPlayer = {}
	playerInfo = {}
	drinkByPlayer = {}

	players_actifs_id = db.select("SELECT par.pl_id FROM Participate par INNER JOIN Game ga ON par.ga_id = ga.ga_id WHERE par.ga_id = '"+ str(game_id) +"' AND par.present = 'true'")

	for players in players_actifs_id:	
		pseudo = db.select("SELECT pl_pseudo FROM Player WHERE pl_id = '"+ str(players["pl_id"]) +"'")[0]["pl_pseudo"]
		itemByPlayer[pseudo] = makeMapItem(players["pl_id"])
		playerInfo[pseudo] = makePlayerInfo(pseudo)
		drinkByPlayer[pseudo] = makeDrinkOffered(pseudo)
	
	ranking = RankingPlayer(game_id)
	region = MakeRegion(game_id)

	db.close()

	return makeJsonResponse({ "map" : { "region" : region, "ranking" : ranking, "itemsByPlayer" : itemByPlayer , "playerInfo" : playerInfo, "drinksByPlayer" : drinkByPlayer })


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
