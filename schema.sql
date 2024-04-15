CREATE TABLE users (
id SERIAL PRIMARY KEY, 
username VARCHAR(50) UNIQUE, 
password TEXT
);

CREATE TABLE cardio (
id SERIAL PRIMARY KEY, 
cardioname TEXT,
lenght INTEGER,
time TIME 
);

--CREATE TABLE popuplarity ( "needs work"
--id SERIAL PRIMARY KEY,

CREATE TABLE exercise (
id SERIAL PRIMARY KEY, 
sets INTEGER, 
weight INTEGER,
exercisename TEXT 
);  
Create TABLE visits (
id SERIAL PRIMARY KEY,
date TEXT ,
user_id INTEGER REFERENCES users(id),
exercise_id INTEGER REFERENCES exercise(id) 
);

CREATE TABLE quotes (
    id SERIAL PRIMARY KEY,
    quotes TEXT,
)
