import json
import random
from db import Db

# VARIABLES GLOBALES
db = Db()
gaNom = [ "Shaddock", "Bashunga", "VaChier", "GitansLand", "Iphone", "Pizza" ]

def creerGame():
	
	gameNom = random.choice(gaNom)

	db.execute("INSERT INTO Game(ga_nom, ga_latitude, ga_longitude, ga_centrex, ga_centrey, ga_run) VALUES ('"+ gameNom +"', '500', '700', '350', '250', 'true')")

def supprimerGame(game_id):

	db.execute("UPDATE Game SET ga_run = 'false' WHERE ga_id = '"+ game_id +"'")
	db.execute("UPDATE Participate SET present = 'false' WHERE ga_id = '"+ game_id +"'")
	
def isCold(rec_id):
	
	booleanVar = 'true'
	
	ingredientsList = db.select("""SELECT ing.ing_cold FROM Ingredient ing 
								  INNER JOIN Contains con ON con.ing_id = ing.ing_id 
								  INNER JOIN Recipe rec ON rec.rec_id = con.rec_id
								  WHERE rec.rec_id = '"""+ str(rec_id) +"""'
								""")
	
	for rows in ingredientsList:
		if (not rows['ing_cold']):
			booleanVar = 'false'	
	
	return booleanVar

def hasAlcohol(rec_id):
	
	booleanVar = 'false'	

	ingredientsList = db.select("""SELECT ing.ing_alcohol FROM Ingredient ing 
								  INNER JOIN Contains con ON con.ing_id = ing.ing_id 
								  INNER JOIN Recipe rec ON rec.rec_id = con.rec_id
								  WHERE rec.rec_id = '"""+ str(rec_id) +"""'
								""")
	
	for rows in ingredientsList:
		if (rows['ing_alcohol']):
			booleanVar = 'true'					
	
	return booleanVar

def recupIdRecFromName(rec_name):
	recId = db.select("SELECT rec_id FROM Recipe WHERE rec_nom = '"+ rec_name +"'")[0]["rec_id"]
	return recId	

def recupNameRecFromId(rec_id):
	recName = db.select("SELECT rec_nom From Recipe WHERE rec_id = '"+ str(rec_id) +"'")[0]["rec_nom"]	
	return recName
	
def getDayCurr():
	daMax = db.select("SELECT MAX(da_id) From Date")[0]["max"]
	dayCurr = db.select("SELECT da_day From Date WHERE da_id = '"+ daMax +"'")[0]["da_day"]
	return dayCurr

def getDayIdCurr():	
	daMax = db.select("SELECT MAX(da_id) From Date")[0]["max"]
	return daMax


def recupIdFromName(pl_name):
	plId = db.select("SELECT pl_id FROM Player WHERE pl_pseudo = '"+ pl_name +"'")[0]["pl_id"]
	return plId

def recupGameId():
	gameId = db.select("SELECT ga_id FROM Game WHERE ga_run = 'true'")[0]["ga_id"]
	return gameId

def getAvailableIngredients(pl_name):
	aIng = []
	plId = recupIdFromName(pl_name)

	db.select(""" SELECT ing_nom FROM Ingredient ing 
				  INNER JOIN Contains con ON con.ing_id = ing.ing_id 
				  INNER JOIN Recipe rec ON con.rec_id = rec.rec_id 
				  INNER JOIN Transaction tr ON tr.rec_id = rec.rec_id 
				  WHERE tr.pl_id = '"""+ plId +"""'
			 """)

	return 0

def makeRegion(game_id):
	""" 
		:param arg1: description
		:param arg2: description
		:type arg1: type
		:type arg1: type
		:return: description de la valeur de retour
		:rtype: type de la valeur de retour
	"""

	coord = db.select("SELECT ga_centrex, ga_centrey FROM Game WHERE ga_id = '"+ str(game_id) +"' AND ga_run = 'true'")
	span = db.select("SELECT ga_latitude, ga_longitude FROM Game WHERE ga_id = '"+ str(game_id) +"' AND ga_run = 'true'")

	return ({ "center" : { "longitude" : coord[0]["ga_centrex"], "latitude" : coord[0]["ga_centrey"] }, "span" : { "latitudeSpan" : span[0]["ga_latitude"], "longitudeSpan" : span[0]["ga_longitude"] } })


def rankingPlayer(game_id):
	""" Permet de classer les joueurs, en fonction de leur budget (le plus riche est premier)
		:param arg1: description
		:param arg2: description
		:type arg1: type
		:type arg1: type
		:return: description de la valeur de retour
		:rtype: type de la valeur de retour
	"""

	ranking = []

	players_actifs = db.select("""	SELECT player.pl_pseudo FROM Player 
									INNER JOIN Participate par ON par.pl_id = player.pl_id 
								    INNER JOIN Game ga ON par.ga_id = ga.ga_id 
								    WHERE par.ga_id = '"""+ str(game_id) +"""' AND par.present = 'true'
							  """)

	for player in players_actifs:
		ranking.append(player["pl_pseudo"])
		#money_info.append({ player["pl_pseudo"] : calculeMoneyInfo(player["pl_pseudo"], 1) })

	return ranking


