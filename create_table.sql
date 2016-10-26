-- Usage: > sqlite3 movies.db -init create_table.sql
DROP TABLE IF EXISTS movies;
CREATE TABLE movies (
    id              integer primary key,
    imdb_id         char(9) UNIQUE,
    title           varchar(100),
    year            smallint,
    rated           varchar(6),
    imdb_rating     float,
    metascore       smallint
);