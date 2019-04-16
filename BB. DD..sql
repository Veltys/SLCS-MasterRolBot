BEGIN TRANSACTION;
DROP TABLE IF EXISTS "Opciones";
CREATE TABLE IF NOT EXISTS "Opciones" (
	"Id"	INTEGER NOT NULL,
	"Estado"	INTEGER NOT NULL,
	"Siguiente"	INTEGER NOT NULL,
	PRIMARY KEY("Id"),
	FOREIGN KEY("Estado") REFERENCES "Estados"("Id"),
	FOREIGN KEY("Siguiente") REFERENCES "Estados"("Id")
);
DROP TABLE IF EXISTS "Juegos";
CREATE TABLE IF NOT EXISTS "Juegos" (
	"Id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"Nombre"	TEXT
);
DROP TABLE IF EXISTS "Estados";
CREATE TABLE IF NOT EXISTS "Estados" (
	"Id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"Juego"	INTEGER NOT NULL,
	"Nombre"	TEXT NOT NULL,
	"Descripción"	TEXT NOT NULL,
	FOREIGN KEY("Juego") REFERENCES "Juegos"("Id")
);
DROP TABLE IF EXISTS "Usuarios";
CREATE TABLE IF NOT EXISTS "Usuarios" (
	"Id"	INTEGER NOT NULL UNIQUE,
	"Estado"	INTEGER NOT NULL DEFAULT 0,
	PRIMARY KEY("Id"),
	FOREIGN KEY("Estado") REFERENCES "Estados"("Id")
);
INSERT INTO "Opciones" VALUES (1,1,2);
INSERT INTO "Opciones" VALUES (2,1,3);
INSERT INTO "Opciones" VALUES (3,1,4);
INSERT INTO "Opciones" VALUES (4,1,5);
INSERT INTO "Juegos" VALUES (0,'Sin juego elegido');
INSERT INTO "Juegos" VALUES (1,'El rol de Cálico Electrónico');
INSERT INTO "Estados" VALUES (0,0,'Sin juego elegido','Estado "especial" que aglutina a los usuarios que no han elegido ningún juego');
INSERT INTO "Estados" VALUES (1,1,'¡Bienvenido!','Nuestro superhéroe favorito ha sido secuestrado por un villano desconocido. Por si eso no fuera suficiente, el equipo de héroes que estaba dedicado a buscarle, los Huérfanos Electrónicos... ¡tampoco aparecen!

¡¡ES TU MOMENTO DE ENTRAR EN ACCIÓN!!');
INSERT INTO "Estados" VALUES (2,1,'Investigas la base secreta','La puerta está cerrada, vas a tener que buscar la manera de entrar.');
INSERT INTO "Estados" VALUES (3,1,'Investigas la casa de Cálico Jack','Llamas al timbre de la casa y... ¡es la madre de Cálico! Te ofrece unos _boquerones en su tinta_, un _bocaillo shope_, un _bocata foigrá_ y unas _cocretas_. ¿Qué elegirás?');
INSERT INTO "Estados" VALUES (4,1,'Investigas Electrónica web','Nada, que no se abre la puerta. ¿Eso es un felpudo con la cara de Muzaman?');
INSERT INTO "Estados" VALUES (5,1,'Visita _ar chacho Migué_','¿Investigar? ¡Eso es para déblies! Vamos a visitar _ar chacho Migué_, que seguro que sabe algo o al menos nos venderá algún arma.');
COMMIT;
