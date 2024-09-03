-- Creación de la tabla Artist
CREATE TABLE Artist (
    id_artist VARCHAR(50) PRIMARY KEY,
    name NVARCHAR(100) NOT NULL
);

-- Creación de la tabla Album
CREATE TABLE Album (
    id_album VARCHAR(50) PRIMARY KEY,
    name NVARCHAR(100) NOT NULL,
    id_artist VARCHAR(50) NOT NULL,
    release_date DATE,
    total_tracks INT,
    release_date_precision VARCHAR(10),
    url_spotify NVARCHAR(255),
    FOREIGN KEY (id_artist) REFERENCES Artist(id_artist)
);

-- Creación de la tabla Track
CREATE TABLE Track (
    id_track VARCHAR(50) PRIMARY KEY,
    id_album VARCHAR(50),
    name NVARCHAR(100) NOT NULL,
    popularity INT,
    duration_ms INT,
    explicit BIT,
    preview_url NVARCHAR(255),
    FOREIGN KEY (id_album) REFERENCES Album(id_album)
);

-- Creación de la tabla Collaboration
CREATE TABLE Collaboration (
    id_track VARCHAR(50),
    id_artist VARCHAR(50),
    PRIMARY KEY (id_track, id_artist),
    FOREIGN KEY (id_track) REFERENCES Track(id_track),
    FOREIGN KEY (id_artist) REFERENCES Artist(id_artist)
);

/*************************************
		NO CORRER ESTO
**************************************/

-- Inserción de datos en Artist
INSERT INTO Artist (id_artist, name) VALUES ('1', 'Shakira');

-- Inserción de datos en Album
INSERT INTO Album (id_album, name, id_artist, release_date, total_tracks, release_date_precision, url_spotify)
VALUES ('101', 'El Dorado', '1', '2017-05-26', 13, 'day', 'https://open.spotify.com/album/3ElMk7XVX0aWdLfkZXfjMg');

-- Inserción de datos en Track
INSERT INTO Track (id_track, id_album, name, popularity, duration_ms, explicit, preview_url)
VALUES ('1001', '101', 'Chantaje', 80, 195840, 0, 'https://p.scdn.co/mp3-preview/');

-- Inserción de datos en Collaboration
INSERT INTO Collaboration (id_track, id_artist) VALUES ('1001', '2');

/*************************************
			SEPARADOR
**************************************/

SELECT * FROM ARTIST
SELECT * FROM ALBUM
SELECT * FROM TRACK
WHERE explicit <> 0
SELECT * FROM COLLABORATION

DROP TABLE ARTIST 
DROP TABLE ALBUM
DROP TABLE TRACK
DROP TABLE COLLABORATION

ALTER TABLE track NOCHECK CONSTRAINT ALL;

/*************************************
PARA ELIMINAR UN ALBUM QUE TIENE SOLO 1 TRACK
**************************************/
-- Eliminar colaboraciones de pistas que van a ser eliminadas
DELETE FROM Collaboration
WHERE id_track IN (
    SELECT id_track
    FROM Track
    WHERE id_album IN (
        SELECT id_album
        FROM Album
        WHERE total_tracks = 1
    )
);

DELETE FROM Track
WHERE id_album IN (
    SELECT id_album
    FROM Album
    WHERE total_tracks = 1
);

-- Luego eliminar los álbumes
DELETE FROM Album
WHERE total_tracks = 1;



SELECT	A.name AS Nombre_del_Album,
		A.release_date Fecha_Publicacion,
		T.name AS Nombre_de_Pista,
		CAST(T.duration_ms / 60000.0 AS DECIMAL(10, 2)) AS Duracion_En_Minutos,
		AR.name AS Nombre_del_Colaborador
FROM	Album A
JOIN    Artist ARt ON A.id_artist = ARt.id_artist
JOIN    Track T ON A.id_album = T.id_album
LEFT JOIN    Collaboration C ON T.id_track = C.id_track
LEFT JOIN    Artist AR ON C.id_artist = AR.id_artist AND AR.id_artist != ARt.id_artist
WHERE   ARt.name = 'Shakira'
ORDER BY  A.name, T.name, A.release_date ASC
