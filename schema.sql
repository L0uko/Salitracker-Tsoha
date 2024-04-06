CREATE TABLE account (
id SERIAL PRIMARY KEY, 
name TEXT, 
password TEXT
);

--CREATE TABLE exercisename (
--id SERIAL PRIMARY KEY, 
--name TEXT
--);

CREATE TABLE exercise (
id SERIAL PRIMARY KEY, 
sets INTEGER, 
weight INTEGER,
account_id INTEGER REFERENCES account(id),
exercisename TEXT 
);  
Create TABLE visits (
id SERIAL PRIMARY KEY,
time INTEGER ,
exercise_id INTEGER REFERENCES exercise(id) 
);


Create TABLE accounts (
id SERIAL PRIMARY KEY, 
account_id INTEGER REFERENCES account(id)
);
--INSERT INTO exercisename (name) VALUES (benchpress);
--INSERT INTO exercisename (name) VALUES (squat);
--INSERT INTO exercisename (name) VALUES (deadlift);
--INSERT INTO exercisename (name) VALUES (barbellcurl);