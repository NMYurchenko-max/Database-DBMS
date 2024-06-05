CREATE TABLE IF NOT EXISTS genre(
    id SERIAL PRIMARY KEY,
    genre_name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS artist(
    id SERIAL PRIMARY KEY,
    artist_name VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS genre_artist(
    genre_id INTEGER REFERENCES genre(id),
    artist_id INTEGER REFERENCES artist(id),
    CONSTRAINT genre_artist_pk PRIMARY KEY (genre_id, artist_id)
);

CREATE TABLE IF NOT EXISTS album(
    id SERIAL PRIMARY KEY,
    album_name VARCHAR(100) NOT NULL,
    year_of_release INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS artist_album(
    artist_id INTEGER REFERENCES artist(id),
    album_id INTEGER REFERENCES album(id),
    CONSTRAINT artist_album_pk PRIMARY KEY  (artist_id, album_id)
);

CREATE TABLE IF NOT EXISTS track(
    id SERIAL PRIMARY KEY,
    track_name VARCHAR(100) NOT NULL UNIQUE,
    duration INTEGER NOT NULL,
    album_id INTEGER REFERENCES album(id)
);

CREATE TABLE IF NOT EXISTS collection_of_songs(
    id SERIAL PRIMARY KEY,
    collection_name VARCHAR(100) NOT NULL,
    year_of_release INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS collection_track(
    collection_id INTEGER REFERENCES collection_of_songs(id),
    track_id INTEGER REFERENCES track(id),
    CONSTRAINT collection_track_pk PRIMARY KEY (collection_id, track_id)
);


