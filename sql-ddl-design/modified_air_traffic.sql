DROP DATABASE IF EXISTS air_traffic;

CREATE DATABASE air_traffic;

\c air_traffic;


-----------------Table for Passenger Names Only-----------------------
CREATE TABLE passengers (
    id SERIAL PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL
);

INSERT INTO passengers (first_name, last_name)
VALUES ('Jennifer', 'Finch'),
  ('Thadeus', 'Gathercoal'),
  ('Sonja', 'Pauley'),
  ('Jennifer', 'Finch'),
  ('Waneta', 'Skeleton'),
  ('Thadeus', 'Gathercoal'),
  ('Berkie', 'Wycliff'),
  ('Alvin', 'Leathes'),
  ('Berkie', 'Wycliff'),
  ('Cory', 'Squibbes');


-----------------------Table for Airlines------------------------

CREATE TABLE airlines (
    id SERIAL PRIMARY KEY,
    airline TEXT NOT NULL
);

INSERT INTO airlines (airline)
VALUES ('Delta'),
('United'),
('TUI Fly Belgium'),
('Air China'),
('British Airways'),
('Avianca Brasil'),
('American Airlines');

---------------------Table for Countries----------------------------

CREATE TABLE countries (
    id SERIAL PRIMARY KEY,
    country TEXT UNIQUE NOT NULL
);

INSERT INTO countries (country)
VALUES 
('United States'),
('France'),
('UAE'),
('Japan'),
('Brazil'),
('United Kingdom'),
('China'),
('Morocco'),
('Chile'),
('Mexico');

---------------------Table for Availabke Cities in Countries--------------------
CREATE TABLE countries_cities (
    id SERIAL PRIMARY KEY,
    country_id INTEGER REFERENCES countries,
    city TEXT NOT NULL
);

INSERT INTO countries_cities (country_id, city)
VALUES 
(1, 'Los Angeles'),
(1, 'Washington DC'),
(1, 'Seattle'),
(1, 'Cedar Rapids'),
(1, 'New York'),
(1, 'Charlotte'),
(2, 'Paris'),
(3, 'Dubai'),
(4, 'Tokyo'),
(5, 'Sao Paolo'),
(6, 'London'),
(1, 'Las Vegas'),
(10, 'Mexico City'),
(8, 'Casablanca'),
(7, 'Beijing'),
(1, 'Charlotte'),
(1, 'Chicago'),
(1, 'New Orleans'),
(9, 'Santiago');

----------------------Table for Tickets------------------------------------

CREATE TABLE tickets (
    id SERIAL PRIMARY KEY,
    passenger_id INTEGER REFERENCES passengers,
    seat TEXT NOT NULL,
    departure TIMESTAMP NOT NULL,
    arrival TIMESTAMP NOT NULL,
    airline_id INTEGER REFERENCES airlines,
    from_location INTEGER REFERENCES countries_cities,
    to_location INTEGER REFERENCES countries_cities
);

INSERT INTO tickets (passenger_id, seat, departure, arrival, airline_id, from_location, to_location)
VALUES 
    (1, '33B', '2018-04-08 09:00:00', '2018-04-08 12:00:00', 1, 1, 3),
    (2, '8A', '2018-12-19 12:45:00', '2018-12-19 16:15:00', 5, 9, 11),
    (3, '12F', '2018-01-02 07:00:00', '2018-01-02 08:03:00', 1, 1, 12),
    (4, '20A', '2018-04-15 16:50:00', '2018-04-15 21:00:00', 1, 3, 13),
    (5, '23D', '2018-08-01 18:30:00', '2018-08-01 21:50:00', 3, 7, 14),
    (6, '18C', '2018-10-31 01:15:00', '2018-10-31 12:55:00', 4, 8, 15),
    (7, '9E', '2019-02-06 06:00:00', '2019-02-06 07:47:00', 2, 5, 16),
    (8, '1A', '2018-12-22 14:42:00', '2018-12-22 15:56:00', 7, 4, 17),
    (9, '32B', '2019-02-06 16:28:00', '2019-02-06 19:18:00', 7, 15, 18),
    (10, '10D', '2019-01-20 19:30:00', '2019-01-20 22:45:00', 6, 10, 19);

-----------------------------------------------------------------------------

