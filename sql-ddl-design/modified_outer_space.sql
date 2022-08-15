DROP DATABASE IF EXISTS outer_space;

CREATE DATABASE outer_space;

\c outer_space

----------------------------------------------------------------
CREATE TABLE orbits_around_values (
    id SERIAL PRIMARY KEY,
    orbits_around TEXT NOT NULL
);

INSERT INTO orbits_around_values (orbits_around)
VALUES ('The Sun'), ('Proxima Centauri'), ('Gliese 876');

---------------------------------------------------------------
CREATE TABLE galaxies (
    id SERIAL PRIMARY KEY,
    galaxy TEXT NOT NULL
);

INSERT INTO galaxies (galaxy)
VALUES ('Milky Way');

----------------------------------------------------------------
CREATE TABLE moons (
    id SERIAL PRIMARY KEY,
    moon TEXT NOT NULL
);

INSERT INTO moons (moon)
VALUES ('The Moon'), ('Phobos'), ('Deimos'),
('Naiad'),('Thalassa'),('Despina'),('Galatea'),
('Larissa'),('S/2004 N 1'),('Proteus'),
('Triton'), ('Nereid'), ('Halimede'), ('Sao'), ('Laomedeia'), ('Psamathe'), ('Neso');

------------------------------------------------------------------

CREATE TABLE planets (
    id SERIAL PRIMARY KEY,
    planet TEXT UNIQUE NOT NULL,
    orbital_period_in_years FLOAT
);

INSERT INTO planets (planet, orbital_period_in_years)
VALUES ('Earth', 1),
('Mars', 1.88),
('Venus', 0.62),
('Neptune', 164.8),
('Proxima Centauri b', 0.03),
('Gliese 876 b', 0.23);

-------------------------------------------------------------------

CREATE TABLE planets_orbits_around_values (
    id SERIAL PRIMARY KEY,
    planet_id INTEGER REFERENCES planets,
    orbits_around_id INTEGER REFERENCES orbits_around_values
);

INSERT INTO planets_orbits_around_values (planet_id, orbits_around_id)
VALUES (1,1),(2,1),(3,1),(4,1),(5,2),(6,3);

---------------------------------------------------------------------

CREATE TABLE planets_galaxies (
    id SERIAL PRIMARY KEY,
    planet_id INTEGER REFERENCES planets,
    galaxy_id INTEGER REFERENCES galaxies
);

INSERT INTO planets_galaxies (planet_id, galaxy_id)
VALUES (1,1),(2,1),(3,1),(4,1),(5,1),(6,1);

-----------------------------------------------------------------------

CREATE TABLE planets_moons (
    id SERIAL PRIMARY KEY,
    planet_id INTEGER REFERENCES planets,
    moon_id INTEGER REFERENCES moons
);

INSERT INTO planets_moons (planet_id, moon_id)
VALUES (1,1),(2,2),(2,3),(4,4),(4,5),(4,6),(4,7),(4,8),(4,9),(4,10),(4,11),(4,12),(4,13),(4,14),(4,15),(4,16),(4,17);