DROP DATABASE IF EXISTS air_traffic_modified;

CREATE DATABASE air_traffic_modified;

\c air_traffic_modified;


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
CREATE TABLE cities (
    id SERIAL PRIMARY KEY,
    city TEXT NOT NULL
);

INSERT INTO cities (city)
VALUES 
('Los Angeles'),
('Washington DC'),
('Seattle'),
('Cedar Rapids'),
('New York'),
('Charlotte'),
('Paris'),
('Dubai'),
('Tokyo'),
('Sao Paolo'),
('London'),
('Las Vegas'),
('Mexico City'),
('Casablanca'),
('Beijing'),
('Charlotte'),
('Chicago'),
('New Orleans'),
('Santiago');

----------------------Table for Tickets------------------------------------

CREATE TABLE tickets (
    id SERIAL PRIMARY KEY,
    passenger_id INTEGER REFERENCES passengers,
    seat TEXT NOT NULL,
    departure TIMESTAMP NOT NULL,
    arrival TIMESTAMP NOT NULL,
    airline_id INTEGER REFERENCES airlines,
    from_city INTEGER REFERENCES cities,
    from_country INTEGER REFERENCES countries,
    to_city INTEGER REFERENCES cities,
    to_country INTEGER REFERENCES countries
);

INSERT INTO tickets (passenger_id, seat, departure, arrival, airline_id, from_city, from_country, to_city, to_country)
VALUES 
    (1, '33B', '2018-04-08 09:00:00', '2018-04-08 12:00:00', 1, 2, 1, 3, 1),
    (2, '8A', '2018-12-19 12:45:00', '2018-12-19 16:15:00', 5, 9, 4, 11, 6),
    (3, '12F', '2018-01-02 07:00:00', '2018-01-02 08:03:00', 1, 1, 1, 12, 1)

-----------------------------------------------------------------------------

SELECT passengers.first_name, passengers.last_name, 
seat, departure, arrival, 
airlines.airline, cities.city as from_city, 
countries.country as from_country, 
cities.city as to_city, 
countries.country as to_country 
FROM tickets
JOIN passengers
ON (tickets.passenger_id = passengers.id)
JOIN cities
ON (cities.id = tickets.to_city)
ON (cities.id = tickets.from_city)
JOIN countries
ON (countries.id = tickets.from_country)
ON (countries.id = tickets.to_country)