def makeMapItem(pl_id):
	""" Permet de creer une donnee Json de type mapItem
		:param arg1: description
		:param arg2: description
		:type arg1: type
		:type arg1: type
		:return: description de la valeur de retour
		:rtype: type de la valeur de retour
	"""

	mapItem = []
	mapItem.append(makeMapItemStand(pl_id))
	pub_id = db.select("SELECT p.p_id FROM Pub p WHERE p.pl_id = "+ str(pl_id))

	if len(pub_id) != 0:
		for row in pub_id:
			mapItem.append(makeMapItemPub(row['pub_id']))

	return (mapItem)


def makeMapItemStand(pl_id):
	""" 
		:param arg1: description
		:param arg2: description
		:type arg1: type
		:type arg1: type
		:return: description de la valeur de retour
		:rtype: type de la valeur de retour
	"""

	coordinates = db.select("SELECT loc_longitude, loc_latitude FROM Stand  WHERE pl_id = '"+ str(pl_id) +"'")
	influence = db.select("SELECT loc_rayon FROM Stand WHERE pl_id = '"+ str(pl_id) +"'")[0]["loc_rayon"]
	pl_name = db.select("SELECT pl_pseudo FROM Player WHERE pl_id = '"+ str(pl_id) +"'")[0]["pl_pseudo"]

	return ({ "kind" : "stand", "owner" : pl_name, "location" : { "latitude" : coordinates[0]['loc_longitude'], "longitude" : coordinates[0]['loc_latitude']}, "influence" : influence })	

def makeMapItemPub(pub_id):
	""" 
		:param arg1: description
		:param arg2: description
		:type arg1: type
		:type arg1: type
		:return: description de la valeur de retour
		:rtype: type de la valeur de retour
	"""

	coordinates = db.select("SELECT p_coordx, p_coordy FROM Pub WHERE pub_id = '"+ str(pub_id) +"'")
	influence = db.select("SELECT p_rayon FROM Pub WHERE pub_id = '"+ str(pub_id) +"'")[0]["p_rayon"]
	pl_name = db.select("""	SELECT pl.pl_pseudo FROM Player pl 
							INNER JOIN Pub p ON pl.pl_id = p.pl_id 
							WHERE p.pub_id = '"""+ str(pub_id) +"""'""")[0]["pl_pseudo"]
	
	return ({ "kind" : "ad", "owner" : pl_name, "location" : { "latitude" : coordinates[0]['p_coordx'], "longitude" : coordinates[0]['p_coordy']}, "influence" : influence })	
	

def makePlayerInfo(pl_name):
	""" Permet de creer une donnee Json de type playerInfo
		:param arg1: description
		:param arg2: description
		:type arg1: type
		:type arg1: type
		:return: description de la valeur de retour
		:rtype: type de la valeur de retour
	"""

	info = calculeMoneyInfo(pl_name, 0)
	drinkInfo = makeDrinkOffered(pl_name)																																																																																																																																																																										

	return ({ "cash" : info['cash'], "profit" : info['profit'], "sales" : info['sales'], "drinksOffered" : drinkInfo })


def calculeMoneyInfo(player, status=0):
	""" Permet de calculer les info monetaires du joueur (son budget courant, ses ventes & son profit depuis le debut de la partie)
		variable nom du player, et 0 ou 1 : renvoit toutes les infos si 0, que le budget si 1
		:param arg1: description
		:param arg2: description
		:type arg1: type
		:type arg1: type
		:return: si status = 0 -> { "cash" : cash, "profit" : profit, "sales" : sales } sinon { "cash" : cash }
		:rtype: Json
	"""

	budget_ini = db.select("SELECT pl_budget_ini FROM Player WHERE pl_pseudo = '"+ player +"'")[0]["pl_budget_ini"]
	player_id = db.select("SELECT p.pl_id FROM Player p WHERE pl_pseudo = '"+ player +"'")[0]["pl_id"]

	earnings = calculeEarnings(player_id)
	spending = calculeSpend(player_id)
	sales = calculeSales(player_id)

	cash = budget_ini - spending + earnings
	profit = earnings - spending

	if status == 0:
		return ({ "cash" : cash, "profit" : profit, "sales" : sales })
	else: 
		return ({ "cash" : cash })
	
