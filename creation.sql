------------------------------------------------------------
--        Script MySQL.
------------------------------------------------------------


------------------------------------------------------------
-- Table: Player
------------------------------------------------------------

CREATE TABLE Player(
        pl_pseudo     Varchar (255) NOT NULL ,
        pl_password   Varchar (255) NOT NULL ,
        pl_id         SERIAL NOT NULL ,
        pl_mail       Varchar (255) ,
        pl_date       Date ,
        pl_budget_ini Float NOT NULL ,
        PRIMARY KEY (pl_id )
);


------------------------------------------------------------
-- Table: Ingrédient
------------------------------------------------------------

CREATE TABLE Ingredient(
        ing_id      SERIAL NOT NULL ,
        ing_nom     Varchar (255) ,
        ing_prix    DECIMAL (15,3)  ,
        ing_alcohol Int ,
        ing_cold    Int ,
        PRIMARY KEY (ing_id )
);


------------------------------------------------------------
-- Table: Recipe
------------------------------------------------------------

CREATE TABLE Recipe(
        rec_id      SERIAL NOT NULL ,
        rec_nom     Varchar (255) NOT NULL ,
        rec_alcohol Int ,
        rec_cold    Int ,
        PRIMARY KEY (rec_id )
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
        ga_run      Bool ,
        PRIMARY KEY (ga_id )
);


------------------------------------------------------------
-- Table: Stand
------------------------------------------------------------

CREATE TABLE Stand(
        loc_coordX Float ,
        loc_id     SERIAL NOT NULL ,
        loc_coordY Float NOT NULL ,
        loc_rayon  Float NOT NULL ,
        pl_id      Int NOT NULL ,
        PRIMARY KEY (loc_id )
);


------------------------------------------------------------
-- Table: Pub
------------------------------------------------------------

CREATE TABLE Pub(
        p_id     SERIAL NOT NULL ,
        p_coordX Float NOT NULL ,
        p_coordY Float NOT NULL ,
        p_rayon  Float NOT NULL ,
        pl_id    Int NOT NULL ,
        PRIMARY KEY (p_id )
);


------------------------------------------------------------
-- Table: Contains
------------------------------------------------------------

CREATE TABLE Contains(
        ing_id Int NOT NULL ,
        rec_id Int NOT NULL ,
        PRIMARY KEY (ing_id ,rec_id )
);


------------------------------------------------------------
-- Table: Participe
------------------------------------------------------------

CREATE TABLE Participate(
        present Bool NOT NULL ,
        ga_id   Int NOT NULL ,
        pl_id   Int NOT NULL ,
        PRIMARY KEY (ga_id ,pl_id )
);


------------------------------------------------------------
-- Table: Transaction
------------------------------------------------------------

CREATE TABLE Transaction(
        qte_prev Int ,
        qte_sale Int ,
        price    Float ,
        day      Int NOT NULL ,
        pl_id    Int NOT NULL ,
        rec_id   Int NOT NULL ,
        PRIMARY KEY (pl_id ,rec_id )
);

ALTER TABLE Stand ADD CONSTRAINT FK_Stand_pl_id FOREIGN KEY (pl_id) REFERENCES Player(pl_id);
ALTER TABLE Pub ADD CONSTRAINT FK_Pub_pl_id FOREIGN KEY (pl_id) REFERENCES Player(pl_id);
ALTER TABLE Contains ADD CONSTRAINT FK_Contains_ing_id FOREIGN KEY (ing_id) REFERENCES Ingredient(ing_id);
ALTER TABLE Contains ADD CONSTRAINT FK_Contains_rec_id FOREIGN KEY (rec_id) REFERENCES Recipe(rec_id);
ALTER TABLE Participate ADD CONSTRAINT FK_Participe_ga_id FOREIGN KEY (ga_id) REFERENCES Game(ga_id);
ALTER TABLE Participate ADD CONSTRAINT FK_Participe_pl_id FOREIGN KEY (pl_id) REFERENCES Player(pl_id);
ALTER TABLE Transaction ADD CONSTRAINT FK_Transaction_pl_id FOREIGN KEY (pl_id) REFERENCES Player(pl_id);
ALTER TABLE Transaction ADD CONSTRAINT FK_Transaction_rec_id FOREIGN KEY (rec_id) REFERENCES Recipe(rec_id);

