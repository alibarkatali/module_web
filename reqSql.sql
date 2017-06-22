-- Quels ingrédients composent le Mojito ?

SELECT i_mojito.ing_nom FROM Ingredient i_mojito
INNER JOIN Contains c_mojito ON i_mojito.ing_id = c_mojito.ing_id
INNER JOIN Recipe r_mojito ON r_mojito.rec_id = c_mojito.rec_id
WHERE r_mojito.rec_nom = 'Mojito'; 

-- Quels est le prix du Mojito?

SELECT SUM(i_mojito.ing_prix) FROM Ingredient i_mojito
INNER JOIN Contains c_mojito ON i_mojito.ing_id = c_mojito.ing_id
INNER JOIN Recipe r_mojito ON r_mojito.rec_id = c_mojito.rec_id
WHERE r_mojito.rec_nom = 'Mojito'; 

-- Liste des recettes
SELECT * FROM Recipe ORDER BY rec_nom;

-- Afficher détail d'une recette à partir de son nom
SELECT * FROM Recipe WHERE rec_nom = 'Mojito' ORDER BY rec_nom;

-- Liste des Ingredients 
SELECT * FROM Ingredient ORDER BY ing_nom;

-- Afficher détail d'un ingrédient à partir de son nom
SELECT * FROM Ingredient WHERE ing_nom = 'Sucre' ORDER BY ing_nom;



