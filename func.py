import json
import random
from db import Db

# VARIABLES GLOBALES
db = Db()
gaNom = [ "Shaddock", "Bashunga", "VaChier", "GitansLand", "Iphone", "Pizza" ]

def creerGame():
	""" Creer une nouvelle partie. """ 
	gameNom = random.choice(gaNom)
	db.execute("INSERT INTO Game(ga_nom, ga_latitude, ga_longitude, ga_centrex, ga_centrey, ga_run) VALUES ('"+ gameNom +"', '500', '700', '350', '250', 'true')")

def supprimerGame(game_id):
	""" Permet de supprimer une partie
		On passe son ga_run a false puis on met les participants a false
		:param arg1: id du game a tester
		:type arg1: int
	"""
		
	db.execute("UPDATE Game SET ga_run = 'false' WHERE ga_id = '"+ game_id +"'")
	db.execute("UPDATE Participate SET present = 'false' WHERE ga_id = '"+ game_id +"'")

def isCold(rec_id):
	""" Permet de tester si une recette (boisson) est froid ou chaude
		:param arg1: id de la recette
		:type arg1: int
		:return: return true ou false
		:rtype: boolean
	"""
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
	""" Permet de tester si une recette (boisson) est alcolisee
		:param arg1: id de la recette
		:type arg1: int
		:return: return true ou false
		:rtype: boolean
	"""
	
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
	""" Recupere l'id d'une recette a partir de son nom """
	recId = db.select("SELECT rec_id FROM Recipe WHERE rec_nom = '"+ rec_name +"'")[0]["rec_id"]
	return recId

def recupNameRecFromId(rec_id):
	""" Recupere le nom d'une recette a partir de son id """
	recName = db.select("SELECT rec_nom From Recipe WHERE rec_id = '"+ str(rec_id) +"'")[0]["rec_nom"]	
	return recName

def getDayCurr():
	""" Recupere la valeur du jour courant """
	daMax = db.select("SELECT MAX(da_id) From Date")[0]["max"]
	dayCurr = db.select("SELECT da_day From Date WHERE da_id = '"+ daMax +"'")[0]["da_day"]
	return dayCurr

def getDayIdCurr():	
	""" Recupere l'id du jour courant """
	daMax = db.select("SELECT MAX(da_id) From Date")[0]["max"]
	return daMax

def recupIdFromName(pl_name):
	""" Recupere l'id d'un player en fonction du nom """
	plId = db.select("SELECT pl_id FROM Player WHERE pl_pseudo = '"+ pl_name +"'")[0]["pl_id"]
	return plId

def recupNameFromId(pl_id):
	""" Recupere le nom d'un player en fonction de l'id """
	plName = db.select("SELECT pl_pseudo FROM Player WHERE pl_id = '"+ str(pl_id) +"'")[0]["pl_pseudo"]
	return plName

def recupGameId():
	""" Recupere l'id du jeu en cours (lorsqu'une seule partie est lancee) """
	gameId = db.select("SELECT ga_id FROM Game WHERE ga_run = 'true'")[0]["ga_id"]
	return gameId

def getAvailableIngredients(pl_name):
	"""" Recupere les ingredients des recettes proposees (decouvertes) pour le player pl_name 
		 :rtype: collection d'objet Json ingredients	
	"""

	aIng = []
	plId = recupIdFromName(pl_name)

	listIngredientId = db.select(""" SELECT ing.ing_id FROM Ingredient ing 
				  INNER JOIN Contains con ON con.ing_id = ing.ing_id 
				  INNER JOIN Recipe rec ON con.rec_id = rec.rec_id 
				  INNER JOIN Transaction tr ON tr.rec_id = rec.rec_id 
				  WHERE tr.pl_id = '"""+ str(plId) +"""'
			 """)
	
	for rows in listIngredientId:
		aIng.append(makeIngredientInfo(rows['ing_id']))

	return aIng	

def makeIngredientInfo(ing_id):
	""" Recupere les info de l'ingredient passe en argument
		:return: donnee Json comportant les informations de l'ingredient
		:rtype: JSON
	"""

	info = db.select("SELECT ing_nom, ing_prix, ing_alcohol, ing_cold FROM Ingredient WHERE ing_id = '"+ str(ing_id) +"'")
	return ({ "name" : info['ing_nom'], "cost" : info['ing_prix'], "hasAlcohol" : info['ing_alcohol'], "isCold" : info['ing_cold'] }) 

