DROP DATABASE IF EXISTS medical_center;

CREATE DATABASE medical_center;

\c medical_center;

--------Database Spreadsheet for Reference----------
------- https://docs.google.com/spreadsheets/d/1NcL0ZopqW03weIu0wNd-xmC6vg_gTkhBIvFTQuYNoz0/edit#gid=0 ----------

--------Creating Doctors Table with Values----------
CREATE TABLE doctors (
    id SERIAL PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL
);

INSERT INTO doctors (first_name, last_name)
VALUES ('John', 'Smith'), ('Jane', 'Doe'), ('Allan', 'Peters');

-- --------Creating Patient Table with Values------------
CREATE TABLE patients (
    id SERIAL PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL
);

INSERT INTO patients (first_name, last_name)
VALUES ('Rick', 'Grimes'), ('Lorry', 'Peters'), ('Shane', 'Smith');

--------Creating Diseases Table with Values----------

CREATE TABLE diseases (
    id SERIAL PRIMARY KEY,
    disease_name TEXT NOT NULL
);

INSERT INTO diseases (disease_name)
VALUES ('Allergies'), ('Colds and Flu'),
('Conjungtivitis'), ('Diarrhea'),
('Headaches'), ('Stomach Aches');

-----------Patient-Doctor Table with Values--------------

CREATE table patient_doctor (
    id SERIAL PRIMARY KEY,

    --------If patient gets deleted, ok if patient-doctor record gets deleted-------
    patient_id INTEGER REFERENCES patients ON DELETE CASCADE,

    --------If doctor gets deleted, patient-doctor record kept, doctor set to null instead---------
    doctor_id INTEGER REFERENCES doctors ON DELETE SET NULL
);

INSERT INTO patient_doctor (patient_id, doctor_id)
VALUES (1,1), (1,2), (2,1), (2,3), (3,1);

------------Patient-Diseases Table with Values---------------

CREATE TABLE patient_diseases (
    id SERIAL PRIMARY KEY,
    patient_id INTEGER REFERENCES patients ON DELETE CASCADE,
    disease_id INTEGER REFERENCES diseases ON DELETE CASCADE
);

INSERT INTO patient_diseases (patient_id, disease_id)
VALUES (1,1), (1,2), (2,3), (3,3), (3,4), (3,5); 