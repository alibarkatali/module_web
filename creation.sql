--------------------------------------------------------------
--        Script SQL
------------------------------------------------------------


------------------------------------------------------------
-- Table: Player
------------------------------------------------------------

CREATE TABLE Player(
        pl_pseudo   Varchar (255) NOT NULL ,
        pl_password Varchar (255) ,
        pl_id       SERIAL NOT NULL,
        pl_mail     Varchar (255) ,
        pl_date     Date ,
        PRIMARY KEY (pl_id)
);

------------------------------------------------------------
-- Table: Player
------------------------------------------------------------
CREATE TABLE Participe(
		pa_present BOOL NOT NULL
        ga_id Int NOT NULL
		pl_id Int NOT NULL
		PRIMARY KEY (pl_id, ga_id)
);
			

------------------------------------------------------------
-- Table: Ingredient
------------------------------------------------------------

CREATE TABLE Ingredient(
        ing_id      SERIAL NOT NULL ,
        ing_nom     Varchar (255) ,
        ing_prix    Float ,
        ing_alcohol Int ,
        ing_cold    Int ,
        PRIMARY KEY (ing_id)
);


------------------------------------------------------------
-- Table: Recipe
------------------------------------------------------------

CREATE TABLE Recipe(
        rec_id      SERIAL NOT NULL ,
        rec_nom     Varchar (255) NOT NULL ,
        rec_alcohol Int ,
        rec_cold    Int ,
        PRIMARY KEY (rec_id)
);


------------------------------------------------------------
-- Table: Game
------------------------------------------------------------

CREATE TABLE Game(
        ga_id       SERIAL NOT NULL ,
        ga_nom      Varchar (255) NOT NULL ,
        ga_centreX  Float NOT NULL ,
        ga_centreY  Float NOT NULL ,
        ga_largeur  Float NOT NULL ,
        ga_longueur Float NOT NULL ,
		ga_run      BOOL NOT NULL,
        PRIMARY KEY (ga_id)
);


------------------------------------------------------------
-- Table: Stand
------------------------------------------------------------

CREATE TABLE Stand(
        loc_coordX Float ,
        loc_id     SERIAL NOT NULL ,
        loc_coordY Float NOT NULL ,
        loc_rayon  Float NOT NULL ,
        pl_id       Int NOT NULL ,
        PRIMARY KEY (loc_id)
);


------------------------------------------------------------
-- Table: Pub
------------------------------------------------------------

CREATE TABLE Pub(
        p_id        SERIAL NOT NULL ,
        p_coordX    Float NOT NULL ,
        p_coordY    Float NOT NULL ,
        p_rayon     Float NOT NULL ,
        pl_id Int NOT NULL ,
        PRIMARY KEY (p_id)
);


------------------------------------------------------------
-- Table: Achete
------------------------------------------------------------

CREATE TABLE Buy(
        quantite Int ,
        pl_id    Int NOT NULL ,
        rec_id   Int NOT NULL ,
        PRIMARY KEY (pl_id, rec_id)
);


------------------------------------------------------------
-- Table: Produit
------------------------------------------------------------

CREATE TABLE Make(
        nombre Int ,
        prix   Float NOT NULL ,
        vendu  Int ,
        rec_id Int NOT NULL ,
        pl_id   Int NOT NULL ,
        PRIMARY KEY (rec_id, pl_id )
);


------------------------------------------------------------
-- Table: Contains
------------------------------------------------------------

CREATE TABLE Contains(
        ing_id Int NOT NULL ,
        rec_id Int NOT NULL ,
        PRIMARY KEY (Ing_id, rec_id )
);

ALTER TABLE Stand ADD CONSTRAINT FK_Stand_pl_id FOREIGN KEY (pl_id) REFERENCES Player(pl_id);
ALTER TABLE Pub ADD CONSTRAINT FK_Pub_pl_id FOREIGN KEY (pl_id) REFERENCES Player(pl_id);
ALTER TABLE Buy ADD CONSTRAINT FK_Buy_pl_id FOREIGN KEY (pl_id) REFERENCES Player(pl_id);
ALTER TABLE Buy ADD CONSTRAINT FK_Buy_rec_id FOREIGN KEY (rec_id) REFERENCES Recipe(rec_id);
ALTER TABLE Make ADD CONSTRAINT FK_Make_rec_id FOREIGN KEY (rec_id) REFERENCES Recipe(rec_id);
ALTER TABLE Make ADD CONSTRAINT FK_Make_pl_id FOREIGN KEY (pl_id) REFERENCES Player(pl_id);
ALTER TABLE Contains ADD CONSTRAINT FK_Contains_ing_id FOREIGN KEY (ing_id) REFERENCES Ingredient(ing_id);
ALTER TABLE Contains ADD CONSTRAINT FK_Contains_rec_id FOREIGN KEY (rec_id) REFERENCES Recipe(rec_id);
ALTER TABLE Participe ADD CONSTRAINT FK_Participe_ga_id FOREIGN KEY (ga_id) REFERENCES Game(ga_id);
ALTER TABLE Participe ADD CONSTRAINT FK_Participe_pl_id FOREIGN KEY (pl_id) REFERENCES Player(pl_id);
