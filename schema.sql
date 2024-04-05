CREATE TABLE account (
id SERIAL PRIMARY KEY, 
name TEXT, 
password TEXT
);

CREATE TABLE exercisename (
id SERIAL PRIMARY KEY, 
name TEXT
);

CREATE TABLE exercise (
id SERIAL PRIMARY KEY, 
sets INTEGER, 
weight INTEGER,
account_id INTEGER REFERENCES account(id),
excersename_id INTEGER REFERENCES exercisename(id) 
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
