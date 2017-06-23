INSERT INTO ingredient(ing_nom, ing_prix, ing_cold, ing_alcohol) VALUES ('Eau Gazeuse', '0.5', '1', '0');
INSERT INTO ingredient(ing_nom, ing_prix, ing_cold, ing_alcohol) VALUES ('Sucre', '0.25', '2', '2');
INSERT INTO ingredient(ing_nom, ing_prix, ing_cold, ing_alcohol) VALUES ('Menthe', '1', '2', '0');
INSERT INTO ingredient(ing_nom, ing_prix, ing_cold, ing_alcohol) VALUES ('Citron', '0.75', '2', '0');
INSERT INTO ingredient(ing_nom, ing_prix, ing_cold, ing_alcohol) VALUES ('Rhum', '4', '1', '1');
INSERT INTO ingredient(ing_nom, ing_prix, ing_cold, ing_alcohol) VALUES ('Café Moulue', '1.25', '2', '2');
INSERT INTO ingredient(ing_nom, ing_prix, ing_cold, ing_alcohol) VALUES ('Eau', '2', '1', '0');
INSERT INTO ingredient(ing_nom, ing_prix, ing_cold, ing_alcohol) VALUES ('Sirop de Grenadine', '1', '1', '0');
INSERT INTO ingredient(ing_nom, ing_prix, ing_cold, ing_alcohol) VALUES ('Sirop de Menthe', '1', '1', '0');
INSERT INTO ingredient(ing_nom, ing_prix, ing_cold, ing_alcohol) VALUES ('Sucre de Canne', '0.25', '1', '0');

INSERT INTO recipe(rec_nom, rec_cold, rec_alcohol) VALUES ('Mojito', '1', '1');
INSERT INTO recipe(rec_nom, rec_cold, rec_alcohol) VALUES ('Eau', '1', '0');
INSERT INTO recipe(rec_nom, rec_cold, rec_alcohol) VALUES ('Limonade', '1', '0');
INSERT INTO recipe(rec_nom, rec_cold, rec_alcohol) VALUES ('Diabolo Menthe', '1', '0');
INSERT INTO recipe(rec_nom, rec_cold, rec_alcohol) VALUES ('Diabolo Grenadine', '1', '0');
INSERT INTO recipe(rec_nom, rec_cold, rec_alcohol) VALUES ('Café avec sucre', '0', '0');
INSERT INTO recipe(rec_nom, rec_cold, rec_alcohol) VALUES ('Café sans sucre', '0', '0');

INSERT INTO contains(ing_id, rec_id) VALUES ('1', '1');
INSERT INTO contains(ing_id, rec_id) VALUES ('2', '1');
INSERT INTO contains(ing_id, rec_id) VALUES ('3', '1');
INSERT INTO contains(ing_id, rec_id) VALUES ('5', '1');
INSERT INTO contains(ing_id, rec_id) VALUES ('10', '1');
INSERT INTO contains(ing_id, rec_id) VALUES ('7', '2');
INSERT INTO contains(ing_id, rec_id) VALUES ('1', '3');
INSERT INTO contains(ing_id, rec_id) VALUES ('2', '3');
INSERT INTO contains(ing_id, rec_id) VALUES ('1', '4');
INSERT INTO contains(ing_id, rec_id) VALUES ('9', '4');
INSERT INTO contains(ing_id, rec_id) VALUES ('1', '5');
INSERT INTO contains(ing_id, rec_id) VALUES ('8', '5');
INSERT INTO contains(ing_id, rec_id) VALUES ('2', '6');
INSERT INTO contains(ing_id, rec_id) VALUES ('6', '6');
INSERT INTO contains(ing_id, rec_id) VALUES ('7', '6');
INSERT INTO contains(ing_id, rec_id) VALUES ('6', '7');
INSERT INTO contains(ing_id, rec_id) VALUES ('7', '7');

