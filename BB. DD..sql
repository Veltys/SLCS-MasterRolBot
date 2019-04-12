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
INSERT INTO "Estados" VALUES (0,0,'Sin juego elegido','Estado "especial" que aglutina a los usuarios que no han elegido ningún juego');
INSERT INTO "Juegos" VALUES (0,'Sin juego elegido');
COMMIT;