def makeDrinkEveryTime(pl_name):
	""" Permet de calculer et de renvoyer les "drinksOffered" d'un player
		:param arg1: description
		:param arg2: description
		:type arg1: type
		:type arg1: type
		:return: description de la valeur de retour
		:rtype: type de la valeur de retour
	"""

	drinkEveryTime = []

	# Boisson par defaut : la limonade
	drinkEveryTime.append(makeDrinkInfo(3))

	player_id = recupIdFromName(pl_name)
	drink_id = db.select("SELECT t.rec_id FROM Transaction t WHERE t.pl_id = '"+ str(player_id) +"'")

	#rec_nom = recupNameRecFromId(rec_id)	
		

	for drink in drink_id:	
		drinkInfo = makeDrinkInfo(drink["rec_id"])	
		drinkEveryTime.append(drinkInfo)


	return (drinkEveryTime)
	

def makeDrinkOffered(pl_name):
	""" Permet de calculer et de renvoyer les "drinksOffered" d'un player
		:param arg1: description
		:param arg2: description
		:type arg1: type
		:type arg1: type
		:return: description de la valeur de retour
		:rtype: type de la valeur de retour
	"""

	drinkOffered = []
	
	player_id = recupIdFromName(pl_name)
	da_max = getDayIdCurr()
	drink_id = db.select("SELECT t.rec_id FROM Transaction t WHERE t.pl_id = '"+ str(player_id) +"' AND t.da_id = '"+ str(da_max) +"'")
		
	for drink in drink_id:	
		drinkInfo = makeDrinkInfo(drink["rec_id"])	
		drinkOffered.append(drinkInfo)

	return (drinkOffered)
	

def makeDrinkInfo(rec_id):
	""" 
		:param arg1: description
		:param arg2: description
		:type arg1: type
		:type arg1: type
		:return: description de la valeur de retour
		:rtype: type de la valeur de retour
	"""

	price = calculePriceRec(rec_id)
	nom = db.select("SELECT rec_nom FROM Recipe WHERE rec_id = '"+ str(rec_id) +"'")[0]["rec_nom"]

	alcohol = hasAlcohol(rec_id)
	cold = isCold(rec_id)
	
	drinkInfo  = { "name" : nom, "price" : price,  "hasAlcohol" :alcohol, "isCold" : cold }
	
	return (drinkInfo)


def calculeEarnings(player_id):
	""" Permet de calculer les ventes globales (en euros) du joueur depuis le debut de la partie.
		:param arg1: description
		:param arg2: description
		:type arg1: type
		:type arg1: type
		:return: description de la valeur de retour
		:rtype: type de la valeur de retour
	"""

	sales = db.select("SELECT SUM(t.qte_sale * t.price) FROM Transaction t WHERE t.pl_id = '" + str(player_id) +"'")[0]["sum"]

	if sales == None:
		return 0
	else: 
		return sales


def calculeSales(player_id):
	""" Permet de calculer le nombre de recette vendu du joueur depuis le debut de la partie.
		:param arg1: description
		:param arg2: description
		:type arg1: type
		:type arg1: type
		:return: description de la valeur de retour
		:rtype: type de la valeur de retour
	"""

	sales = db.select("SELECT SUM(t.qte_sale) FROM Transaction t WHERE t.pl_id = '" + str(player_id) +"'")[0]["sum"]

	if sales == None:
		return 0
	else:
		return sales


def calculeSpend(player_id):
	""" Permet de calculer les depenses globales (en euros) du joueur depuis le debut de la partie.
		:param arg1: description
		:param arg2: description
		:type arg1: type
		:type arg1: type
		:return: description de la valeur de retour
		:rtype: type de la valeur de retour
	"""

	spending = db.select("""	SELECT SUM(t.qte_prev * 
									(SELECT SUM(i.ing_prix) FROM Ingredient i 
									INNER JOIN Contains c ON i.ing_id = c.ing_id 
									INNER JOIN Recipe r ON r.rec_id = c.rec_id 
									WHERE r.rec_id = t.rec_id) ) 
								FROM Transaction t 
								WHERE t.pl_id = '"""+ str(player_id) +"""'""")[0]["sum"]

	if spending == None:
		return 0
	else: 
		return spending


def calculePriceRec(rec_id):
	""" Permet de calculer le prix d'une recette
		:param arg1: description
		:param arg2: description
		:type arg1: type
		:type arg1: type
		:return: description de la valeur de retour
		:rtype: type de la valeur de retour
	"""

	price_rec = db.select("""	SELECT SUM(i.ing_prix) FROM Ingredient i 
								INNER JOIN Contains c ON i.ing_id = c.ing_id 
								INNER JOIN Recipe r ON r.rec_id = c.rec_id 
								WHERE r.rec_id	 = '"""+ str(rec_id) +"""'""")[0]['sum']

	return price_rec


def makeJsonResponse(data,status=200):
	""" Permet de convert une liste en JSON et ajouter le code de retour.
		:param arg1: description
		:param arg2: description
		:type arg1: type
		:type arg1: type
		:return: description de la valeur de retour
		:rtype: type de la valeur de retour
	"""

	return json.dumps(data), status, {'Content-Type': 'application/json'}
