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

-- Afficher la liste des joueurs 
SELECT pl.* FROM Player pl
INNER JOIN Participe pa ON pa.pl_id = pl.pl_id
INNER JOIN Game ga ON ga.ga_id = pa.ga_id
WHERE ga.ga_run = true AND pa.pa_present = true; 

-- Inscrire un player s'il n'existe pas

-- Regarder si le pseudo est déjà prit
SELECT pl_pseudo FROM Player;

-- Regarder si l'email est déjà prit 
SELECT pl_mail FROM Player;

-- Insérer le pseudo, le mail et la date
INSERT INTO Player(pl_pseudo, pl_mail, pl_date) VALUES ('PSEUDO', 'MAIL', 'DATE');

-- Insérer juste le pseudo 
INSERT INTO Player(pl_pseudo) VALUES ('PSEUDO'); 

-- Créer un stand à son inscription, après avoir récupérer l'id du joueur que nous venons de créer
INSERT INTO Stand(loc_coordX, loc_coordY, loc_rayon, pl_id) VALUES ('ALEA', 'ALEA', 'RAYON', 'ID'); 




