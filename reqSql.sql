-- Quels ingrédients composent le Mojito ?

SELECT r.rec_nom FROM Recipe r
INNER JOIN Contains c_Mojito ON c_Mojito.rec_id = r.rec_id
INNER JOIN Ingredient i_mojito ON i_mojito.ing_id = c_Mojito.ing_id
WHERE r.rec_nom = 'Mojito'; 

