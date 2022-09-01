DROP TABLE IF EXISTS artist;
CREATE TABLE artist (
    id_artist int PRIMARY KEY,
    artist_name varchar(255) NOT NULL
);

DROP TABLE IF EXISTS feat;
CREATE TABLE feat (
    id_feat int PRIMARY KEY,
    feat_date date  NOT NULL ,
    id_primary_artist int  NOT NULL,
    FOREIGN KEY (id_primary_artist) REFERENCES artist(id_artist)
);

DROP TABLE IF EXISTS featured;
CREATE TABLE featured (
    id_featured_artist int  NOT NULL ,
    id_feat int  NOT NULL ,
    PRIMARY KEY (id_featured_artist,id_feat),
    FOREIGN KEY (id_featured_artist) REFERENCES artist(id_artist),
    FOREIGN KEY (id_feat) REFERENCES feat(id_feat)
);
