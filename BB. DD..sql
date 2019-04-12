BEGIN TRANSACTION;
DROP TABLE IF EXISTS "Opciones";
CREATE TABLE IF NOT EXISTS "Opciones" (
	"Id"	INTEGER NOT NULL,
	"Estado"	INTEGER NOT NULL,
	"Nombre"	TEXT NOT NULL,
	"Seguiente"	INTEGER NOT NULL,
	PRIMARY KEY("Id"),
	FOREIGN KEY("Estado") REFERENCES "Estados"("Id")
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
INSERT INTO "Juegos" VALUES (0,'Sin juego elegido');
INSERT INTO "Juegos" VALUES (1,'El rol de Cálico Electrónico');
INSERT INTO "Estados" VALUES (0,0,'Sin juego elegido','Estado "especial" que aglutina a los usuarios que no han elegido ningún juego');
INSERT INTO "Estados" VALUES (1,1,'¡Bienvenido!','Nuestro superhéroe favorito ha sido secuestrado por un villano desconocido. Por si eso no fuera suficiente, el equipo de héroes que estaba dedicado a buscarle, los Huérfanos Electrónicos... ¡tampoco aparecen!

¡¡ES TU MOMENTO DE ENTRAR EN ACCIÓN!!');
COMMIT;
