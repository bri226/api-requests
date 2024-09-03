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
