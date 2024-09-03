USE [DB_BRILLITT]

CREATE TABLE YouTubeVideos (
    VideoID NVARCHAR(255) PRIMARY KEY,
	Canal NVARCHAR(255),
    Titulo NVARCHAR(255),
    Descripcion NVARCHAR(MAX),
    PublicadoEn DATETIME,
    Vistas BIGINT
);

INSERT INTO YouTubeVideos (VideoID, Canal, Titulo, Descripcion, PublicadoEn, Vistas)
VALUES ('123', 'Canal Ejemplo', 'Video de Prueba', 'Este es un video de prueba insertado directamente en la base de datos.', '2024-04-01 10:00:00', 100);

drop table YouTubeVideos

SELECT * from YouTubeVideos
where Canal LIKE 'Dua%'
order by PublicadoEn DESC

select distinct Canal from YouTubeVideos

ALTER LOGIN [COMERCIO\mariorith.arellan] WITH DEFAULT_DATABASE = [DB_BRILLITT];






