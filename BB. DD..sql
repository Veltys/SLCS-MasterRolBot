BEGIN TRANSACTION;
DROP TABLE IF EXISTS "Usuarios";
CREATE TABLE IF NOT EXISTS "Usuarios" (
	"Id"	INTEGER NOT NULL UNIQUE,
	"Estado"	INTEGER NOT NULL DEFAULT 0,
	PRIMARY KEY("Id"),
	FOREIGN KEY("Estado") REFERENCES "Estados"("Id")
);
DROP TABLE IF EXISTS "Estados";
CREATE TABLE IF NOT EXISTS "Estados" (
	"Id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"Juego"	INTEGER NOT NULL,
	"Nombre"	TEXT NOT NULL,
	"Descripción"	TEXT NOT NULL,
	FOREIGN KEY("Juego") REFERENCES "Juegos"("Id")
);
DROP TABLE IF EXISTS "Juegos";
CREATE TABLE IF NOT EXISTS "Juegos" (
	"Id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"Nombre"	TEXT
);
DROP TABLE IF EXISTS "Opciones";
CREATE TABLE IF NOT EXISTS "Opciones" (
	"Id"	INTEGER NOT NULL,
	"Estado"	INTEGER NOT NULL,
	"Siguiente"	INTEGER NOT NULL,
	PRIMARY KEY("Id"),
	FOREIGN KEY("Estado") REFERENCES "Estados"("Id"),
	FOREIGN KEY("Siguiente") REFERENCES "Estados"("Id")
);
INSERT INTO "Estados" VALUES (0,0,'Sin juego elegido','Estado "especial" que aglutina a los usuarios que no han elegido ningún juego');
INSERT INTO "Estados" VALUES (1,1,'¡Bienvenido!','Nuestro superhéroe favorito ha sido secuestrado por un villano desconocido. Por si eso no fuera suficiente, el equipo de héroes que estaba dedicado a buscarle, los Huérfanos Electrónicos... ¡tampoco aparecen!

¡¡ES TU MOMENTO DE ENTRAR EN ACCIÓN!!');
INSERT INTO "Estados" VALUES (2,1,'Investigas la base secreta','La puerta está cerrada, vas a tener que buscar la manera de entrar.');
INSERT INTO "Estados" VALUES (3,1,'Investigas la casa de Cálico Jack','Llamas al timbre de la casa y... ¡es la madre de Cálico! Te ofrece unos _boquerones en su tinta_, un _bocaillo shope_, un _bocata foigrá_ y unas _cocretas_. ¿Qué elegirás?');
INSERT INTO "Estados" VALUES (4,1,'Investigas Electrónica web','Nada, que no se abre la puerta. ¿Eso es un felpudo con la cara de Muzaman?');
INSERT INTO "Estados" VALUES (5,1,'Visita _ar chacho Migué_','¿Investigar? ¡Eso es para déblies! Vamos a visitar _ar chacho Migué_, que seguro que sabe algo o al menos nos venderá algún arma.');
INSERT INTO "Estados" VALUES (100,1,'¡Bienvenido!','¡Fabuloso enunciado sin tema!

¡¡Resuelve este maravilloso misterio!!');
INSERT INTO "Estados" VALUES (101,1,'Título 1','Opción 1');
INSERT INTO "Estados" VALUES (102,1,'Título 2','Opción 2');
INSERT INTO "Estados" VALUES (103,1,'Título 3','Opción 3');
INSERT INTO "Estados" VALUES (104,1,'Título 4','Opción 4');
INSERT INTO "Estados" VALUES (105,1,'Título 5','Opción 5');
INSERT INTO "Estados" VALUES (106,1,'Título 6','Opción 6');
INSERT INTO "Estados" VALUES (107,1,'Título 7','Opción 7');
INSERT INTO "Estados" VALUES (108,1,'Título 8','Opción 8');
INSERT INTO "Estados" VALUES (109,1,'Título 9','Opción 9');
INSERT INTO "Estados" VALUES (110,1,'Título 10','Opción 10');
INSERT INTO "Estados" VALUES (111,1,'Título 11','Opción 11');
INSERT INTO "Estados" VALUES (112,1,'Título 12','Opción 12');
INSERT INTO "Estados" VALUES (113,1,'Título 13','Opción 13');
INSERT INTO "Estados" VALUES (114,1,'Título 14','Opción 14');
INSERT INTO "Estados" VALUES (115,1,'Título 15','Opción 15');
INSERT INTO "Juegos" VALUES (0,'Sin juego elegido');
INSERT INTO "Juegos" VALUES (1,'El rol de Cálico Electrónico');
INSERT INTO "Juegos" VALUES (2,'Juego de rol de prueba');
INSERT INTO "Opciones" VALUES (1,1,2);
INSERT INTO "Opciones" VALUES (2,1,3);
INSERT INTO "Opciones" VALUES (3,1,4);
INSERT INTO "Opciones" VALUES (4,1,5);
INSERT INTO "Opciones" VALUES (101,101,102);
INSERT INTO "Opciones" VALUES (102,101,103);
INSERT INTO "Opciones" VALUES (103,101,104);
INSERT INTO "Opciones" VALUES (104,101,105);
INSERT INTO "Opciones" VALUES (105,102,103);
INSERT INTO "Opciones" VALUES (106,102,104);
INSERT INTO "Opciones" VALUES (107,102,105);
INSERT INTO "Opciones" VALUES (108,102,106);
INSERT INTO "Opciones" VALUES (109,103,104);
INSERT INTO "Opciones" VALUES (110,103,105);
INSERT INTO "Opciones" VALUES (111,103,106);
INSERT INTO "Opciones" VALUES (112,103,107);
INSERT INTO "Opciones" VALUES (113,104,102);
INSERT INTO "Opciones" VALUES (114,104,103);
INSERT INTO "Opciones" VALUES (115,104,105);
INSERT INTO "Opciones" VALUES (116,104,106);
INSERT INTO "Opciones" VALUES (117,105,101);
INSERT INTO "Opciones" VALUES (118,105,102);
INSERT INTO "Opciones" VALUES (119,105,103);
INSERT INTO "Opciones" VALUES (120,105,104);
INSERT INTO "Opciones" VALUES (121,106,104);
INSERT INTO "Opciones" VALUES (122,106,108);
INSERT INTO "Opciones" VALUES (123,106,110);
INSERT INTO "Opciones" VALUES (124,106,111);
INSERT INTO "Opciones" VALUES (125,107,111);
INSERT INTO "Opciones" VALUES (126,107,112);
INSERT INTO "Opciones" VALUES (127,107,113);
INSERT INTO "Opciones" VALUES (128,107,114);
INSERT INTO "Opciones" VALUES (129,108,104);
INSERT INTO "Opciones" VALUES (130,108,105);
INSERT INTO "Opciones" VALUES (131,108,106);
INSERT INTO "Opciones" VALUES (132,108,109);
INSERT INTO "Opciones" VALUES (133,109,103);
INSERT INTO "Opciones" VALUES (134,109,106);
INSERT INTO "Opciones" VALUES (135,109,110);
INSERT INTO "Opciones" VALUES (136,109,111);
INSERT INTO "Opciones" VALUES (137,110,103);
INSERT INTO "Opciones" VALUES (138,110,105);
INSERT INTO "Opciones" VALUES (139,110,108);
INSERT INTO "Opciones" VALUES (140,110,115);
INSERT INTO "Opciones" VALUES (141,111,103);
INSERT INTO "Opciones" VALUES (142,111,107);
INSERT INTO "Opciones" VALUES (143,111,108);
INSERT INTO "Opciones" VALUES (144,111,109);
INSERT INTO "Opciones" VALUES (145,112,101);
INSERT INTO "Opciones" VALUES (146,112,102);
INSERT INTO "Opciones" VALUES (147,112,107);
INSERT INTO "Opciones" VALUES (148,112,108);
COMMIT;
