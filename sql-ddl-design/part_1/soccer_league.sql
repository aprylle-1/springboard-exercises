DROP DATABASE IF EXISTS soccer_league_db;

CREATE DATABASE soccer_league_db;

\c soccer_league_db;


------------------Creating Teams Table----------------

CREATE TABLE teams (
    id SERIAL PRIMARY KEY,
    team_name TEXT UNIQUE NOT NULL
);

INSERT INTO teams (team_name)
VALUES ('Rush Hour'),('The Avengers'),('Amigos'),('Thunders');

------------------Creating Players Table----------------

CREATE TABLE players (
    id SERIAL PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT  NOT NULL,
    team_id INTEGER REFERENCES teams ON DELETE SET NULL
);

INSERT INTO players (first_name, last_name, team_id)
VALUES ('Rick', 'Grimes', 1),
('Lorry', 'Peters', 2),
('Shane','Smith', 3),
('Alex','Kane', 4),
('Carol','Rogers', 2);


------------------Creating Referees Table-----------------------
CREATE TABLE referees (
    id SERIAL PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT  NOT NULL
);

INSERT INTO referees (first_name, last_name)
VALUES ('Tinashe', 'Jo'),
('Devon', 'Sengphet'),
('Neta', 'Jyothi');


------------------Creating Seasons Table------------------------

CREATE TABLE seasons (
    id SERIAL PRIMARY KEY,
    start_date DATE UNIQUE NOT NULL,
    end_date DATE UNIQUE NOT NULL
);

INSERT INTO seasons (start_date, end_date)
VALUES ('1/1/2022', '3/30/2022'),
('4/1/2022', '6/30/2022'),
('7/1/2022', '9/30/2022'),
('10/1/2022', '12/30/2022');

----------------Creating Matches Table---------------------------

CREATE TABLE matches (
    id SERIAL PRIMARY KEY,
    match_date DATE NOT NULL,
    team1 INTEGER REFERENCES teams,
    team2 INTEGER REFERENCES teams,
    season INTEGER REFERENCES seasons
);

INSERT INTO matches (match_date, team1, team2, season)
VALUES ('7/10/2022', 1, 2, 3),
('6/08/2022', 1, 3, 2),
('1/5/2022', 2, 3, 1),
('3/04/2022', 3, 4, 1),
('4/23/2022', 1, 4, 2);

------------------Creating Goals Table---------------------------

CREATE TABLE goals (
    id SERIAL PRIMARY KEY,
    player_id  INTEGER REFERENCES players,
    match_id INTEGER REFERENCES matches
);

INSERT INTO goals (player_id, match_id)
VALUES (1,1),(2,1),(3,2),(4,4),(5,1),(1,5);

------------------Creating Matches_Referees------------------------

CREATE TABLE matches_referees (
    id SERIAL PRIMARY KEY,
    referee_id INTEGER REFERENCES referees,
    match_id INTEGER REFERENCES matches
);

INSERT INTO matches_referees (referee_id, match_id)
VALUES (1,1),(1,2),(2,3),(3,4),(3,5),(1,3);
