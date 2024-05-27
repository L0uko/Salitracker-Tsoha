CREATE TABLE users (
id SERIAL PRIMARY KEY, 
username VARCHAR(50) UNIQUE, 
password TEXT
);

CREATE TABLE cardio (
id SERIAL PRIMARY KEY, 
cardioname TEXT,
lenght INTEGER,
times INTEGER 
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
exercise_id INTEGER REFERENCES exercise(id),
cardio_id INTEGER REFERENCES cardio(id) 
);

CREATE TABLE quotes (
    id SERIAL PRIMARY KEY,
    quotes TEXT
);
INSERT INTO quotes (quotes) VALUES ('Yeah Buddyy! -Ronnie Coleman');
INSERT INTO quotes (quotes) VALUES ('Lightweight! -Ronnie Coleman');
INSERT INTO quotes (quotes) VALUES ('Discipline is doing what you hate to do, but nonetheless doing it like you love it -Mike Tyson');
INSERT INTO quotes (quotes) VALUES ('We suffer more in imagination than in reality -Seneca');
INSERT INTO quotes (quotes) VALUES ('There are no shortcuts—everything is reps, reps, reps. -Arnold Schwarzenegger');
INSERT INTO quotes (quotes) VALUES ('The only bad workout is the one that didnt happen.');
INSERT INTO quotes (quotes) VALUES ('Stay hard -David Goggins');
INSERT INTO quotes (quotes) VALUES ('Whos gonna carry the boats? -David Goggins');
INSERT INTO quotes (quotes) VALUES ('Lock in');
INSERT INTO quotes (quotes) VALUES ('You are in danger of living a life so comfortable and soft, that you will die without ever realizing your true potential. -David Goggins');
INSERT INTO quotes (quotes) VALUES ('Dont stop when youre tired. Stop when youre done. -David Goggins');
INSERT INTO quotes (quotes) VALUES ('The most important conversation is the one you have with yourself. -David Goggins');