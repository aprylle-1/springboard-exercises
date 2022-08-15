DROP DATABASE IF EXISTS craigslist_db;

CREATE DATABASE craigslist_db;

\c craigslist_db;


--------------------------------------Table Spreadsheet for Reference-----------------------------------------------
------https://docs.google.com/spreadsheets/d/1NcL0ZopqW03weIu0wNd-xmC6vg_gTkhBIvFTQuYNoz0/edit#gid=1499381478-------

--------------------------Creating Regions Table and Populating It--------------------------
CREATE TABLE regions (
    id SERIAL PRIMARY KEY,
    region TEXT
);

INSERT INTO regions (region)
VALUES ('San Francisco'), ('Atlanta'), ('Seattle');

---------------------------Creating Users Table and Populating It---------------------------

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL
);

INSERT INTO users (first_name, last_name)
VALUES ('Rick', 'Grimes'),
('Lorry', 'Peters'),
('Shane','Smith'),
('Alex','Kane');

----------------------------Creating Categories Table and Populating It------------------------

CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    category TEXT NOT NULL
);

INSERT INTO categories (category)
VALUES ('Jobs'),
('Housing'),
('Items Wanted'),
('Gigs'),
('Resumes'),
('Discussion Forum');

---------------------------Creating User_Region (Preferences) Table and Populating It---------------

CREATE TABLE user_region (
    id SERIAL PRIMARY KEY,

    -------Delete Record if user does not exist--------
    user_id INTEGER REFERENCES users ON DELETE CASCADE,

    -------Set User's Region to NULL IF Region Does Not Exist--------
    region_id INTEGER REFERENCES regions ON DELETE SET NULL
);

INSERT INTO user_region (user_id, region_id)
VALUES (1,1),(2,1),(3,2),(4,3);

---------------------------Creating Posts Table and Populating It----------------------

CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    user_region_id INTEGER REFERENCES user_region,
    post_location TEXT,
    post_title TEXT NOT NULL,
    post_text TEXT NOT NULL,
    category_id INTEGER REFERENCES categories ON DELETE SET NULL
);

INSERT INTO posts (user_region_id, post_location, post_title, post_text, category_id)
VALUES (1, 'Alameda', 'Couch for Sale', 'Buy this couch, it is cheap and clean', 3),
(2, 'Albany', 'Wanted: Garage Cleaner', 'Clean my garage, I will pay you', 1),
(1, 'Brentwood', 'Nintendo Swich OLED: Buy or not?', 'Making a decision to buy a new console. What are the pros and cons of this?', 6),
(3, 'Georgia', 'Buying: Game Boy Color', 'I collect old toys. If anyone is selling their old GBC, call me', 3),
(4, 'Washington', 'House for Sale', 'I am moving, buy my house', 2);