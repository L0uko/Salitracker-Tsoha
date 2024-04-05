Create TABLE visits (
id SERIAL PRIMARY KEY,
exersise_id REFERENCES exersise(id),
time CURRENT_TIME
);
CREATE TABLE excersise (
id SERIAL PRIMARY KEY, 
excersename_id REFERENCES excersisename(id), 
sets INTEGER, 
weight INTEGER
);  
CREATE TABLE excersisename (
id SERIAL PRIMARY KEY, 
name TEXT
);
Create TABLE users (
id SERIAL PRIMARY KEY, 
user_id REFERENCES user(id
);
CREATE TABLE user (
id SERIAL PRIMARY KEY, 
name TEXT, 
password TEXT
);
