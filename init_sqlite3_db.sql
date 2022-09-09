DROP TABLE IF EXISTS artist;
CREATE TABLE artist (
    artist_id integer PRIMARY KEY autoincrement,
    artist_name text NOT NULL
);

DROP TABLE IF EXISTS feat;
CREATE TABLE feat (
    feat_id integer PRIMARY KEY autoincrement,
    feat_date date NOT NULL ,
    primary_artist_id int REFERENCES artist(artist_id)
);

DROP TABLE IF EXISTS featured;
CREATE TABLE featured (
    featured_artist_id int REFERENCES artist(artist_id),
    feat_id int REFERENCES feat(feat_id) ,
    PRIMARY KEY (featured_artist_id,feat_id)
);