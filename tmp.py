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

meteos = {"timestamp" : 0,"weather" : [{"dfn" : 0,"weather" : "RAINNY"},{"dfn" : 1, "weather" : "CLOUDY"}]}

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