def makeRegion(game_id):
	""" Recupere les infos concernant la taille ainsi que le centre de la map de la partie courante
		:param arg1: id du game a tester
		:type arg1: int
		:return: donne comportant le centre (x et y), ainsi que le span (latitude et longitude) de la partie voulue
		:rtype: Json
	"""

	coord = db.select("SELECT ga_centrex, ga_centrey FROM Game WHERE ga_id = '"+ str(game_id) +"' AND ga_run = 'true'")
	span = db.select("SELECT ga_latitude, ga_longitude FROM Game WHERE ga_id = '"+ str(game_id) +"' AND ga_run = 'true'")

	return ({ "center" : { "longitude" : coord[0]["ga_centrex"], "latitude" : coord[0]["ga_centrey"] }, "span" : { "latitudeSpan" : span[0]["ga_latitude"], "longitudeSpan" : span[0]["ga_longitude"] } })


def rankingPlayer(game_id):
	""" Permet de classer les joueurs, en fonction de leur budget (le plus riche est premier)
		:param arg1: id du game en question
		:type arg1: int
		:return: retourne une liste avec les noms des players dans l'ordre classes
		:rtype: Array
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
	""" Recupere les items d'un player sur la map (stand ou pub). Utilise les fonctions makeMapItemStand et Pub.
		:param arg1: id du joueur
		:type arg1: int
		:return: collection des objets appartenant au joueur, avec leur position
		:rtype: Collection d'objets Json
	"""

	mapItem = []
	mapItem.append(makeMapItemStand(pl_id))
	pub_id = db.select("SELECT p.p_id FROM Pub p WHERE p.pl_id = "+ str(pl_id))

	if len(pub_id) != 0:
		for row in pub_id:
			mapItem.append(makeMapItemPub(row['pub_id']))

	return (mapItem)


def makeMapItemStand(pl_id):
	""" Recupere les infos sur le stand du joueur (coordonnee, influence)
		:param arg1: id du joueur
		:type arg1: int
		:return: retour infos du stand possede par la joueur
		:rtype: Json
	"""

	coordinates = db.select("SELECT loc_longitude, loc_latitude FROM Stand  WHERE pl_id = '"+ str(pl_id) +"'")
	influence = db.select("SELECT loc_rayon FROM Stand WHERE pl_id = '"+ str(pl_id) +"'")[0]["loc_rayon"]
	pl_name = recupNameFromId(pl_id)

	return ({ "kind" : "stand", "owner" : pl_name, "location" : { "latitude" : coordinates[0]['loc_longitude'], "longitude" : coordinates[0]['loc_latitude']}, "influence" : influence })	

def makeMapItemPub(pub_id):
	""" Recupere les infos sur les pubs du joueur (coordonnee, influence)
		:param arg1: id du joueur
		:type arg1: int
		:return: retour infos des pubs possedees par le joueur
		:rtype: Json
	"""

	coordinates = db.select("SELECT p_coordx, p_coordy FROM Pub WHERE pub_id = '"+ str(pub_id) +"'")
	influence = db.select("SELECT p_rayon FROM Pub WHERE pub_id = '"+ str(pub_id) +"'")[0]["p_rayon"]
	pl_name = db.select("""	SELECT pl.pl_pseudo FROM Player pl 
							INNER JOIN Pub p ON pl.pl_id = p.pl_id 
							WHERE p.pub_id = '"""+ str(pub_id) +"""'""")[0]["pl_pseudo"]

	return ({ "kind" : "ad", "owner" : pl_name, "location" : { "latitude" : coordinates[0]['p_coordx'], "longitude" : coordinates[0]['p_coordy']}, "influence" : influence })	


def makePlayerInfo(pl_name):
	""" Recupere toutes les infos d'un player
		:param arg1: nom du joueur
		:type arg1: chaine de caracteres
		:return: infos du player : budget, profit & ventes (depuis le debut de la partie), boissons a vendre ce jour
		:rtype: Json
	"""

	info = calculeMoneyInfo(pl_name, 0)
	drinkInfo = makeDrinkOffered(pl_name)

	return ({ "cash" : info['cash'], "profit" : info['profit'], "sales" : info['sales'], "drinksOffered" : drinkInfo })


def calculeMoneyInfo(player_name, status=0):
	""" Permet de calculer les info monetaires du joueur (son budget courant, ses ventes & son profit depuis le debut de la partie)
		:param arg1: nom du joueur
		:param arg2: si a 1, calcule que le budget, si a 0, calcule en plus le profit et les ventes (defaut)
		:type arg1: chaine de caracteres
		:type arg1: int
		:return: si status = 0 -> { "cash" : cash, "profit" : profit, "sales" : sales } sinon { "cash" : cash }
		:rtype: Json
	"""

	budget_ini = db.select("SELECT pl_budget_ini FROM Player WHERE pl_pseudo = '"+ player_name +"'")[0]["pl_budget_ini"]
	player_id = recupIdFromName(player_name)

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
	""" Permet de calculer et de renvoyer les boissons POUVANT etre propose par le player
		:param arg1: nom du player
		:type arg1: chaine de caracteres
		:return: collection des infos de chaque boissons 
		:rtype: Collection d'objets Json
	"""

	drinkEveryTime = []

	# Boisson par defaut : la limonade
	drinkEveryTime.append(makeDrinkInfo(3))

	player_id = recupIdFromName(pl_name)
	drink_id = db.select("SELECT t.rec_id FROM Transaction t WHERE t.pl_id = '"+ str(player_id) +"'")
		

	for drink in drink_id:	
		drinkEveryTime.append(makeDrinkInfo(drink["rec_id"]))	

	return (drinkEveryTime)
	

def makeDrinkOffered(pl_name):
	""" Permet de calculer et de renvoyer les "drinksOffered" d'un player
		:param arg1: nom du joueur
		:type arg1: chaine de caracteres
		:return: Collection des boissons mises en ventes par le joueur le jour courant
		:rtype: Collection d'objets Json
	"""

	drinkOffered = []
	
	player_id = recupIdFromName(pl_name)
	da_max = getDayIdCurr()
	drink_id = db.select("SELECT t.rec_id FROM Transaction t WHERE t.pl_id = '"+ str(player_id) +"' AND t.da_id = '"+ str(da_max) +"'")
		
	for drink in drink_id:	
		drinkOffered.append(makeDrinkInfo(drink["rec_id"]))

	return (drinkOffered)
	

def makeDrinkInfo(rec_id):
	""" Permet de dresser les infos de la boissons passees en argument
		:param arg1: id de la boissons (recette)
		:type arg1: int
		:return: le nom, prix et les informations utiles (alcool, chaud ou froid) de la boissons
		:rtype: Json
	"""

	price = calculePriceRec(rec_id)
	nom = recupNameRecFromId(rec_id)

	alcohol = hasAlcohol(rec_id)
	cold = isCold(rec_id)
	
	drinkInfo  = { "name" : nom, "price" : price,  "hasAlcohol" :alcohol, "isCold" : cold }
	
	return (drinkInfo)


def calculeEarnings(player_id):
	""" Permet de calculer les ventes globales (en euros) du joueur depuis le debut de la partie.
		:param arg1: id du player
		:type arg1: int
		:return: total de l'argent gagne par les ventes
		:rtype: float
	"""

	sales = db.select("SELECT SUM(t.qte_sale * t.price) FROM Transaction t WHERE t.pl_id = '" + str(player_id) +"'")[0]["sum"]

	if sales == None:
		return 0
	else: 
		return sales


def calculeSales(player_id):
	""" Permet de calculer le nombre de recette vendu du joueur depuis le debut de la partie.
		:param arg1: id du joueur
		:type arg1: int
		:return: nombre total de recettes vendues
		:rtype: float
	"""

	sales = db.select("SELECT SUM(t.qte_sale) FROM Transaction t WHERE t.pl_id = '" + str(player_id) +"'")[0]["sum"]

	if sales == None:
		return 0
	else:
		return sales


def calculeSpend(player_id):
	""" Permet de calculer les depenses globales (en euros) du joueur depuis le debut de la partie.
		:param arg1: id du joueur
		:type arg1: int
		:return: depenses globales depuis le debut de la partie (sans la pub pour l'instant)
		:rtype: float
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
		:param arg1: id de la recette
		:type arg1: int
		:return: prix de la recette
		:rtype: float
	"""

	price_rec = db.select("""	SELECT SUM(i.ing_prix) FROM Ingredient i 
								INNER JOIN Contains c ON i.ing_id = c.ing_id 
								INNER JOIN Recipe r ON r.rec_id = c.rec_id 
								WHERE r.rec_id	 = '"""+ str(rec_id) +"""'""")[0]['sum']

	return price_rec


def makeJsonResponse(data,status=200):
	""" Permet de convert une liste en JSON et ajouter le code de retour.
		:param arg1: donnee
		:param arg2: status de la reponse http voulue
		:type arg1: - 
		:type arg1: int
		:return: http response
		:rtype: http response
	"""

	return json.dumps(data), status, {'Content-Type': 'application/json'}
